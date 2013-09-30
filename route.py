#! /usr/bin/env python

from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, jsonify
from flask_oauth import OAuth
from models import User, Email
from functools import wraps
from datetime import datetime, timedelta
import mongo
import mailgun
import os
import hashlib, hmac
import sha3


app = Flask(__name__)
app.secret_key = os.environ.get('API_SECRET_KEY')
secret = os.environ.get('SECRET')

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key= os.environ.get('CONSUMER_KEY'),
    consumer_secret=os.environ.get('CONSUMER_SECRET'),
    request_token_params={'scope': ('email, ')}
)

def logged_in(f):
    @wraps(f)
    def decoratd_function(*args, **kwargs):
        if session.get('logged_in'):
            return f(*args, **kwargs)
        else:
            flash('Please log in first.', 'error')
            return redirect('/')
    return decoratd_function

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))

@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('find_symptoms')

    if resp is None or 'access_token' not in resp:
        return redirect('/')

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    data = facebook.get('/me').data
    fb_email = data.get('email')

    email = mongo.check_user(fb_email)

    if email:
        session['email'] = email
        return redirect('/find_symptoms')

    return redirect('/sign_up')

@app.route('/sign_up', methods=['GET', 'POST'])
@logged_in
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        fb_email = request.form['fb_email']
        email = request.form['email']

        if not first_name or not last_name or not fb_email or not email:
            flash(u'Please fill out all required fields', 'error')
            return render_template('sign_up.html')

        u = User(first_name=first_name, last_name=last_name, fb_email=fb_email,email=email)

        if not mongo.check_user(u.fb_email):
            s = hashlib.sha3_512()
            s.update((secret+u.email).encode('utf-8'))
            token = s.hexdigest()
            mongo.signed_up(u)
            mailgun.send_verification(u, token)
            return render_template('verify.html')

        else:
            flash('%s, we see you have already signed up! Please log in.' % (first_name), "success")
            return redirect('/')

    else:
        return render_template('404.html'), 404

@app.route('/verify', methods=['GET'])
def verify_token():
    email = request.args.get('email', '')
    token = request.args.get('token', '')

    user = mongo.verified(email)

    if user:
        u = User.from_json(user)

        s = hashlib.sha3_512()
        s.update((secret+u.email).encode('utf-8'))

        if s.hexdigest() == token:
            mongo.add_user(u)
            mailgun.add_list_member(u)
            session['email'] = u.email
            flash('Welcome %s, thanks for signing up!' % (u.first_name), "success")
            mongo.delete_verified(u.email)
            return redirect('/find_symptoms')
    flash('We could not verify this email', 'error')
    return render_template('404.html')

@app.route('/logout')
@logged_in
def logout():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/feedback')
@logged_in
def feedback():
    return render_template('feedback.html')
    
@app.route('/get_feedback')
@logged_in
def get_feedback():
    email = session['email']
    feedback = request.args['feedback']
    mongo.save_feedback(email=email, message=feedback)
    flash('We appreciate your feedback! Thanks for using Symptomatic!')
    return redirect('/')


@app.route('/messages', methods=['POST'])
def messages():
    # Handler for HTTP POST to http://symptomatic.me/messages
    api_key = os.environ.get('MAILGUN_APIKEY')
    token = request.form.get('token')
    signature = request.form.get('signature')
    sender = request.form.get('sender')
    recipient = request.form.get('recipient')
    stripped_text = request.form.get('stripped-text', '')
    timestamp = request.form.get('timestamp')

    verified = _verify(api_key=api_key, token=token, timestamp=timestamp, signature=signature)
    if app.debug or verified:
        if sender != "symptomatic@symptomatic.mailgun.org":
            date = datetime.fromtimestamp(int(timestamp))
            e = Email.validate(date=date, sender=sender, stripped_text=stripped_text, symptoms=stripped_text.splitlines())
            mongo.save_email(e)
            return "OK"

        return "Nope", 404

@app.route('/find_symptoms')
@logged_in
def find_symptoms():
    return render_template('select.html')

@app.route('/show_all')
@logged_in
def find_all():
    email = session['email']
    symptoms = mongo.find_all_symptoms(email)

    return render_template('aggregate_view.html', start_date=None, end_date=None, symptoms=symptoms)

@app.route('/show_symptoms')
@logged_in
def show_symptoms():
    email = session['email']
    start_date = request.args['start_date']
    end_date = request.args['end_date']

    if not start_date or not end_date or not email:
        flash(u'Please fill in all required fields', 'error')
        return render_template('select.html')

    #converts date into datetime object to be able to compare
    start_datetime = datetime.strptime(start_date, "%m/%d/%Y")
    end_datetime = datetime.strptime(end_date, "%m/%d/%Y")

    symptoms = mongo.find_symptoms(email, start_datetime, end_datetime)

    if more_than_week(start_datetime, end_datetime):
        return render_template('aggregate_view.html', start_date=start_date, end_date=end_date, symptoms=symptoms)

    return render_template('micro_view.html', start_date=start_date, end_date=end_date, symptoms=symptoms)

def more_than_week(d1, d2):
    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))

    difference = (monday2 - monday1).days
    if difference >= 7:
        return True
    return False

@app.route('/symptoms')
@logged_in
def symptons_json():
    email = session['email']

    filter = { "sender" : email }

    start_date = request.args.get('start_date')
    if start_date:
        filter['start_date'] = datetime.strptime(start_date, "%m/%d/%Y")

    end_date = request.args.get('end_date')
    if end_date:
        filter['end_date'] = datetime.strptime(end_date, "%m/%d/%Y")

    return jsonify(mongo.find_symptoms_count(filter))


# This chunk was taken from the MailGun Docs
def _verify(api_key, token, timestamp, signature):
    return signature == hmac.new(
                             key=api_key,
                             msg='{}{}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 58733))
    app.run(debug=True, host='0.0.0.0', port=port)


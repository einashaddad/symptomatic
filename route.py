#! /usr/bin/env python

from flask import Flask, render_template, request, url_for
import os
#import httplib
import mongo
import datetime

app = Flask(__name__) 

@app.route('/')
def index():
	return render_template('index.html')

# Handler for HTTP POST to http://symptomatic.me/messages
@app.route('/messages', methods=['GET', 'POST'])
def on_incoming_message():
	if request.method == 'POST':
		sender = request.form.get('sender')
		recipient = request.form.get('recipient')

		body_plain = request.form.get('body-plain', '')
		timestamp = request.form.get('timestamp', '')

		mongo.saving_email(timestamp, sender, body_plain.splitlines(), body_plain)

		return "OK"
		

@app.route('/show_symptoms', methods=['GET', 'POST'])
def show_symptoms():
	if request.method == 'GET':
		return render_template('select.html')
	else:
		if request.form.get('Submit'):
			email = request.form.get('email')
			
			start_date = request.form.get('start_date')
			end_date = request.form.get('end_date')

			if not start_date and end_date and email:
				return render_template('select.html')

			#converts date into datetime object to be able to compare
			start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
			end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d") 
 
 			#timedelta(1) adds one day to end_datetime compare the entire day
			symptoms = mongo.reading_email(email, start_datetime, end_datetime + datetime.timedelta(1))
			return render_template('show_symptoms.html', start_date=start_date, end_date=end_date, symptoms=symptoms)
		
		elif request.form.get("Find All"):
			email = request.form.get('email')
			if not email:
				return render_template('select.html')

			symptoms = mongo.reading_email(email, None, None, True)
			return render_template('show_symptoms.html', start_date=None, end_date=None, symptoms=symptoms)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 35779))
	app.run(debug=True, host='0.0.0.0', port=port)
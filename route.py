#! /usr/bin/env python

from flask import Flask, render_template, request, url_for
import os
import httplib
import saving_email

app = Flask(__name__) 

# Handler for HTTP POST to http://symptomatic.me/messages
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/messages', methods=['GET', 'POST'])
def on_incoming_message():
	#TODO save in database
	if request.method == 'POST':
		sender = request.form.get('sender')
		recipient = request.form.get('recipient')

		body_plain = request.form.get('body-plain', '')
		timestamp = request.form.get('timestamp', '')

		saving_email.main(timestamp, sender, recipient, body_plain.splitlines(), body_plain)

		return "OK"

	else:
		return render_template('messages.html')

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 35779))
	app.run(debug=True, host='0.0.0.0', port=port)
#! /usr/bin/env python

import requests
import smtplib
import os
import mongo

user_name = os.environ.get('MAILGUN_USERNAME')
api_key = os.environ.get('MAILGUN_APIKEY')

login = os.environ.get('MAILGUN_LOGIN')
password = os.environ.get('MAILGUN_PASSWORD')

s = requests.Session()
s.auth = user_name, api_key 


def send_simple_message():
	"""
	Sends a an email using the mailgun API
	"""
	return requests.post(
		"https://api.mailgun.net/v2/symptomatic.mailgun.org/messages",
		auth=(user_name, api_key),
		data={"from": "Symptomatic <symptomatic@symptomatic.mailgun.org>",
				"to": mongo.list_emails(),
				"subject": "How are you feeling today?",
				"html": "<html><h4>Hi %recipient.first%,<br><br>Please take a minute to write out any symptoms you are feeling today.</h4></html>"},
				"recipient-variables": mongo.emails_to_json())

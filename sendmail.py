#! /usr/bin/env python

import requests
import smtplib
import os

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
				"to": ["einas.haddad@gmail.com"],
				"subject": "How are you feeling today?",
				"html": "<html><h3>Please take a minute to write out any symptoms you are feeling today.</h3></html>"})

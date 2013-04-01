#! /usr/bin/env python

import requests
import smtplib

user_name = "api"
api_key = "key-3b36qwxrjcphvtavdiskcmwjq2issg92"

login = "postmaster@symptomatic.mailgun.org"
password = "0hgnsoknpcd1"

s = requests.Session()
s.auth = user_name, api_key 


def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v2/symptomatic.mailgun.org/messages",
		auth=(user_name, api_key),
		data={"from": "Symptomatic <symptomatic@symptomatic.mailgun.org>",
				"to": ["einas.haddad@gmail.com"],
				"subject": "How are you feeling today?",
				"html": "<html><h3>Please take a minute to write out any symptoms you are feeling today.</h3></html>"})

# if __name__ == '__main__':
# 	send_simple_message()
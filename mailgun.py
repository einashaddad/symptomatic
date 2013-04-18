#! /usr/bin/env python

import requests
import smtplib
import os

user_name = os.environ.get('MAILGUN_USERNAME')
api_key = os.environ.get('MAILGUN_APIKEY')

login = os.environ.get('MAILGUN_LOGIN')
password = os.environ.get('MAILGUN_PASSWORD')

secret = os.environ.get('SECRET')

s = requests.Session()
s.auth = user_name, api_key 

def daily_email():
    return requests.post(
        "https://api.mailgun.net/v2/symptomatic.mailgun.org/messages",
        auth=(user_name, api_key),
        data={"from": "Symptomatic <symptomatic@symptomatic.mailgun.org>",
                "to": "users@symptomatic.mailgun.org",
                "subject": "How are you feeling today?",
                "html": "<html><h4>Hi %recipient_fname%,<br><br>\
                Please take a minute to write out any symptoms you are feeling today.\
                <br><br>Sincerely,<br>The Symptomatic Team</h4></html>"},
                )

def create_mailing_list():
    return requests.post(
        "https://api.mailgun.net/v2/lists",
        auth=(user_name, api_key),
        data={'address': 'users@symptomatic.mailgun.org',
              'description': "Users"})

def add_list_member(u):
    return requests.post(
        "https://api.mailgun.net/v2/lists/users@symptomatic.mailgun.org/members",
        auth=(user_name, api_key),
        data={'subscribed': True,
              'address': u.email,
              'name': u.first_name + u.last_name,
              'description': "User"})

def send_verification(u, token):
    return requests.post(
        "https://api.mailgun.net/v2/symptomatic.mailgun.org/messages",
        auth=(user_name, api_key),
        data={"from": "Symptomatic <symptomatic@symptomatic.mailgun.org>",
            "to": u.email,
            "subject": "Symptomatic Accout Confirmation",
            "html": "<html><h4>Hi %s,<br><br>Thanks for signing up! \
                    We're almost ready to activate your account. We just need you to \
                    verify your email address.<br><br>\
                    Please click on the following link to verify:\
                    http://localhost:5000/verify?email=%s&token=%s'\
                    <br><br>- The Symptomatic Team</h4></html>" % (u.first_name, u.email, token) }
            )




#! /usr/bin/env python
import requests
from werkzeug.datastructures import MultiDict

user_name = os.environ.get('MAILGUN_USERNAME')
api_key = os.environ.get('MAILGUN_APIKEY')

login = os.environ.get('MAILGUN_LOGIN')
password = os.environ.get('MAILGUN_PASSWORD')

def create_route():
	return requests.post(
		"https://api.mailgun.net/v2/routes",
		auth=(user_name, api_key),
		data=MultiDict([("priority", 1),
						("description", "email route"),
						("expression", "match_recipient('')"),
						("action", "forward('http://shrouded-tundra-4968.herokuapp.com/messages')"),
						("action", "stop()")]))

create_route()
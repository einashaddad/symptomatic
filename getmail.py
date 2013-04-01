#! /usr/bin/env python
import requests
from werkzeug.datastructures import MultiDict

user_name = "api"
api_key = "key-3b36qwxrjcphvtavdiskcmwjq2issg92"

login = "postmaster@symptomatic.mailgun.org"
password = "0hgnsoknpcd1"

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
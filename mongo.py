#! /usr/bin/env python

import pymongo
import sys
import os
from urlparse import urlparse
import datetime

MONGOHQ_URL = os.environ.get('MONGOHQ_URL')

if MONGOHQ_URL:
  connection = pymongo.Connection(MONGOHQ_URL, safe=True)	# safe enables pymongo to wait to get all errors (getlasterror call)
  db = connection[urlparse(MONGOHQ_URL).path[1:]]	# this parses the app number from the url (app13974775)
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.test

def saving_email(timestamp, sender, list_of_symptoms, body_plain):

	email = db.email

	date = datetime.datetime.fromtimestamp(int(timestamp))	#converts timestamp into datetime type

	r_email = {"date": date, "sender": sender, "symptoms": list_of_symptoms, "email": body_plain} 	# json object 

	try:
		email.insert(r_email) #inserts into the db

	except:
		print "insert failed:", sys.exec_info()[0]

def reading_email(sender=None, start_date=None, end_date=None, find_all=False):
	email = db.email 
	result = []
	if sender and start_date and end_date:
			for message in email.find( { "sender" : sender, "date" : { "$gte" : start_date, "$lt" : end_date } } ):
				for symptom in message['symptoms']:
					result.append(symptom)
	elif find_all:
		for message in email.find({"sender" : sender}):
			for symptom in message['symptoms']:
				result.append(symptom)

	return set(result)
		
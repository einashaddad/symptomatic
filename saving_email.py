import pymongo
import sys
import os
from urlparse import urlparse

MONGOHQ_URL = os.environ.get('MONGOHQ_URL')

if MONGOHQ_URL:
  connection = pymongo.Connection(MONGOHQ_URL, safe=True)	# safe enables pymongo to wait to get all errors (getlasterror call)
  db = connection[urlparse(MONGOHQ_URL).path[1:]]	# this parses the app number from the url (app13974775)
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.test

def main(timestamp, sender, recipient, list_of_symptoms, body_plain):

	email = db.email

	r_email = {"_id": timestamp, "sender": sender, "recipient" : recipient,\
			   "symptoms": list_of_symptoms, "email": body_plain} 	 # json object 

	try:
		email.insert(r_email) #inserts into the db

	except:
		print "insert failed:"#, sys.exec_info()[0]

if __name__ == '__main__':
	main(sender, recipient, subject, body_plain)
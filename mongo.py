import pymongo
import sys
import os
import datetime
from urlparse import urlparse


MONGOHQ_URL = os.environ.get('MONGOHQ_URL')

if MONGOHQ_URL:
  connection = pymongo.Connection(MONGOHQ_URL, safe=True)   # safe enables pymongo to wait to get all errors (getlasterror call)
  db = connection[urlparse(MONGOHQ_URL).path[1:]]   # this parses the app number from the url (app13974775)
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.test

def save_email(e):
    """
    Saves the symptoms along with the timestamp, sender and email in mongodb
    """
    email = db.email
    r_email = e.to_json()

    #TODO: Add more error handling
    try:
        email.insert(r_email) #inserts into the db
    except:
        print "insert failed:", sys.exec_info()[0]

def reading_email(sender=None, start_date=None, end_date=None, find_all=False):
    """
    Returns the symptoms from mongodb

    Finds the entry according to the sender (the person logged in), 
    the start date and the end date
    """
    email = db.email 
    result = []
    if sender and start_date and end_date:
            for message in email.find( { "sender" : sender, 
                                         "date" : { "$gte" : start_date, 
                                         "$lt" : end_date } } ):
                for symptom in message['symptoms']:
                    result.append(symptom)

  #TODO: SHOULD CREATE TWO DIFFERENT FUNCTIONS FOR FINDALL AND OTHER
    elif find_all:
        for message in email.find({"sender" : sender}):
            for symptom in message['symptoms']:
                result.append(symptom)

    return set(result)

def check_user(email):
    """
    Returns True and the email when the user is found or False when the user is a new user
    """
    user = db.user

    user_found = user.find_one( { "fb_email": email } )

    if user_found:
        return user_found['email']  # True when user is found
    return None     # False when user is new

def add_user(u):
    """
    Accepts models.User class Adds a new user in mongodb 
    """
    user = db.user

    save_user = u.to_json()

    try:
        user.insert(save_user)
    except:
        print "insert failed:", sys.exec_info()[0]

        
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

    #TODO: Figure out more insertion errors and catch all
    try:
        email.insert(e.to_json()) 
    except:
        print "insert failed:", sys.exec_info()[0]

def find_symptoms(sender=None, start_date=None, end_date=None):
    """
    Returns the symptoms from mongodb

    Finds the entry according to the sender (the person logged in), 
    the start date and the end date
    """
    end_date += datetime.timedelta(1)
    email = db.email 
    messages = email.find({ "sender" : sender, 
                            "date" : { "$gte" : start_date, 
                                       "$lt" : end_date } })
    result = set(symptom for message in messages
                         for symptom in message['symptoms'])
    return result

def find_all_symptoms(sender=None):
    email = db.email 
    # Convert to comprehension syntax.
    result = []
    for message in email.find({"sender" : sender}):
        for symptom in message['symptoms']:
            result.append(symptom)
    return set(result)

def check_user(fb_email):
    """
    Returns email when the user is found or None when the user is a new user
    """
    # TODO: Split check_user into check_fb_email() and user_exists()
    user = db.user
    user_found = user.find_one( { "fb_email": fb_email } )

    if user_found:
        return user_found['email']  
    return None     

def add_user(u):
    """
    Accepts models.User class Adds a new user in mongodb 
    """
    user = db.user
    #TODO: Add more error handling when inserting into DB
    try:
        user.insert(u.to_json())
    except:
        print "insert failed:", sys.exec_info()[0]

        

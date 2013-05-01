import pymongo
import os
import datetime
from urlparse import urlparse
from collections import Counter


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
    email.insert(e.to_json())

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
    result = Counter(symptom for message in messages for symptom in message['symptoms'])
    return [(str(s), result[s]*100/sum(result.values())) for s in result]

def find_all_symptoms(sender=None):
    """
    Returns all symptoms from mongodb
    """
    email = db.email
    messages = email.find({"sender" : sender})
    result = Counter(symptom for message in messages for symptom in message['symptoms'])
    most_common = result.most_common(10)

    return [(str(s[0]), result[s[0]]*100/sum(result.values())) for s in most_common]

def find_symptoms_count(filter={}):
    """
    Returns the symptoms from mongodb as a raw count, rather than a percentage

    Finds the entry according to the sender (the person logged in),
    the start date and the end date
    """
    query = {}

    if 'sender' in filter:
        query['sender'] = filter['sender']

    if 'start_date' in filter:
        if 'date' not in query: query['date'] = {}
        query['date']['$gte'] = filter['start_date']

    if 'end_date' in filter:
        if 'date' not in query: query['date'] = {}
        filter['end_date'] += datetime.timedelta(1)
        query['date']['$lte'] = filter['end_date']

    messages = db.email.find(query)
    result = Counter(symptom for message in messages for symptom in message['symptoms'])
    return [(str(s), result[s]) for s in result]

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
    user.insert(u.to_json())

def signed_up(u):
    """
    Accepts models.User class adds a new user in mongodb as signed up
    """
    not_verified = db.not_verified
    not_verified.insert(u.to_json())

def verified(email):
    not_verified = db.not_verified
    return not_verified.find_one( { "email": email } )

def delete_verified(email):
    not_verified = db.not_verified
    db.not_verified.remove({ "email": email })


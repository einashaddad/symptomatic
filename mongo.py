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

    try:
        email.insert(e.to_json()) 
    
    except pymongo.errors.AutoReconnect:
        raise MongoInsertionError("Connection to the databas was lost. Will attempt to reconnect.")
    
    except pymongo.errors.CollectionInvalid:
        raise MongoInsertionError("Collection validation has failed.")
    
    except pymongo.errors.ConfigurationError:
        raise MongoInsertionError("Something is incorrectly configured.")
    
    except pymongo.errors.ConnectionFailure:
        raise MongoInsertionError("A connection to the database cannot be made or is lost.")

    except pymongo.errors.DuplicateKeyError:
        raise MongoInsertionError("Duplicate keys at insertion.")
    
    except pymongo.errors.InvalidBSON:
        raise MongoInsertionError("Trying to create a BSON object from invalid data.") 

    except pymongo.errors.InvalidName:
        raise MongoInsertionError("An invalid name has been used.")

    except pymongo.errors.InvalidOperation:
        raise MongoInsertionError("Client attempted to perform an invalid operation.") 

    except pymongo.errors.InvalidStringData:
        raise MongoInsertionError("Trying to encode a string containing non-UTF8 data.")
    
    except pymongo.errors.InvalidURI:
        raise MongoInsertionError("Trying to parse an invalid mongodb URI.")

    except pymongo.errors.OperationFailure:
        raise MongoInsertionError("Inserting has failed.")


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

    try:
        user.insert(u.to_json())

    except pymongo.errors.AutoReconnect:
        raise MongoInsertionError("Connection to the databas was lost. Will attempt to reconnect.")
    
    except pymongo.errors.CollectionInvalid:
        raise MongoInsertionError("Collection validation has failed.")
    
    except pymongo.errors.ConfigurationError:
        raise MongoInsertionError("Something is incorrectly configured.")
    
    except pymongo.errors.ConnectionFailure:
        raise MongoInsertionError("A connection to the database cannot be made or is lost.")

    except pymongo.errors.DuplicateKeyError:
        raise MongoInsertionError("Duplicate keys at insertion.")
    
    except pymongo.errors.InvalidBSON:
        raise MongoInsertionError("Trying to create a BSON object from invalid data.") 

    except pymongo.errors.InvalidName:
        raise MongoInsertionError("An invalid name has been used.")

    except pymongo.errors.InvalidOperation:
        raise MongoInsertionError("Client attempted to perform an invalid operation.") 

    except pymongo.errors.InvalidStringData:
        raise MongoInsertionError("Trying to encode a string containing non-UTF8 data.")
    
    except pymongo.errors.InvalidURI:
        raise MongoInsertionError("Trying to parse an invalid mongodb URI.")

    except pymongo.errors.OperationFailure:
        raise MongoInsertionError("Inserting has failed.") 


def signed_up(u):
    """
    Accepts models.User class Adds a new user in mongodb 
    """
    not_verified = db.not_verified

    try:
        not_verified.insert(u.to_json())

    except pymongo.errors.AutoReconnect:
        raise MongoInsertionError("Connection to the databas was lost. Will attempt to reconnect.")
    
    except pymongo.errors.CollectionInvalid:
        raise MongoInsertionError("Collection validation has failed.")
    
    except pymongo.errors.ConfigurationError:
        raise MongoInsertionError("Something is incorrectly configured.")
    
    except pymongo.errors.ConnectionFailure:
        raise MongoInsertionError("A connection to the database cannot be made or is lost.")

    except pymongo.errors.DuplicateKeyError:
        raise MongoInsertionError("Duplicate keys at insertion.")
    
    except pymongo.errors.InvalidBSON:
        raise MongoInsertionError("Trying to create a BSON object from invalid data.") 

    except pymongo.errors.InvalidName:
        raise MongoInsertionError("An invalid name has been used.")

    except pymongo.errors.InvalidOperation:
        raise MongoInsertionError("Client attempted to perform an invalid operation.") 

    except pymongo.errors.InvalidStringData:
        raise MongoInsertionError("Trying to encode a string containing non-UTF8 data.")
    
    except pymongo.errors.InvalidURI:
        raise MongoInsertionError("Trying to parse an invalid mongodb URI.")

    except pymongo.errors.OperationFailure:
        raise MongoInsertionError("Inserting has failed.") 

def verified(email):
    not_verified = db.not_verified

    user_found = not_verified.find_one( { "email": email } )

    if user_found:
        db.not_verified.remove({ "email": email })
        return user_found
    
    return None     



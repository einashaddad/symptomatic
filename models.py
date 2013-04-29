import re
import datetime

class User(object):
    def __init__(self, first_name, last_name, fb_email, email):
        self.first_name = first_name
        self.last_name = last_name
        self.fb_email = fb_email
        self.email = email
        self._validate()

    def _validate(self):
        if type(self.first_name) != unicode or not self.first_name:
            raise UserValidationError("Invalid First Name")
        elif type(self.last_name) != unicode or not self.last_name:
            raise UserValidationError("Invalid Last Name")

    @classmethod
    def from_json(cls, user):
        first_name=user['first_name']
        last_name=user['last_name']
        fb_email=user['fb_email']
        email=user['email']

        return cls(first_name=first_name, last_name=last_name, fb_email=fb_email, email=email)



    def to_json(self):
        return  { "first_name": self.first_name, 
                  "last_name":  self.last_name, 
                  "fb_email":   self.fb_email, 
                  "email" :     self.email, 
                }


class Email(object):
    def __init__(self, date, sender, symptoms, body_plain):
        self.date = date
        self.sender = sender
        self.body_plain=body_plain
        self.symptoms = symptoms

    def to_json(self):
        return {"date": self.date,
                "sender": self.sender, 
                "symptoms": self.symptoms, 
                "body_plain": self.body_plain,
                }

    @classmethod
    def validate(cls, date, sender, symptoms, stripped_text):
        """
        TODO: ADD DOCSTRINGS
        """
        if type(date) != datetime.datetime:
            raise EmailValidationError("date is not of type datetime")
        elif stripped_text.splitlines() != symptoms:
            raise EmailValidationError("list of symptoms not as in email sent")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", sender): 
            raise EmailValidationError("invalid email address")

        return cls(date=date, sender=sender, symptoms=symptoms,
                   body_plain=body_plain)


class EmailValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class UserValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class MongoInsertionError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


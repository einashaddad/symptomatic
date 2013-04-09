import re
import datetime

class User(object):
    def __init__(self, first_name, last_name, fb_email, email, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.fb_email = fb_email
        self.email = email
        self.birthday = birthday    

    def to_json(self):
        return  { "first_name": self.first_name, 
                  "last_name":  self.last_name, 
                  "fb_email":   self.fb_email, 
                  "email" :     self.email, 
                  "birthday" :  self.birthday,
                }

    @classmethod
    def validate(cls, first_name, last_name, fb_email, email, birthday):
        # TODO: Figure out more exceptions
        if type(first_name) != unicode or first_name == None:
            raise UserValidationError("Invalid First Name")
        elif type(last_name) != unicode or last_name == None:
            raise UserValidationError("Invalid Last Name")
        elif birthday == "":
            raise UserValidationError("Birthday field is empty")

        return cls(first_name, last_name, fb_email, email, birthday)

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
    def validate(cls, date, sender, symptoms, body_plain):
        # TODO: Figure out more exceptions
        if type(date) != datetime.datetime:
            raise EmailValidationError("date is not of type datetime")
        elif body_plain.splitlines() != symptoms:
            raise EmailValidationError("list of symptoms not as in email sent")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", sender): 
            raise EmailValidationError("invalid email address")

        return cls(date=date, sender=sender, symptoms=symptoms, body_plain=body_plain)


class EmailValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class UserValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)



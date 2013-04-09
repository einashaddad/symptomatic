#! /usr/bin/env python

import requests
import pdb
import time

"""
This sends a dummy email to the app
"""

data = {'sender': 'einas.haddad@gmail.com', 
        'recipient': 'symtomatic@symtomatic.mailgun.org',
        'subject': 'test',
        'body-plain': 'craycray\nsymptom',
        'timestamp': str(int(time.time())),     
        }

#r = requests.post('http://shrouded-tundra-4968.herokuapp.com/messages', data=data)
r = requests.post('http://localhost:58733/messages', data=data)

assert r.status_code == 200

#pdb.set_trace()
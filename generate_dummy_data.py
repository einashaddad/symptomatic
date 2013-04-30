#! /usr/bin/env python

import requests
import pdb
import time
import datetime
import random

"""
Generate dummy data for testing
"""
# how many days of symptoms to generate
days_of_data = 90

symptoms = [
  'fatigue',
  'pain',
  'fogginess/memory',
  'poor sleep',
  'depression',
  'light sensitivity',
  'abdominal pain',
  'dizzy',
  'headache',
  'joint pain',
  'lymph node tenderness',
  'sore throat'
]

date = datetime.datetime.now() - datetime.timedelta(days_of_data)

for i in range (1, days_of_data):
  symptom_count = random.randint(1, len(symptoms)/2)
  chosen_symptoms = random.sample(set(symptoms), symptom_count)

  data = {'sender': 'allie.jones@gmail.com',
          'recipient': 'symtomatic@symtomatic.mailgun.org',
          'subject': 'test',
          'stripped-text': "\n".join(chosen_symptoms),
          'timestamp': str(int(time.mktime(date.timetuple()))),
          }

  r = requests.post('http://localhost:58733/messages', data=data)

  date += datetime.timedelta(1)

  # assert r.status_code == 200

import requests
import pdb
import time

data = {'sender': 'einas@isthebest.com', 
		'recipient': 'symtomatic@symtomatic.mailgun.org',
		'subject': 'testing',
		'body-plain': 'symptom1\nsymptom2\nsymptom3\nsymptom4',
		'timestamp': str(int(time.time())),		
		}

#r = requests.post('http://shrouded-tundra-4968.herokuapp.com/messages', data=data)
r = requests.post('http://localhost:35779/messages', data=data)

assert r.status_code == 200

#pdb.set_trace()
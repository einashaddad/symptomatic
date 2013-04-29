symptomatic
==========

symptomatic is a symptoms tracker/manager for people living with a chronic illness.

Sends a daily email reminder which the user replies to with the symptoms they are experiencing. The app keeps track of the symptoms and provides an interface which the user can view stats/summary of their symtoms. 

Currently @ http://shrouded-tundra-4968.herokuapp.com/

To run on localhost:

    python route.py

The following environment variables need to be set:

* API_SECRET_KEY
* CONSUMER_KEY
* CONSUMER_SECRET
* MAILGUN_APIKEY
* MAILGUN_LOGIN
* MAILGUN_PASSWORD
* MAILGUN_USERNAME
* SECRET
    

TODO:

* Add better email parsing (detect and ignore signatures)
* Feedback page for users
* Settings page
* Graphs and analytics when looking up symptoms
* Texting capability (to prompt user to submit symptoms)
* Alternative authentication method (either OpenID or Mozilla Persona)

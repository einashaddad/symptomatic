symptomatic
==========

symptomatic is a symptoms tracker/manager for people living with a chronic illness.

Sends a daily email reminder which the user replies to with the symptoms they are experiencing. The app keeps track of the symptoms and provides an interface which the user can view stats/summary of their symtoms.  

To run on localhost:

    python route.py

To send a dummy_email with your symptoms:

    python dummy_email.py
    

TODO:
1. Add better email parsing (detect and ignore signatures)
2. Send daily email through Heroku Scheduler 
3. Twitter Bootstrap

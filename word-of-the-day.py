#!/usr/bin/env python

from TwilioCredentials import *
import requests
import datetime
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

# getting today's date & formatting
today = datetime.date.today()
datestring = today.strftime('%Y/%m/%d')

# building the url & making the request
url = "http://learning.blogs.nytimes.com/{0}/word-of-the-day-quiz".format(datestring)
site = requests.get(url)

# loading the page into BeautifulSoup
page = site.text
soup = BeautifulSoup(page, 'html.parser')

# finding the word of the day container
wod_container = soup.find("article", {"class": "category-word-of-the-day"})

# pulling out the elements we need
# TODO: test that the wod_def & wod_example to make sure they behave consistently 
wod_word = wod_container.find('h3', {"class": "wod"})
wod_def = wod_container.find_all('p', {"class": "story-body-text"}, limit=2)
wod_example = wod_container.find('blockquote')

# making the elements pretty
pretty_wod_word = wod_word.get_text().encode('utf-8')
pretty_wod_def = '\n\n'.join(i.get_text() for i in wod_def).encode('utf-8')
pretty_wod_example = wod_example.get_text().encode('utf-8')

args = (pretty_wod_word, pretty_wod_def, pretty_wod_example)

msg = '''
===========
WORD OF THE DAY
==========

{0}
-----
{1}

{2}'''.format(*args)

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body=msg,
    to= twilio_to,
    from_= twilio_from)

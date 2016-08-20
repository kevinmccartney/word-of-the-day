#!/usr/bin/env python

from TwilioCredentials import *
import requests
import datetime
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from twilio.rest import TwilioRestClient
import pprint
import textwrap

def buildURL():
    global site
 
    # getting today's date & formatting
    today = datetime.date.today()
    datestring = today.strftime('%Y/%m/%d')

    # building the url & making the request
    url = "http://learning.blogs.nytimes.com/{0}/word-of-the-day-quiz".format(datestring)
    site = requests.get(url)
   
    return site

def scrape():
    global msg_raw

    # loading the page into BeautifulSoup
    global site
    page = site.text
    soup = BeautifulSoup(page, 'html.parser')

    # finding the word of the day container
    wod_container = soup.find("article", {"class": "category-word-of-the-day"}).find("div", {"class" : "entry-content"})

    # pulling out the elements we need
    # TODO: test that the wod_def & wod_example to make sure they behave consistently 
    wod_word =  wod_container.find('h3', {"class": "wod"})
    wod_def = wod_container.find_all('p', {"class": "story-body-text"}, limit=2)[0]
    wod_example_intro = wod_container.find_all("p", {"class": "story-body-text"}, limit=2)[1]
    wod_example_text = wod_container.find('blockquote')

    msg_raw = {
        'word': wod_word, 
        'def' : wod_def, 
        'example_intro': wod_example_intro, 
        'example_text': wod_example_text
    }

    return msg_raw
    
def cleanMsg():
    global msg_raw    

    for key, value in msg_raw.iteritems():
        msg_raw[key] = value.get_text().encode('utf-8')

    args = (msg_raw["word"], msg_raw["def"], msg_raw["example_intro"], msg_raw["example_text"])
    msg = textwrap.dedent(
    '''
    ===========
    WORD OF THE DAY
    ==========

    {0}
    {1}
    -----
    {2}
    {3}
    '''.format(*args)
    )

def sendSMS():
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body=msg,
        to= twilio_to,
        from_= twilio_from)

def main():
    buildURL()
    scrape()
    cleanMsg()
    sendSMS()

main()

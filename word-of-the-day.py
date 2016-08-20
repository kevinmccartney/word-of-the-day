#!/usr/bin/env python3

import requests
import datetime
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
import json

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
    page = site.text.encode('utf-8')
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
    global msg    

    for key, value in msg_raw.items():
        msg_raw[key] = value.get_text()

    args = (msg_raw["word"], msg_raw["def"], msg_raw["example_intro"], msg_raw["example_text"])
    msg = open("message-template.txt", "r").read().format(*args)

    print(msg)

def sendSMS():
    with open('twiliocredentials.json', 'r') as j:
        credentials = json.load(j)

    client = TwilioRestClient(credentials["account_sid"], credentials["auth_token"])

    message = client.messages.create(body=msg,
        to= credentials["twilio_to"],
        from_= credentials["twilio_from"])

def main():
    buildURL()
    scrape()
    cleanMsg()
    sendSMS()

main()

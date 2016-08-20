#!/usr/bin/env python3

import requests
import datetime
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
import json
import time

class Wod:
    def __init__(self):
        self.build_url()
        self.scrape()
        self.build_msg()
        self.send_sms()

    def build_url(self):
        # getting today's date & formatting
        today = datetime.date.today()
        datestring = today.strftime('%Y/%m/%d')

        # building the url & making the request
        url = "http://learning.blogs.nytimes.com/{0}/word-of-the-day-quiz".format(datestring)
        
        try:
            self.site = requests.get(url)
        except (HTTPError, Timeout):
            time.sleep(1800)
            self.site = requests.get(url)

        return self.site

    def scrape(self):
        # loading the page into BeautifulSoup
        page = self.site.text.encode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')

        # finding the word of the day container
        wod_container = soup.find("article", {"class": "category-word-of-the-day"}).find("div", {"class" : "entry-content"})

        if wod_container:
            # pulling out the elements we need
            # TODO: test that the wod_def & wod_example to make sure they behave consistently 
            try:
                wod_def = wod_container.find_all('p', {"class": "story-body-text"}, limit=2)[0]
                wod_example_intro = wod_container.find_all("p", {"class": "story-body-text"}, limit=2)[1]
            except IndexError:
                raise SystemExit
        
            wod_word =  wod_container.find('h3', {"class": "wod"})
            wod_example_text = wod_container.find('blockquote')

            if wod_word and wod_example_text:
                pass
            else:
                raise SystemExit
        else: 
            raise SystemExit

        self.msg_raw = {
            'word': wod_word, 
            'def' : wod_def, 
            'example_intro': wod_example_intro, 
            'example_text': wod_example_text
        }

        return self.msg_raw
    
    def build_msg(self):
        for key, value in self.msg_raw.items():
            self.msg_raw[key] = value.get_text()

        args = (self.msg_raw["word"], self.msg_raw["def"], self.msg_raw["example_intro"], self.msg_raw["example_text"])
        self.msg = open("message-template.txt", "r").read().format(*args)

        return self.msg

    def send_sms(self):
        with open('twiliocredentials.json', 'r') as j:
            credentials = json.load(j)

        client = TwilioRestClient(credentials["account_sid"], credentials["auth_token"])

        message = client.messages.create(body=self.msg,
            to= credentials["twilio_to"],
            from_= credentials["twilio_from"])

word_of_the_day = Wod()

word_of_the_day

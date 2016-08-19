#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

site = requests.get("http://learning.blogs.nytimes.com/2016/08/19/word-of-the-day-quiz-gazette/")
page = site.text

soup = BeautifulSoup(page, 'html.parser')

wod_container = soup.find("article", {"class": "category-word-of-the-day"})

wod_word = wod_container.find('h3', {"class": "wod"})
wod_def = wod_container.find_all('p', {"class": "story-body-text"}, limit=2)
wod_example = wod_container.find('blockquote')

pretty_wod_word = wod_word.get_text()
pretty_wod_def = '\n\n'.join(i.get_text() for i in wod_def)
pretty_wod_example = wod_example.get_text()

print("""==========
WORD OF THE DAY
==========
""")

print(pretty_wod_word)
print('-----')
print(pretty_wod_def)
print('\n')
print(pretty_wod_example)

# Word of the day
This is a very simple Python 3 script to grab the New York Times word of the day & shoot it out to your phone using Twilio's API. You can run it ad-hoc, but you should probably set it up as a Cron job.

## Get Started
+ `pip3 install -r requirements.txt`
+ Replace the values in `twiliocredentials.json` with the correct values
+ `chmod +x word-of-the-day.py`
+ Run the script with `./word-of-the-day.py` or add `0 7 * * * /path/to/word-of-the-day.py` to your crontab

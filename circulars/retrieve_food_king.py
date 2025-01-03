#!/usr/bin/env python

import json
import datetime, requests, re

################################################################################

store = "81"
file_location = "./pdfs/"

################################################################################

# Usage: This should be put into a weekly cron job, probably on Wed. Script
# doesn't do any error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of the cookes in dev tools. 
# Probably unnecessary, I can't imagine they're running more than the one flyer
# in any given week. Can change it (above) if you want. Adjust the file_location
# (above) to any relative or absolute path.

# Storage: These circular pdfs seem to weigh in at 4 meg each. Prepare 20m/month
# (240 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

wednesday = datetime.date.today() + datetime.timedelta(days = -datetime.date.today().weekday() + 2)

cookies = {'3233_consumer_credentials': 'q3vTYMJgdxp7w4zBr5Yo',
           'ahoy_visitor': '8b6b14ec-4e83-42e9-a566-127475179bfe',
           'ahoy_visit': 'd4869ae6-eaae-4aa5-a189-7934cfe2c0b9',
           '3233_circular_forma': 'newsprint', 
           '3233_store_number': store, 
           'mobileapp': '1' }

r = requests.get(f"https://www.foodkingcostplus.com/circulars/Page/1/Base/1/{wednesday.strftime('%y%m%d')}_LW_KING/",
                 cookies=cookies)

regex = re.compile("view_pdf_ad\('(https.+?pdf)'\)")
url = re.search(regex, r.text).group(1)
pdf = f"{file_location}Food Kind Circular - {wednesday.strftime('%Y-%m-%d')}.pdf"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(pdf, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

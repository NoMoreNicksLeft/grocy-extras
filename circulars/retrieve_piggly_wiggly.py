#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '4600'            # North Carolina.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. Visit the page at 
# https://www.pigglywigglystores.com/my-store/store-locator and open dev tools. 
# Then click on the selected store from the list. In the network tab,
# approximately 20 files down will be a call to the 'stores' file (type: json). 
# Click on it, check out the response, and the id property of items[0] should be
# a 4 digit number. Each circular pdf seems to be marked with that stores 
# address and quite possibly each (or at least some are unique). Also adjust the
# file_location (above) to any relative or absolute path. 

# Storage: These circular pdfs seem to weigh in at 6+ megs each. Prepare 
# 30m/month (400 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

r = requests.get(f"https://api.freshop.ncrcloud.com/1/circulars?app_key=piggly_wiggly_nc&store_id={store}",
                 headers=headers)

for c in r.json().get('items'):
    url = c.get('pdf_url')
    date = c.get('start_date')[:10]
    pdf = f"{file_location}Piggly Wiggly Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
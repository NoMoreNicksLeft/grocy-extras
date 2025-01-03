#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '177'             # Texas.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 2+ megs each. Prepare 
# 12m/month (150 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get(f"https://dam.flippenterprise.net/flyerkit/publications/albertsons?locale=en&access_token=bfe2071d14d1448296a13b19311ce041&show_storefronts=true&postal_code=83713&store_code={store}")

# With Flipp, sometimes there's a list of more than one flyer (current and next), 
# so let's get all of them unless already gotten.

filtered = [j for j in r.json() if j.get('name').startswith("Weekly Ad")]

for c in filtered:
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    pdf = f"{file_location}Albertsons Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '6023'            # Pennsylvania.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 25+ megs each. Prepare 
# 100m/month (1.2 gigs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get(f"https://flipp-api.giantfoodstores.com/flyerkit/v4.0/publications/giantfoodstores?locale=en-US&access_token=9618f9bed100f3bac0e6ae38357aad28&store_code={store}")

# With Flipp, sometimes there's a list of more than one flyer (current and next), 
# so let's get all of them unless already gotten.

filtered = [j for j in r.json() if j.get('name') == 'Weekly Circular']

for c in filtered:
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    pdf = f"{file_location}Giant Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
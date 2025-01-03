#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '2452'            # Texas.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a semimonthly cron job. Script doesn't do any 
# error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 3+ megs each. Prepare 
# 7m/month (90 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get(f"https://dam.flippenterprise.net/flyerkit/publications/ffdollartree2?locale=en&access_token=a913e06749cf36408dad121142280774&show_storefronts=true&store_code={store}")

# With Flipp, sometimes there's a list of more than one flyer (current and next), 
# so let's get all of them unless already gotten.

filtered = [j for j in r.json() if j.get('name') == 'Flyer']

for c in filtered:
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    pdf = f"{file_location}Dollar Tree Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
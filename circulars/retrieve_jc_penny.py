#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '0611'            # Texas.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job. Script doesn't do any error 
# handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in anywhere from 2 megs on up to 
# 20ish. They become available on an irregular schedule. Difficult to estimate 
# how much storage will be needed on a monthly or yearly basis.

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get(f"https://dam.flippenterprise.net/flyerkit/publications/jcpenney?locale=en&access_token=935d8402d3b1f0772a3b071880f35012&show_storefronts=true&postal_code=79414&store_code={store}")

for c in r.json():
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    title = c.get('external_display_name')
    pdf = f"{file_location}JC Penny Circular - {date} - {title}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
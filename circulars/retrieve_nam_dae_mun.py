#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '2130'            # North Carolina.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. Open 
# https://api.freshop.ncrcloud.com/1/stores?app_key=nam_dae_mun in Firefox and 
# the json object returned will have an items array with about a dozen objects. 
# Pick the id of the appropriate store and change the number (4 digits) above. 
# The name property is conveniently below id for easy identification. Also 
# adjust the file_location (above) to any relative or absolute path. 

# Storage: These circular pdfs seem to weigh in at 18+ megs each. Prepare 
# 80m/month (1 gig per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

r = requests.get(f"https://api.freshop.ncrcloud.com/1/circulars?app_key=nam_dae_mun&store_id={store}",
                 headers=headers)

for c in r.json().get('items'):
    url = c.get('pdf_url')
    date = c.get('start_date')[:10]
    pdf = f"{file_location}Nam Dae Mun Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
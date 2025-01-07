#!/usr/bin/env python

from pathlib import Path
import datetime, requests

################################################################################

store = '607'             # New Jersey.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script doesn't require a store code. Probably needs one, I can't
# tell if circulars vary by region. If we get that far, the following link
# provides all store codes.
# https://app.redpepper.digital/client/4573/catalogue/geo_location/json
# Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 50+ meg each. Prepare 
# 200m/month (2.5 gigs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

sunday = datetime.date.today() + datetime.timedelta(days = -datetime.date.today().weekday() + 6)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

r = requests.get(f"https://app.redpepper.digital/getUsDomainClientid/week-of-{sunday.strftime('%m_%d')}-z1-r1/json?_format=json", headers=headers)

url = r.json().get('field_catalogue_pdf_s3')
pdf = f"{file_location}ShopRite Circular - {sunday.strftime('%Y-%m-%d')}.pdf"

if not Path(pdf).is_file():
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(pdf, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
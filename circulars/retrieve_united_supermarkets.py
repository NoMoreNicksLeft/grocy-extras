#!/usr/bin/env python

from pathlib import Path
import datetime, requests

################################################################################

file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, prior to Sunday. Script 
# doesn't do any error handling.

# Storage: These circular pdfs seem to weigh in at 65+ megs each. Prepare 
# 280m/month (3.5 gigs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

wednesday = datetime.date.today() + datetime.timedelta(days = -datetime.date.today().weekday() + 9)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

r = requests.get(f"https://digitaledition.net/getUsDomainClientid/{wednesday.strftime('%m%d%Y')}_wtx_lc/json?_format=json",
                 headers=headers)

url = r.json().get('field_catalogue_pdf_s3')
pdf = f"{file_location}United Supermarkets Circular - {wednesday.strftime('%Y-%m-%d')}.pdf"

if not Path(pdf).is_file():
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(pdf, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
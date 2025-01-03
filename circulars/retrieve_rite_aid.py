#!/usr/bin/env python

from pathlib import Path
import requests

################################################################################

store = '362'             # Baltimore.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Usage: This should be put into a weekly cron job, probably on Sun. Script
# doesn't do any error handling.

# Notes: This script requires a store code. Same as on the 'store selector' page
# (without leading zeros) at https://www.riteaid.com/locations/search.html . Can
# change it (above) if you want. Adjust the file_location (above) to any 
# relative or absolute path.

# Storage: These circular pdfs seem to weigh in at 4 meg each. Prepare 20m/month
# (240 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get(f"https://dam.flippenterprise.net/flyerkit/publications/riteaid?locale=en&access_token=0ebf9efc5d4c2b8bed77ca26a01261f4&show_storefronts=true&store_code={store}")

# With Flipp, sometimes there's a list of more than one flyer (current and next), 
# so let's get all of them unless already gotten.

filtered = [j for j in r.json() if j.get('name') == 'Weekly Ad']

for c in filtered:
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    pdf = f"{file_location}Rite Aid Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
#!/usr/bin/env python

from pathlib import Path
from PIL import Image
import datetime, requests, tempfile

################################################################################

store = '2190'            # Texas.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Special: Target does not seem to provide pdf downloads or even hidden pdf 
# masters of its circulars. However the web app does provide large, medium res 
# images of each page and these have been stitched together into something not 
# much different than what they have internally at corporate.

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 12+ meg each. Prepare 
# 60m/month (750 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

r1 = requests.get(f"https://api.target.com/weekly_ads/v1/store_promotions?key=9ba599525edd204c560a2182ae1cbfaa3eeddca5&store_id={store}")

filtered = [j for j in r1.json() if j.get('title') == 'Weekly Ad']

for c in filtered:
    id = c.get('promotion_id')
    date = datetime.datetime.strptime(c.get('sale_start_date')[:10], '%m/%d/%Y').strftime('%Y-%m-%d')
    pdf = f"{file_location}Target Circular - {date}.pdf"

    if not Path(pdf).is_file():
        r2 = requests.get(f"https://api.target.com/weekly_ads/v1/promotions/{id}?key=9ba599525edd204c560a2182ae1cbfaa3eeddca5")
        image_files = []
        for p in r2.json().get('pages'):
            page_url = f"{p.get('image_url')[:-3]}2000"
            with requests.get(page_url, stream=True) as r:
                r.raise_for_status()
                with open(f"{tempfile.gettempdir()}{p.get('page_index')}.jpg", 'wb') as f:
                    image_files.append(f"{p.get('page_index')}.jpg")
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        images = [
            Image.open(tempfile.gettempdir() + f)
            for f in image_files
        ]
    
        images[0].save(
            pdf, "PDF" ,resolution=150.0, save_all=True, append_images=images[1:]
        )
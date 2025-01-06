#!/usr/bin/env python

from pathlib import Path
from PIL import Image
import requests, tempfile

################################################################################

store = '517240'          # Texas.
file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

# Special: Sprouts does not seem to provide pdf downloads or even hidden pdf 
# masters of its circulars. However the web app does provide large, medium res 
# images of each page and these have been stitched together into something not 
# much different than what they have internally at corporate.

# Usage: This should be put into a weekly cron job, probably on Fri. Script
# doesn't do any error handling.

# Notes: This script requires a store code. No good way of getting the correct
# code for your location, short of digging it out of dev tools. Can change it 
# (above) if you want. Adjust the file_location (above) to any relative or 
# absolute path.

# Storage: These circular pdfs seem to weigh in at 5+ meg each. Prepare 
# 25m/month (350 megs per year) for archiving.

################################################################################
#################################### main() ####################################
################################################################################

cookies = {'__Host-instacart_sid': 'v2.3833943f368100.YvHJF-yYC_2GobjKt6Z6jMKo9GJhjRua9dyAU6m1Joo'}

r = requests.get(f"https://shop.sprouts.com/graphql?operationName=Flyers&variables=%7B%22shopId%22%3A%22{store}%22%2C%22active%22%3Atrue%2C%22tag%22%3Anull%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2258654d81e59571aef2d895f18fa1b277f9e84bf2a8bce18491a281db40064d67%22%7D%7D",
                 cookies=cookies)

filtered = [j for j in r.json().get('data').get('flyers') if j.get('name') == 'Weekly Ad']

for c in filtered:
    date = c.get('flyerRetailerLocation').get('startsAt')[:10]
    pdf = f"{file_location}Sprouts Circular - {date}.pdf"
    if not Path(pdf).is_file():
        image_files = []
        for p in c.get('flyerPages'):
            with requests.get(p.get('image'), stream=True) as r:
                r.raise_for_status()
                with open(f"{tempfile.gettempdir()}{p.get('pageNumber')}.jpg", 'wb') as f:
                    image_files.append(f"{p.get('pageNumber')}.jpg")
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        images = [
            Image.open(tempfile.gettempdir() + f)
            for f in image_files
        ]

        images[0].save(
            pdf, "PDF" ,resolution=150.0, save_all=True, append_images=images[1:]
        )
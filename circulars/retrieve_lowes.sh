#!/bin/bash

# BROKEN BROKEN BROKEN. The final curl call fails with a 403, and the web page doesn't seem to have any exposed
# functionality to allow pdf download. This one may just be locked.

# Usage: This should be put into a weekly cron job, probably on a Friday or a Saturyday. Script doesn't do any error 
# handling.

# Notes: This script requires a number (4 digit?) store code, and I can't find a good way of getting one short of
# digging through homedepot.com markup or even the deluge of dev tools network tab entries. 
# Finally, there does not seem to be a realistic way to get past issues. One could dig through the Wayback machine, but 
# they will likely encounter the same flipp.com json url as below, which when retrieved will just be this week's. If 
# Wayback has the content of the url though, then the pdf links within could point to past issues. Those are low-value,
# for only the most pathetic sort of data hoarders (like myself?), maybe not worth the effort.

# Storage: These circular pdfs seem to weigh in at 2+ megs each. Prepare 10m/month (120 megs per year) for archiving.

STORE=0271
FILE_LOCATION=./pdfs/

CHROME_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
PAGE='https://dam.flippenterprise.net/flyerkit/publications/lowesusa?locale=en&access_token=0221fb997ed13ee0a32ef4d5d703852a&show_storefronts=true&store_code='
CURL=`which curl`
JQ=`which jq`

QUERY1=".[] | select(.external_display_name==\"Weekly Ad\") | .pdf_url"
QUERY2=".[] | select(.external_display_name==\"Weekly Ad\") | .valid_from | .[0:10]"

JSON=`$CURL -s $PAGE$STORE`
PDF=`echo $JSON | $JQ -r "$QUERY1"`
DATE=`echo $JSON | $JQ -r "$QUERY2"`

$CURL -s -e "https://www.lowes.com/weekly-ad" -A "$CHROME_UA" $PDF > "${FILE_LOCATION}Lowe's Circular - $DATE.pdf"
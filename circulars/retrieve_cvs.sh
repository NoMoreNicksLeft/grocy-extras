#!/bin/bash

# Usage: This should be put into a weekly cron job, probably on a Friday or a Saturyday. Script doesn't do any error 
# handling.

# Notes: This script requires a number (5 digit?) store code, and I can't find a good way of getting one short of
# digging through cvs.com markup or even the deluge of dev tools network tab entries. Furthermore, there are always two
# circulars available, the current week's and next week's. For simplicity's sake, this will always get next week's. 
# Finally, there does not seem to be a realistic way to get past issues. One could dig through the Wayback machine, but 
# they will likely encounter the same flipp.com json url as below, which when retrieved will just be this week's. If 
# Wayback has the content of the url though, then the pdf links within could point to past issues. Those are low-value,
# for only the most pathetic sort of data hoarders (like myself?), maybe not worth the effort.

# Storage: These circular pdfs seem to weigh in at 30+ megs each. Prepare 150m/month (2 gigs per year) for archiving.

STORE=10521
FILE_LOCATION=./pdfs/

PAGE='https://api.flipp.com/flyerkit/v4.0/publications/cvspharmacy?access_token=d005d9bbce4a77a9f3908b83e38aae19&locale=en-US&store_code='
CURL=`which curl`
JQ=`which jq`

DATE=`date -v+Sunday +"%Y-%m-%d"`

QUERY1=".[] | select(.valid_from | startswith(\"$DATE\")) | .pdf_url"

JSON=`$CURL -s $PAGE$STORE`
PDF=`echo $JSON | $JQ -r "$QUERY1"`

$CURL -s $PDF > "${FILE_LOCATION}CVS Pharmacy Circular - $DATE.pdf"
#!/bin/bash

# Usage: This should be put into a weekly cron job, probably on a Friday or a Saturyday. Script doesn't do any error 
# handling.

# Notes: This script requires a number (4 digit?) store code, and I can't find a good way of getting one short of
# digging through dollartree.com markup or even the deluge of dev tools network tab entries. 
# Finally, there does not seem to be a realistic way to get past issues. One could dig through the Wayback machine, but 
# they will likely encounter the same flipp.com json url as below, which when retrieved will just be this week's. If 
# Wayback has the content of the url though, then the pdf links within could point to past issues. Those are low-value,
# for only the most pathetic sort of data hoarders (like myself?), maybe not worth the effort.

# Storage: These circular pdfs seem to weigh in at 3+ megs each. Prepare 7m/month (90 megs per year) for archiving.

STORE=2452
FILE_LOCATION=./pdfs/

PAGE='https://dam.flippenterprise.net/flyerkit/publications/ffdollartree2?locale=en&access_token=a913e06749cf36408dad121142280774&show_storefronts=true&store_code='
CURL=`which curl`
JQ=`which jq`

QUERY1=".[0] | .pdf_url"
QUERY2=".[0] | .valid_from | .[0:10]"

JSON=`$CURL -s $PAGE$STORE`
PDF=`echo $JSON | $JQ -r "$QUERY1"`
DATE=`echo $JSON | $JQ -r "$QUERY2"`

$CURL -s $PDF > "${FILE_LOCATION}Dollar Tree Circular - $DATE.pdf"
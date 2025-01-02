#!/bin/bash

# Usage: This should be put into a weekly cron job, probably on a Friday or a Saturyday. Script doesn't do any error 
# handling. Visit https://www.foodkingcostplus.com/circulars/select_a_store/ and click on a store. The store id should
# be added to the end of the url in the address bar after the page loads. This is the store id, change the shell
# variable below.

# Notes: This script requires a number (5 digit?) store code, and I can't find a good way of getting one short of
# digging through cvs.com markup or even the deluge of dev tools network tab entries. Furthermore, there are always two
# circulars available, the current week's and next week's. For simplicity's sake, this will always get next week's. 
# Finally, there does not seem to be a realistic way to get past issues. One could dig through the Wayback machine, but 
# they will likely encounter the same flipp.com json url as below, which when retrieved will just be this week's. If 
# Wayback has the content of the url though, then the pdf links within could point to past issues. Those are low-value,
# for only the most pathetic sort of data hoarders (like myself?), maybe not worth the effort.

# Storage: These circular pdfs seem to weigh in at 30+ megs each. Prepare 150m/month (2 gigs per year) for archiving.

STORE=81
FILE_LOCATION=./pdfs/

#https://www.foodkingcostplus.com/circulars/Page/1/Base/1/250101_LW_KING/?store=4708

# https://www.foodkingcostplus.com/circulars

if date --version >/dev/null 2>&1 ; then
    DATE=`date -d "Wednesday" +"%y%m%d"`
else
    DATE=`date -v Wednesday +"%y%m%d"`
fi

PAGE="https://www.foodkingcostplus.com/circulars/Page/1/Base/1/${DATE}_LW_KING/"
CURL=`which curl`
JQ=`which jq`
COOKIE="3233_consumer_credentials=q3vTYMJgdxp7w4zBr5Yo; ahoy_visitor=4e101db2-e901-4e02-8479-06402d98349c; ahoy_visit=359737b8-bff7-4416-a80e-b7822308c0ff; 3233_circular_format=newsprint; 3233_store_number=$STORE; mobileapp=1"

WEB=`$CURL -s --cookie "$COOKIE" --location "$PAGE"`
# echo $WEB | grep "View PDF"
# echo "$WEB" | sed -e '/.+onclick="view_pdf_ad..https.+\.pdf..+/'
echo "$WEB" | sed -nr 's/span\(......\)/\1/p' 
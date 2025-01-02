#!/bin/bash

# Usage: This should be put into a weekly cron job, prior to Wednesday (after will get next week's). Script doesn't do
# any error handling.

# Notes:

# Storage: These circular pdfs seem to weigh in at 65+ megs each. Prepare 280m/month (3.5 gigs per year) for archiving.

FILE_LOCATION=./pdfs/

if date --version >/dev/null 2>&1 ; then
    NEXTWED=`date -d "next Wednesday" +"%m%d%Y"`
    DATE=`date -d "next Wednesday" +"%Y-%m-%d"`
else
    NEXTWED=`date -v+Wednesday +"%m%d%Y"`
    DATE=`date -v+Wednesday +"%Y-%m-%d"`
fi

CHROME_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
PAGE="https://digitaledition.net/getUsDomainClientid/${NEXTWED}_wtx_lc/json?_format=json"
CURL=`which curl`
JQ=`which jq`

JSON=`$CURL -s -A "$CHROME_UA" $PAGE`
QUERY1=".field_catalogue_pdf_s3"
PDF=`echo $JSON | $JQ -r "$QUERY1"`

$CURL -s $PDF > "${FILE_LOCATION}United Supermarkets Circular - $DATE.pdf"

# date -v+Wednesday 

#!/usr/bin/env python

from pathlib import Path
import us_state_abbreviations as states
import sys, argparse, requests, re

################################################################################

file_location = './pdfs/' # Create (or change) directory or script will fail.

################################################################################

################################################################################
################################ Parse arguments ###############################
################################################################################

parser = argparse.ArgumentParser(prog = 'retrieve_xxx.py',
                                 description = 'Scripts for automatically downloading weekly ads, flyers, circulars.',
                                 epilog = 'Just run without arguments or switches for typical use.',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=27))
parser.add_argument('--list-store-ids', help='lists store ids directly as provided by site', action='store_true', dest='list_stores')
parser.add_argument('--list-store-states', help='lists store locations (states) directly as provided by site', action='store_true', dest='list_states')
parser.add_argument('--list-store-ids-by-zip', help='lists store ids directly as provided by site', action='store_true', dest='list_stores')
parser.add_argument('--list-store-ids-by-state', help='lists store ids directly as provided by site', action='store', dest='list_stores_by_state', type=lambda s: [str(item) for item in s.split(',')])
parser.add_argument('--store', help='store id, uniquely identifies retail location for specific weekly ad', dest='store', nargs='?', const='002', type=str, default='002')
parser.add_argument('--format-string', help='format string for file path and name', dest='format_string')
args = parser.parse_args()

################################################################################
########################## --list-store-states output ##########################
################################################################################

if args.list_states:
    print("""
The following states have CTown locations: ct, ma, nj, ny, pa
          
Use the --list-store-ids-by-state switch with one or more (comma-delimited, no
spaces) states abbreviations.

    ./retrieve_ctown.py --list-store-ids-by-state ct,nj
""")
    sys.exit()

################################################################################
########################### --list-store-ids output ############################
################################################################################

if args.list_stores:
    new_offset = 0
    r = requests.get('https://liveapi.yext.com/v2/accounts/me/entities/geosearch', 
                     params={'radius': 1000,
                             'location': '10010',
                             'limit': 50,
                             'api_key': '62850d78675a712e91b03d1d5868d470',
                             'v': '20181201', # Supposed to be a date. Hard-coded on the website, we'll do the same.
                             'entityTypes': 'location',
                             'offset': new_offset})
    
    total_remaining = int(r.json().get('response').get('count')) - 50

    entities = r.json().get('response').get('entities')

    while total_remaining > 0:
        new_offset += 50
        r = requests.get('https://liveapi.yext.com/v2/accounts/me/entities/geosearch', 
                         params={'radius': 1000,
                                 'location': '10010',
                                 'limit': 50,
                                 'api_key': '62850d78675a712e91b03d1d5868d470',
                                 'v': '20181201',
                                 'entityTypes': 'location',
                                 'offset': new_offset})
        total_remaining -= 50
        entities += r.json().get('response').get('entities')

    entities.sort(key=lambda e: (e['address']['region'], e['address']['city']))
    filtered = [j for j in entities if 'CTown' in j.get('name') and 'CLOSED' not in j.get('name')]

    prev = ''
    for e in filtered:
        if e.get('meta').get('id') == '17176938076': e['meta']['id'] = 'U41_415' # This one is fucked up in their data.
        if e.get('meta').get('id') == 'U41-030': e['meta']['id'] = 'PU41_030' # This one was double-screwed up.
        e['meta']['id'] = e['meta']['id'].replace('-', '_', 1) # Some of these use dashes, supposed to be underscores.
        a = e.get('address')
        if prev != a.get('region'): print(states.abbreviation_to_name[a.get('region')]+':')
        print(f"    {e.get('meta').get('id'):<12}  =  {a.get('city').title()+', '+a.get('region'):<19}   {a.get('line1')}")
        prev = a.get('region')

    sys.exit()

################################################################################
#################################### main() ####################################
################################################################################

r = requests.get('https://dam.flippenterprise.net/flyerkit/publications/ctown',
                 params={'store_code': args.store,
                         'show_storefronts': 'true',
                         'locale': 'en',
                         'access_token': '30bc560130542d12ce1817299c5a19bc'})

filtered = [j for j in r.json() if j.get('name') == 'Weekly Ad']

for c in filtered:
    url = c.get('pdf_url')
    date = c.get('valid_from')[:10]
    pdf = f"{file_location}CTown Circular - {date}.pdf"

    if not Path(pdf).is_file():
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

# 06451 
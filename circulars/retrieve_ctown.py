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
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=32))
parser.add_argument('--list-store-ids', 
                    help='lists store ids directly as provided by site', 
                    action='store_true', dest='list_stores')
parser.add_argument('--list-store-states', 
                    help='lists store locations (states) directly as provided by site', 
                    action='store_true', dest='list_states')
parser.add_argument('--list-store-ids-by-zip', 
                    help='lists store ids directly as provided by site', 
                    action='store_true', dest='list_stores_by_zip')
parser.add_argument('--list-store-ids-by-state', 
                    help='lists store ids directly as provided by site', 
                    action='store', dest='list_stores_by_state', 
                    type=lambda s: [str(item) for item in s.upper().split(',')])
parser.add_argument('--store', 
                    help='store id, uniquely identifies retail location for specific weekly ad', 
                    dest='store', nargs='?', const='PU41_338', 
                    type=str, default='PU41_338')
parser.add_argument('--format-string', 
                    help='format string for file path and name', 
                    dest='format_string', 
                    type=str, default='{home}/{brand} Circular - {date}.pdf')
args = parser.parse_args()

################################################################################
#################################### main() ####################################
################################################################################

def main():
    if args.list_states:
        list_states()
        sys.exit()
    elif args.list_stores:
        list_stores()
        sys.exit()
    elif args.list_stores_by_state:
        list_stores(by_state=True)
        sys.exit()
    elif args.list_stores_by_zip:
        list_stores(by_zip=True)
        sys.exit()

    r = requests.get('https://dam.flippenterprise.net/flyerkit/publications/ctown',
                    params={'store_code': args.store,
                            'show_storefronts': 'true',
                            'locale': 'en',
                            'access_token': '30bc560130542d12ce1817299c5a19bc'})

    filtered = [j for j in r.json() if j.get('name') == 'Weekly Ad']

    for c in filtered:

################################################################################
        name = c.get('name')
        brand = 'CTown'
        store = args.store
        home = str(Path.home())
        date = c.get('valid_from')[:10]
################################################################################

        try:
            pdf = eval('f"'+args.format_string+'"')
        except NameError:
            print('ERROR: unsupported format_string variable.')

        url = c.get('pdf_url')

        if not Path(pdf).is_file():
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(pdf, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

################################################################################
################################## Functions ###################################
################################################################################

def list_states():
    print("""
The following states have CTown locations: ct, ma, nj, ny, pa
          
Use the --list-store-ids-by-state switch with one or more (comma-delimited, no
spaces) states abbreviations.

    ./retrieve_ctown.py --list-store-ids-by-state ct,nj
""")

def list_stores(by_state=False, by_zip=False):
    new_offset = 0
    radius = 1000
    zip = '10010'
    if by_zip:
        radius = 25
        zip = args.list_stores_by_zip

    r = requests.get('https://liveapi.yext.com/v2/accounts/me/entities/geosearch', 
                     params={'radius': radius,
                             'location': zip,
                             'limit': 50,
                             'api_key': '62850d78675a712e91b03d1d5868d470',
                             # Supposed to be a date. Hard-coded on the website,
                             # we'll do the same.
                             'v': '20181201', 
                             'entityTypes': 'location',
                             'offset': new_offset})
    
    total_remaining = int(r.json().get('response').get('count')) - 50

    entities = r.json().get('response').get('entities')

    while total_remaining > 0:
        new_offset += 50
        r = requests.get('https://liveapi.yext.com/v2/accounts/me/entities/geosearch', 
                         params={'radius': radius,
                                 'location': zip,
                                 'limit': 50,
                                 'api_key': '62850d78675a712e91b03d1d5868d470',
                                 'v': '20181201',
                                 'entityTypes': 'location',
                                 'offset': new_offset})
        total_remaining -= 50
        entities += r.json().get('response').get('entities')

    entities.sort(key=lambda e: (e['address']['region'], e['address']['city']))

    if by_state:
        filtered = [j for j in entities 
                    if 'CTown' in j.get('name') 
                    and 'CLOSED' not in j.get('name') 
                    and j.get('address').get('region') in args.list_stores_by_state ]
    # if by_zip:
    #     filtered = [j for j in entities 
    #                 if 'CTown' in j.get('name') 
    #                 and 'CLOSED' not in j.get('name') 
    #                 and j.get('address').get('postCode') == args.list_stores_by_zip ]
    else:
        filtered = [j for j in entities if 'CTown' in j.get('name') and 'CLOSED' not in j.get('name')]

    prev = ''
    for e in filtered:
        # This one is fucked up in their data.
        if e.get('meta').get('id') == '17176938076': e['meta']['id'] = 'U41_415' 
        # This one was double-screwed up.
        if e.get('meta').get('id') == 'U41-030': e['meta']['id'] = 'PU41_030'
        # Some of these use dashes, supposed to be underscores.
        e['meta']['id'] = e['meta']['id'].replace('-', '_', 1) 
        a = e.get('address')
        if prev != a.get('region'): 
            print(states.abbreviation_to_name[a.get('region')]+':')
        print(f"    {e.get('meta').get('id'):<12}  =  {a.get('city').title()+', '+a.get('region'):<19}   {a.get('line1')}")
        prev = a.get('region')

################################################################################
################################################################################
            
main()
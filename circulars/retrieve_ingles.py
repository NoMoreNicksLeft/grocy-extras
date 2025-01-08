#!/usr/bin/env python

from pathlib import Path
from PIL import Image
import sys, argparse, requests, re, tempfile

requests.packages.urllib3.disable_warnings()

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
parser.add_argument('--list-store-ids', help = 'lists available store ids directly as provided by site', action = 'store_true', dest = 'list_stores')
parser.add_argument('--store', help = 'store id, uniquely identifies retail location for specific weekly ad', dest = 'store', nargs='?', const='002', type=str, default='002')
parser.add_argument('--format-string', help = 'format string for file path and name', dest = 'format_string')
args = parser.parse_args()

################################################################################
########################### --list-store-ids output ############################
################################################################################

session = requests.Session()
magic = 'WE52VVkyKzZ0ZitGVE9PSWp6UmxENHAxYjZxRWp4QlQ1Q1BCUkhSSQ=='

if args.list_stores:
    r1 = session.get('https://ingles-markets.com/', verify=False)
    states = re.search(r'<select name="state".+?>(.*?)<.select>', r1.text, re.S).group(1)
    
    for s, state in re.findall(r'<option value="([A-Z][A-Z])">(.+?)<', states):
        print(f"{state}:")
        r2 = session.get('https://www.ingles-markets.com/js/modal/getcity.php', params={'t': magic, 'q': s}, verify=False)
        for city in re.findall(r"<OPTION VALUE='(.+?)'", r2.text, re.I):
            r3 = session.get('https://www.ingles-markets.com/js/modal/getstore.php', params={'t': magic, 'q': city}, verify=False)
            for storeid in re.findall(r"<option value='(.+?)'>", r3.text):
                print(f"    {storeid[-3:]}  =  {city+', '+s:<23}    {storeid[:-5]}")
    sys.exit()

################################################################################
#################################### main() ####################################
################################################################################

pdf = 'test.pdf'

if not Path(pdf).is_file():
    image_files = []
    r1 = session.get('https://flyer.inglesads.com/noncard/ThisWeek/ShopList.jsp', params={'VMODE': 'FLYER', 'StoreID': args.store})
    for p in range(1,8):
        
        page_url = f"{p.get('image_url')[:-3]}2000"
        with requests.get(page_url, stream=True) as r:
            r.raise_for_status()
            with open(f"{tempfile.gettempdir()}{p.get('page_index')}.jpg", 'wb') as f:
                image_files.append(f"{p.get('page_index')}.jpg")
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

# https://flyer.inglesads.com/noncard/ThisWeek/ShopList.jsp?VMODE=FLYER&StoreID=601

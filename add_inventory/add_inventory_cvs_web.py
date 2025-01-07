#!/usr/bin/env python

from pathlib import Path
import sys, shutil
import json, argparse, base64, pwinput, re, jose
import requests, http.client
# import add_product_cvs

http.client._MAXHEADERS = 300

################################################################################
################################################################################

grocy_headers = { 'GROCY-API-KEY' : 'empty', 
                  'accept': 'application/json',
                  'Content-Type': 'application/json' }

session = requests.Session()
session.cookies.clear()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
session.headers = headers

################################################################################
################################ Parse arguments ###############################
################################################################################

parser = argparse.ArgumentParser(prog = 'add_inventory_xxx.py',
                                 description = 'Scripts for automatically adding purchases to inventory',
                                 epilog = 'Just run without arguments or switches for typical use.',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=27))
parser.add_argument('--dry-run', help = 'tests functionality without making changes to grocy', action = 'store_true', dest = 'dry_run')
args = parser.parse_args()

################################################################################
##################################### Main #####################################
################################################################################

def main():
    load_config()

    if not config.get('c') or not config.get('c').get('cvs'):
        prompt1 = """
This script requires your CVS login credentials. These will be stored in the 
config file. What is your email or mobile phone number?
"""
        login = input(prompt1)
        prompt2 = """
What is your CVS password?
"""
        pwd = pwinput.pwinput(prompt=prompt2,mask='*')

        set_credentials_in_config(login, pwd)
        load_config()

    # Let's login (or if the credentials are bad, vomit up an error message).
    if not login_to_cvs():
        print('ERROR: Your CVS login information is incorrect. Please double-check by logging in manually.')
        rm_credentials_in_config()
        sys.exit()



################################################################################

################################################################################
################################## Functions ###################################
################################################################################

def load_config():
    global config, grocy_headers
    if not Path("config.json").is_file():
        print('ERROR: grocy-extras is not configured. Please run initialize_grocy.py first.')
        sys.exit()
    else:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            grocy_headers['GROCY-API-KEY'] = config['api_key']

def set_credentials_in_config(login, pwd):
    global config
    c = { 'cvs': { 'u': base64.b64encode(bytes(login, 'utf-8')).decode('utf-8'), 'p': base64.b64encode(bytes(pwd, 'utf-8')).decode('utf-8') } }
    config['c'] = c
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def rm_credentials_in_config():
    global config
    if config.get('c'):
        config['c'].pop('cvs', None)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def login_to_cvs():
    global config, session

    u = base64.b64decode(config['c']['cvs']['u']).decode('utf-8')
    p = base64.b64decode(config['c']['cvs']['p']).decode('utf-8')

    session.get('https://www.cvs.com')
    
    # x-experienceId is a mandatory header.
    regex = re.compile('"x-experienceId":"([0-9a-f-]+?)",')
    r = session.get('https://www.cvs.com/retail-component-server/v1/ui/header-build/v2/p-4d960940.entry.js')
    experience_id = re.search(regex, r.text).group(1)
    if not experience_id:
        print()
    # H = "6TiidoRjpQG3uSjKU33lgq97MAuVBtpz",
    session.headers['x-channel'] = 'WEB'
    session.headers['x-experienceid'] = experience_id
    session.headers['x-api-key'] = '6TiidoRjpQG3uSjKU33lgq97MAuVBtpz'
    session.headers['x-visitor-id'] = 'd5c4a96a10dc494484e180e0097dfc1a'
    session.headers['x-client-fingerprint-id'] = 'eyJjbGllbnRDaGFyYWN0ZXJpc3RpY3MiOnsiYnJvd3Nlck5hbWUiOiJGaXJlZm94IiwiYnJvd3Nlck1ham9yVmVyc2lvbiI6IjEzMyIsImJyb3dzZXJGdWxsVmVyc2lvbiI6IjEzMy4wIiwib3BlcmF0aW5nU3lzdGVtIjoiTWFjIE9TIiwib3NWZXJzaW9uIjoiMTAuMTUiLCJjYW52YXNQcmludCI6ImQ1YzRhOTZhMTBkYzQ5NDQ4NGUxODBlMDA5N2RmYzFhIiwiY2hhbm5lbCI6IldFQiIsInVhIjoiTW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTU7IHJ2OjEzMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzMy4wIiwiY2FudmFzUHJpbnRfb2xkIjoiZmFkN2Q4ZmY3NDE1ZTY4ZTQ1OTRiYmNkOThhMzE0NDIwNDc1YmM0MGJlNzk4NGJmYmIwMDExNWI4ODA3ZGM0ZiIsImJuY3AiOiJGaXJlZm94IiwiYm12Y3AiOiIxMzMiLCJidmNwIjoiMTMzLjAiLCJvc2NwIjoiTWFjIE9TIiwib3N2Y3AiOiIxMC4xNSJ9fQ=='
    # cp is a sha256 hash of a data-uri, of a blob, of a html canvast that the above js scribbled on. Doesn't look like it changes much though.
    r = session.post('https://www.cvs.com/api/guest/v1/token', json={'data':{'cp':'fad7d8ff7415e68e4594bbcd98a314420475bc40be7984bfbb00115b8807dc4f'}})
    session.cookies.set('access_token', r.json().get('access_token'),domain='*.cvs.com')
    
    # Actually start the login.
    r = session.post('https://www.cvs.com/api/client/experience/v1/load', json={'data':{'searchType':'BY_EMAIL_AND_PHONE','lob':'RETAIL','securityAccountLookupInput':{'email': u}}})

    # Password needs to be encrypted.
    r = session.get('https://www.cvs.com/account-login/_next/static/scripts/joseEncryption.js')
    regex = re.compile('prod:.pk:"([0-9a-f][0-9a-f](?::[0-9a-f][0-9a-f])+)".,qa')
    prod_pk = re.search(regex, r.text).group(1)
    print(prod_pk)

    r = session.post('https://www.cvs.com/api/auth/experience/v1/load', json=4)
    # {'data':{'inputReq':{'userName': u,'password': p,'grantType':'password','flowName':'FSLOGIN','lob':'RETAIL','fp': session.headers['x-client-fingerprint-id']}}}


    return True
#john.m.oyler@gmail.com
#m3LODY15ab@2009

################################################################################
################################################################################
            
main()
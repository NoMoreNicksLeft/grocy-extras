#!/usr/bin/env python

from pathlib import Path
import sys
import json, argparse
import requests
import grocy_extras

################################################################################
################################################################################

store_headers = {}

grocy_headers = { 'GROCY-API-KEY' : 'empty', 
                  'accept': 'application/json',
                  'Content-Type': 'application/json' }

parser = argparse.ArgumentParser(prog = 'add_product_xxx.py',
                                 description = 'add_product_xxx.py automatically adds a retail product to grocy given an EAN argument',
                                 epilog='Text at the bottom of help')
parser.add_argument('--dry-run', help = 'performs all actions other than adding product', action = 'store_true', dest = 'dry_run')
parser.add_argument('code')
args = parser.parse_args()

def main():

    load_config()

################################################################################
################################# Find store id ################################
################################################################################
    
    r1 = requests.get(f"{config.get('base_uri')}/api/objects/shopping_locations?query%5B%5D=name%3DUnited%20Supermarkets",
                     headers = grocy_headers)

    store_id = ''
    if not r1.json():
        # add the store now
        store_id = grocy_extras.add_store('United Supermarkets', 
                                          'united_supermarkets.png', 
                                          'https://www.unitedsupermarkets.com')
    else:
        store_id = r1.json()[0].get('id')

################################################################################
############################## Get product details #############################
################################################################################

# https://www.unitedsupermarkets.com/rs/products/00049000012590

    r2 = requests.get(f"https://www.unitedsupermarkets.com/rs/products/{args.code}",
                     headers = store_headers)
    print(r2.text)

################################################################################
################################ Quantity Unit #################################
################################################################################

# Due to the way grocy stores quantities, a 2 liter bottle of soda seems to
# require a "2L" quantity unit. There are probably dozens or hundreds of qty
# values for bottles, cans, boxes, bags, and so forth. These pretty much have to
# added when (and for the purpose of) adding products.

    r3 = requests.get(f"{config.get('base_uri')}/api/objects/shopping_locations?query%5B%5D=name%3DUnited%20Supermarkets",
                     headers = grocy_headers)
    
    qty_id = ''
    if not r3.json():
        # add the new quantity unit
        qty_id = grocy_extras.add_quantity_unit()
        # add any quantity conversion needed

    else:
        qty_id = r1.json()[0].get('id')

################################################################################
############################### Add the Product ################################
################################################################################

################################################################################
################################## Functions ###################################
################################################################################

def load_config():
    global config
    global grocy_headers
    if not Path("config.json").is_file():
        print('ERROR: grocy-extras is not configured. Please run initialize_grocy.py first.')
        sys.exit()
    else:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            grocy_headers['GROCY-API-KEY'] = config['api_key']

################################################################################
################################################################################
            
main()
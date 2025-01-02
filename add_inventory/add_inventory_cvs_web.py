#!/usr/bin/env python

from pathlib import Path
import sys, shutil
import json, argparse
# import add_product_cvs

################################################################################
################################################################################

grocy_headers = { 'GROCY-API-KEY' : 'empty', 
                  'accept': 'application/json',
                  'Content-Type': 'application/json' }

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
What is your password?
"""
        pwd = input(prompt2)
        prompt3 = """
CVS should 
"""

        print('a')


# ,
#     "c" : {
#         "cvs": { "u": "", "p": ""}
#     }
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
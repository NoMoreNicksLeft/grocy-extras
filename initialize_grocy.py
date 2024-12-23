#!/usr/bin/env python

from pathlib import Path
import sys, shutil
import json, argparse
import initialization as init

def main():
################################################################################
############################### Special commands ###############################
################################################################################

    parser = argparse.ArgumentParser(prog = 'initialize_grocy',
                                    description = 'A utility to simplify setting up grocy, https://grocy.info/',
                                    epilog = 'Just run without arguments or switches for typical use.',
                                    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=27))
    parser.add_argument('--delete-all-qty-units', help = 'deletes all existing quantity units', action = 'store_true', dest = 'delete_all_qty')
    parser.add_argument('--delete-all-stores', help = 'deletes all existing stores', action = 'store_true', dest = 'delete_all_stores')
    args = parser.parse_args()

    if args.delete_all_qty:
        load_config()
        init.delete_all_quantity_units()
        sys.exit()

################################################################################
#################################### Prelim ####################################
################################################################################

    first_prompt = """
grocy-extras initialization wizard!

\033[91mWARNING: This script assumes that no significant grocy configuration has 
occurred. It will clobber many custom settings if allowed to continue on an
already-configured system. Press control-C to exit now.\033[0m
"""

    load_config()

    print(first_prompt)

################################################################################
################################ Quantity Units ################################
################################################################################

    second_prompt = """
grocy has no default settings for quantities. Some "arbitrary" quantities like 
'count', 'box', and 'can' will be added to all systems. Please choose the 
appropriate quantity system for your usage:
"""

    qty_unit_options = """
1) American (gallons, pounds, inches) [note: also includes metric]
2) Metric (only)
x) Exit wizard

? """

    print(second_prompt)

    choice = ""

    while choice not in ["1", "2", "x"]:
        choice = input(qty_unit_options)
        if choice not in ["1", "2", "x"]: print("Option unavailable")
        elif choice == 'x': sys.exit()

    init.add_all_quantity_units(choice)

################################################################################
############################## Locations (Stores) ##############################
################################################################################

    third_prompt = """
grocy keeps track of where inventory items were purchased. You will need to add
those supermarkets which you shop at, either regularly or occasionally. 
Independent or non-chain supermarkets should be entered manually through the
grocy web interface. Which country are you in?
"""

    with open('data/stores.json') as f:
        init.stores = json.load(f)

    country_options = [f"{i+1}) {c.get('country')}" for i, c in enumerate(init.stores)]
    country_options.append('x) Exit wizard')
    country_options = "\n".join(country_options) + "\n"
    country_answers = [str(i+1) for i, c in enumerate(init.stores)]
    country_answers.append('x')

    print(third_prompt)

    choice1 = ""

    while choice1 not in country_answers:
        choice1 = input(country_options)
        if choice1 not in country_answers: print("Option unavailable")
        elif choice1 == 'x': sys.exit()

    fourth_prompt = """
Please choose any of the following stores. Separate multiple selections with 
commas. Which stores do you shop at?
"""

    store_options = format_store_options(int(choice1)-1)
    store_answers = ""

    print(fourth_prompt)

    choice2 = ""

    while choice2 not in store_answers:
        choice2 = input(store_options)
        if choice2 not in store_answers: print("Option unavailable")
        elif choice2 == 'x': sys.exit()

    # init.add_all_stores(choice1, choice2)

################################################################################
################################## Functions ###################################
################################################################################

def prompt_for_grocy_details():
    config_prompt = """
To be able to modify your grocy configuration, grocy-extras needs some details
about the installation. What is the url for the service?
"""

    config_prompt2 = """
grocy-extras also needs an API key. This is similar to a password, and you can
create one by clicking on the wrench icon in the top right corner, and selecting
"Manage API keys". From there, click the blue "Add" button at the top and add a
name for the key. Finally, copy and paste the key from the list.
What is the key?
"""

    uri = input(config_prompt)
    key = input(config_prompt2)
    init.config = {'base_uri': uri, 'api_key': key}
    init.headers['GROCY-API-KEY'] = key
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump({'base_uri': uri, 'api_key': key}, f, ensure_ascii=False, indent=4)
    print('got here')

def load_config():
    if not Path("config.json").is_file():
        prompt_for_grocy_details()
    else:
        with open('config.json', 'r') as config_file:
            init.config = json.load(config_file)
            init.headers['GROCY-API-KEY'] = init.config['api_key']

def format_store_options(country):
    terminal = shutil.get_terminal_size()

    lines = terminal.lines - 5
    options = [""] * lines
    total_stores = len(init.stores[country]['stores'])
    for i, s in enumerate(init.stores[country]['stores']):
        # print(str(i+1))
        # print(s.get('name'))
        options[i % lines] += "{:>2}) {}  ".format(str(i), s.get('name'))
        if i % lines == 5:
            wide = max(options, key=len)
            for j, o in enumerate(options):
                options[j] = f"{options[j]}:<{wide}"

    options = "\n".join(options) + "\n"

    print(options)

    return

################################################################################
################################################################################
            
main()
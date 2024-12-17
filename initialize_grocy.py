#!/usr/bin/env python

from pathlib import Path
import json

################################################################################
#################################### Prelim ####################################
################################################################################

first_prompt = """
grocy-extras initialization wizard!

\033[91mWARNING: This script assumes that no significant grocy configuration has 
occurred. It will clobber many custom settings if allowed to continue on an
already-configured system. Press control-C to exit now.\033[0m
"""

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

print(first_prompt)

if not Path("config.json").is_file():
    uri = input(config_prompt)
    key = input(config_prompt2)
    config = {'base_uri': uri, 'api_key': key}
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump({'base_uri': uri, 'api_key': key}, f, ensure_ascii=False, indent=4)
else:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        
import initialization as init


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

init.add_all_quantity_units(choice)

################################################################################
############################## Locations (Stores) ##############################
################################################################################


# grocy-extras
A set of tools to aid in the configuration and data population for grocy.

## Initialization script - initialize_grocy.py
This script sets up some basic configuration that is tedious to do by hand such as adding quantity units and conversions (though the bulk of these are done elsewhere). Run this script, answer its questions when prompted.

## Adding Inventory - ./add_inventory/*
These scripts add inventory semi-automatically and automatically. Many can be run from a cron job several times a day to have your inventory show up nearly immediately. All require logins to the store's web app. These scripts automatically add any missing configurations or products. Some (United Supermarkets, in Texas) prompt for missing information as the web app does not provide quantities (wtf?).

## Adding Products - ./add_products/*
Available to use but generally not necessary to run directly; the inventory scripts will call these as necessary. Feel free to tinker with these, deleting products out of Grocy is relatively straightforward.

## Circulars, flyers, and weekly ads - ./circulars/*
I've been known to lurk in r/datahoarder. These scripts can be run out of cron jobs and will download flyers one per week/month (or however often they're made available), so that you can keep a 100gbyte archive of tree-safe RiteAid advertisements. 

# Development
1. Create the virtual environment with `python -m venv .venv`
2. Activate it with `source .venv/bin/activate`
3. Install modules with `pip install -r requirements.txt`
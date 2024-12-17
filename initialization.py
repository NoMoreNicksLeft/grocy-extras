import sys
import json
import requests

headers = { 'GROCY-API-KEY' : config['api_key'], 
            'accept': 'application/json',
            'Content-Type': 'application/json' }

################################################################################
################################## Functions ###################################
################################################################################

def delete_all_quantity_units():
    r = requests.get(config['base_uri'] + '/api/objects/quantity_units', )
    return

def add_all_quantity_units(option):
    match option:
        case "1":
            data_file = 'american_units.json'
        case "2":
            data_file = 'metric_units.json'
        case "x":
            sys.exit()

    with open('data/' + data_file) as f:
        units = json.load(f)

    # Add the units first, can't do conversions here because both units need to
    # exist for that to succeed.
    for unit in units:
        print(add_quantity_unit(unit['singular'], unit['plural'], unit['description']))

    # Now do the conversions.
    # for unit in units:
    #     for conversion in unit['conversions']:
    #         print('f')
    
    return

def add_quantity_unit(singular, plural, description):
    r = requests.post(config['base_uri'] + '/api/objects/quantity_units', 
                      headers = headers,
                      json = {'name': singular, 'name_plural': plural, 'active': '1', 'description': description})

    return r.json().get('created_object_id')
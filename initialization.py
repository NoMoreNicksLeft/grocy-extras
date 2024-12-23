import json
import requests
import alive_progress 

headers = { 'GROCY-API-KEY' : 'empty', 
            'accept': 'application/json',
            'Content-Type': 'application/json' }
config = {}

alive_progress.config_handler.set_global(length=60)

################################################################################
################################## Functions ###################################
################################################################################

def delete_all_quantity_units():
    r = requests.get(f"{config.get('base_uri')}/api/objects/quantity_units",
                     headers = headers)
    with alive_progress.alive_bar(len(r.json()), title='Qty Units  ') as bar:
        for unit in r.json():
            requests.delete(f"{config.get('base_uri')}/api/objects/quantity_units/{unit.get('id')}",
                            headers = headers)
            bar()
    return

def add_all_quantity_units(option):
    match option:
        case "1":
            data_file = 'american_units.json'
        case "2":
            data_file = 'metric_units.json'

    with open('data/' + data_file) as f:
        units = json.load(f)

    conversions_count = 0

    print()

    # Add the units first, can't do conversions here because both units need to
    # exist for that to succeed.
    with alive_progress.alive_bar(len(units), title='Qty Units  ') as bar:
        for unit in units:
            unit_id = add_quantity_unit(unit['singular'], unit['plural'], unit['description'])
            if unit_id:
                bar()

            for i, un in enumerate(units):
                if un.get('singular') == unit['singular']:
                    units[i]['id'] = unit_id
                if un.get('conversions'):
                    for j, conversion in enumerate(units[i]['conversions']):
                        if conversion.get('name') == unit['singular']:
                            units[i]['conversions'][j]['id'] = unit_id
                            conversions_count += 1

    # Now do the conversions.
    with alive_progress.alive_bar(conversions_count // 2, title='Conversions') as bar:
        for unit in units:
            if unit.get('conversions'):
                for conversion in unit['conversions']:
                    r = requests.post(f"{config.get('base_uri')}/api/objects/quantity_unit_conversions",
                                      headers = headers,
                                      json = {'to_qu_id': conversion.get('id'), 'factor': conversion.get('ratio'), 'from_qu_id': unit.get('id')})
                    if r.status_code == requests.codes.ok:
                        bar()
    return

def add_quantity_unit(singular, plural, description):
    r = requests.post(f"{config.get('base_uri')}/api/objects/quantity_units",
                      headers = headers,
                      json = {'name': singular, 'name_plural': plural, 'active': '1', 'description': description})

    return r.json().get('created_object_id')

def add_all_stores(country_option, store_indices):
    if country_option == 'x':
        sys.exit()
    
    return

def add_store(country_id, store):
    return
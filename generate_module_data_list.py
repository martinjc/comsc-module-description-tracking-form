import os
import csv
import json

###
# A quick and dirty script to get something to start with. Generates a list of module codes
# from a heavily edited version of the COMSC teaching allocation spreadsheet

SRC_DATA_DIR = os.path.join(os.getcwd(), 'src_data')

modules = []

with open(os.path.join(SRC_DATA_DIR, 'module_data.csv'), 'r') as in_file:

    csv_reader = csv.DictReader(in_file)
    for row in csv_reader:
        modules.append({'module_code': row['Code'], 'module_title': row['Title'], 'module_leader_(comsc-data)': row['Staff']})

with open(os.path.join(SRC_DATA_DIR, 'module_data_list.json'), 'w') as out_file:
    json.dump(modules, out_file)

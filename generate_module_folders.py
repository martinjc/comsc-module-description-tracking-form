import os
import requests
import subprocess

from lib.handbookdata import *

# where to put all the module descriptions
OUTPUT_DIR = os.path.join(os.getcwd(), 'dist')

# get the list of modules for the school
modules = get_module_list('COMSC')
for module in modules:
    mcode = module['moduleCode']
    if not os.path.exists(os.path.join(OUTPUT_DIR, mcode)):
        os.makedirs(os.path.join(OUTPUT_DIR, mcode))

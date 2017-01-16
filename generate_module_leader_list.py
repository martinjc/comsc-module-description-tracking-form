import os
import csv

from lib.handbookdata import *

# where to put all the module descriptions
OUTPUT_DIR = os.path.join(os.getcwd(), 'src_data')

if __name__ == "__main__":

    fields = ['Module Code', 'Module Title', 'First Name', 'Surname', 'Email']
    module_leader_data = []

    modules = get_module_list('COMSC')
    for module in modules:

        mcode = module['moduleCode']
        print(mcode)

        module_data = get_module_handbook(mcode)

        module_staff = module_data['occurrences']['staff']['moduleLeader']
        ml_dict = {}
        module_leader_data.append({
            'Module Code': mcode,
            'Module Title': module_data['module']['moduleName'],
            'First Name': module_staff['firstName'],
            'Surname': module_staff['surname'],
            'Email': ""
        })

    with open(os.path.join(OUTPUT_DIR, 'module_leader_list.csv'), 'w') as output_file:
        csv_writer = csv.DictWriter(output_file, fields)
        csv_writer.writeheader()
        csv_writer.writerows(module_leader_data)

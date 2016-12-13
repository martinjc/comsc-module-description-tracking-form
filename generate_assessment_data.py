import os
import csv
import requests

from lib.handbookdata import *
from lib.pdfdata import *


# where to put all the module descriptions
OUTPUT_DIR = os.path.join(os.getcwd(), 'src_data')

filled_fields = []

if __name__ == "__main__":


    with open(os.path.join(OUTPUT_DIR, 'assessment_data.csv'), 'w') as output_file:

        fields = ['moduleCode', 'assessmentNumber', 'assessmentType', 'assessmentName', 'percentage']

        writer = csv.DictWriter(output_file, fields)
        writer.writeheader()

        # get the list of modules for the school
        modules = get_module_list('COMSC')

        # get the handbook data and create a fillable pdf
        # for each module
        for module in modules:
            mcode = module['moduleCode']

            module_data = get_module_handbook(mcode)

            count = 1
            for assessment in module_data['assessments']:

                data = {
                    'moduleCode': mcode,
                    'assessmentNumber': count,
                    'assessmentType': assessment['assessmentType']['assessmentType'],
                    'assessmentName': assessment['name'],
                    'percentage': assessment['percentage']
                }
                count += 1
                writer.writerow(data)

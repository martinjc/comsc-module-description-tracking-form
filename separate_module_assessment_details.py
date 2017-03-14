import os
import pandas
import shutil

from tqdm import tqdm

from lib.handbookdata import get_module_list

assessment_data = pandas.read_excel('extracted/assessment-details.xlsx')

modules = get_module_list('COMSC')

for module in tqdm(modules):

    mcode = module['moduleCode']
    module_data = assessment_data[assessment_data['Module Code'] == mcode]
    del module_data['Assessment Date (MD)']
    del module_data['Assessment Title (TF)']
    del module_data['Assessment Type (TF)']
    del module_data['Assessment Contribution (TF)']
    with open(os.path.join('extracted', 'module_assessment', '%s_assessment.csv' % mcode), 'w') as output_file:
        output_file.write(module_data.to_csv())

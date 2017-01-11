import os
import math
import pandas
import requests
import subprocess

from fdfgen import forge_fdf

from lib.handbookdata import *
from lib.pdfdata import *
from lib.html import *

# where to put all the module descriptions
OUTPUT_DIR = os.path.join(os.getcwd(), 'dist', 'tracking_forms')

# source data
SOURCE_DIR = os.path.join(os.getcwd(), 'src_data')

def add_existing_data(filled_fields, key, value):
    filled_fields.append((key, value))
    return filled_fields

def get_description(descriptions, name):
    """
    Extract a named description from the list of descriptions in
    the module handbook data, and return it as text
    """
    for description in descriptions:
        if description['descriptionName']['descriptionCode'] == name:
            return strip_tags(description['descriptionDetail'])
    return None


def fill_teaching_hours(filled_fields, module_code):
    with open(os.path.join(SOURCE_DIR, 'KIS.csv')) as input_file:
        kis_data = pandas.read_csv(input_file, index_col=0)
        if module_code in kis_data.index:
            module_data = kis_data.loc[module_code]
            for column in kis_data.columns:
                filled_fields = add_existing_data(filled_fields, column, module_data.ix[column])

    return filled_fields

def fill_assessment_data(filled_fields, module_data, module_code):
    with open(os.path.join(SOURCE_DIR, 'assessment_data.csv')) as input_file:
        kis_data = pandas.read_csv(input_file)
        assessment_data = kis_data.loc[kis_data['moduleCode'] == module_code]
        count = 1
        for assessment in module_data['assessments']:
            if count <= 4:
                filled_fields = add_existing_data(filled_fields, '4-textbox-assessment%d-weighting' % count, assessment['percentage'])
                filled_fields = add_existing_data(filled_fields, '4-textbox-assessment%d-title' % count, assessment['name'])
                filled_fields = add_existing_data(filled_fields, '4-dropdown-assessment%d-type' % count, assessment['assessmentType']['assessmentType'])
                filled_fields = add_existing_data(filled_fields, '4-textbox-assessment%d-hand_out_week' % count, assessment_data.loc[assessment_data['assessmentNumber'] == count, 'approximateHandOut'].values[0])
                filled_fields = add_existing_data(filled_fields, '4-textbox-assessment%d-hand_in_week' % count, assessment_data.loc[assessment_data['assessmentNumber'] == count, 'approximateHandIn'].values[0])
                count += 1

    return filled_fields


def fill_software_requirements(filled_fields, module_code):

    with open(os.path.join(SOURCE_DIR, 'SoftwareRequirements.csv')) as input_file:
        software_data = pandas.read_csv(input_file)
        software_data.fillna('?', inplace=True)
        module_data = software_data.loc[software_data['ModuleCode'] == module_code]
        software_details = ""
        for row in module_data.itertuples():
            software_details += row[2]
            if row[3] is not '?':
                software_details += " (min ver: %s" % row[3]
                if row[4] is not '?':
                    software_details += ", max ver: %s" % row[4]
                software_details += ")"
            if row[5] is not '?':
                software_details += (" (SupportedOS: %s)\n" % row[5])
        filled_fields = add_existing_data(filled_fields, '5-textbox-software_lab_requirements', software_details)

    return filled_fields

if __name__ == "__main__":

    # get the list of modules for the school
    modules = get_module_list('COMSC')

    # get the handbook data and create a fillable pdf
    # for each module
    for module in modules:
        mcode = module['moduleCode']
        print(mcode)

        filled_fields = []
        module_data = get_module_handbook(mcode)

        filled_fields = add_existing_data(filled_fields, "ModuleCode", mcode)
        filled_fields = fill_teaching_hours(filled_fields, mcode)
        filled_fields = fill_assessment_data(filled_fields, module_data, mcode)
        filled_fields = fill_software_requirements(filled_fields, mcode)

        fdf = forge_fdf("", filled_fields, [], [], [])
        fdf_file = open(os.path.join(OUTPUT_DIR, 'data.fdf'), 'wb')
        fdf_file.write(fdf)
        fdf_file.close()

        subprocess.run(["pdftk", "templates/tracking_form_template.pdf",  "fill_form",  "dist/tracking_forms/data.fdf", "output", "dist/%s/%s_tracking_form.pdf" % (mcode, mcode)])

import os
import json
import requests

from datetime import datetime

FIELD_NAMES = ["module_name","module_code","level","delivery_language","module_leader","school_code","external_subject_code","number_of_credits","module_description","semester","learning_outcomes","delivery","skills","assessment","1_assessment_title","1_assessment_type","1_assessment_contribution","1_assessment_date","2_assessment_title","2_assessment_type","2_assessment_contribution","2_assessment_date","3_assessment_title","3_assessment_type","3_assessment_contribution","3_assessment_date","4_assessment_title","4_assessment_type","4_assessment_contribution","4_assessment_date","5_assessment_title","5_assessment_type","5_assessment_contribution","5_assessment_date","6_assessment_title","6_assessment_type","6_assessment_contribution","6_assessment_date","syllabus_content","essential_reading","background_reading"]

YEAR1 = ['CM1101', 'CM1102', 'CM1103', 'CM1104', 'CM1201', 'CM1202', 'CM1204', 'CM1205', 'CM1206', 'CM1208', 'CM1209']
YEAR2 = ['CM2101', 'CM2102', 'CM2103', 'CM2104', 'CM2105', 'CM2201', 'CM2203', 'CM2205', 'CM2206', 'CM2207', 'CM2208', 'CM2302', 'CM2303', 'CM2305', 'CM2500']
YEAR3 = ['CM3101', 'CM3103', 'CM3104', 'CM3105', 'CM3106', 'CM3107', 'CM3109', 'CM3110', 'CM3111', 'CM3112', 'CM3113', 'CM3114', 'CM3201', 'CM3202', 'CM3203', 'CM3301', 'CM3302', 'CM3303', 'CM3304']
MSC = ['CMT102', 'CMT103', 'CMT104', 'CMT105', 'CMT106', 'CMT107', 'CMT108', 'CMT111', 'CMT112', 'CMT202', 'CMT205', 'CMT206', 'CMT207', 'CMT209', 'CMT212', 'CMT213', 'CMT301', 'CMT302', 'CMT303', 'CMT304', 'CMT305', 'CMT306', 'CMT400']
NSA_YEAR1 = ['CM6112', 'CM6113', 'CM6114', 'CM6121', 'CM6122', 'CM6123']
NSA_YEAR2 = ['CM6211', 'CM6212', 'CM6213', 'CM6221', 'CM6222', 'CM6223']
NSA_YEAR3 = ['CM6311', 'CM6312', 'CM6321', 'CM6331', 'CM6332']

BASE_URL = 'https://handbooks.data.cardiff.ac.uk'
ASPECTS = {
    'module_list': 'modulesrunning',
    'module': 'module'
}

def get_module_list(school, year=datetime.now().year):
    """
    Retrieves the list of all modules running in the supplied school and year

    If no module list is returned from the API, returns None
    """

    # API expects uppercase school acronym
    school = school.upper()

    # Construct the API url
    module_list_url = '%s/%s/%s/%s' % (BASE_URL, ASPECTS['module_list'], school, year)

    # Retrieve the data
    r = requests.get(module_list_url)
    data = r.json()

    # Check we got something back
    if data.get('modRunning'):
        return data['modRunning']
    else:
        return None

def get_module_handbook(module_code, occurence = ''):
    """
    Retrieves the module handbook for the supplied module code and occurence (if any)
    """

    module_code = module_code.upper()

    # Construct the API url
    module_handbook_url = '%s/%s/%s/%s' % (BASE_URL, ASPECTS['module'], module_code, occurence)

    # Retrieve and return the data
    r = requests.get(module_handbook_url)
    data = r.json()

    return data


if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), 'src_data', 'COMSC_modules.json'), 'w') as output_file:
        module_list = get_module_list('COMSC')
        print(module_list)
        json.dump(module_list, output_file)
    with open(os.path.join(os.getcwd(), 'src_data', 'sample_module_description.json'), 'w') as output_file:
        module_details = get_module_handbook('CMT112')
        print(module_details)
        json.dump(module_details, output_file)

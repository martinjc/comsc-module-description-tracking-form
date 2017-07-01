import os
import csv
import pandas
import subprocess

from difflib import Differ, HtmlDiff
from bs4 import BeautifulSoup as bs

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list
from lib.handbookdata import FIELD_NAMES_AND_LABELS as field_names, ASSESSMENT_NAMES_AND_LABELS as asssesment_names, NON_ASSESSMENT_FIELD_NAMES as na_field_names, FIELD_NAMES as FN


def convert_data_to_text(input_data, output_file):

    for fn in field_names:
        if input_data.get(fn):
            output_file.write('%s:\n' % fn)
            output_file.write('%s\n' % input_data[fn])


if __name__ == "__main__":

    modules = get_module_list('COMSC')

    updated_folder = os.path.join(os.getcwd(), 'comparisons', 'shared_drive')
    txt_folder = os.path.join(os.getcwd(), 'text')

    for module in modules:

        mcode = module['moduleCode']

        if os.path.exists(os.path.join(updated_folder, mcode)):
            print(mcode)

            subprocess.run(["pdftk", "comparisons/shared_drive/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "modified.fdf"])

            with open("modified.fdf", 'r', encoding='utf-8') as modified_input:
                modified_data = parse_fdf(modified_input)

                with open(os.path.join(txt_folder, "%s.txt" % module), 'w') as modified_text:
                    convert_data_to_text(modified_data, modified_text)

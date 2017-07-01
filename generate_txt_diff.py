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

def replace_style(html_string, new_style_string):
    soup = bs(html_string, 'html.parser')
    head = soup.head
    new_style = soup.new_tag("style")
    new_style.string = new_style_string
    head.style.replace_with(new_style)
    return str(soup)

def create_diffs(original_file, modified_file, output_diff_file, output_html_file, changes_file):

    d = Differ()
    original = original_file.readlines()
    modified = modified_file.readlines()
    output_diff_file.writelines(list(d.compare(original, modified)))
    hd = HtmlDiff()

    html_string = hd.make_file(original, modified)
    html = replace_style(html_string, "table.diff {font-family:Courier; border:medium;table-layout: fixed;width:100%;}.diff_header {background-color:#e0e0e0}td {word-wrap: break-word;white-space: normal;}td.diff_header {text-align:right; width:3%;}.diff_next {background-color:#c0c0c0; width: 1.5%}.diff_add {background-color:#aaffaa}.diff_chg {background-color:#ffff77}.diff_sub {background-color:#ffaaaa}")
    output_html_file.write(html)

    changes_string = hd.make_file(original, modified, context=True, numlines=1)
    html = replace_style(changes_string, "table.diff {font-family:Courier; border:medium;table-layout: fixed;width:100%;}.diff_header {background-color:#e0e0e0}td {word-wrap: break-word;white-space: normal;}td.diff_header {text-align:right; width:3%;}.diff_next {background-color:#c0c0c0; width: 1.5%}.diff_add {background-color:#aaffaa}.diff_chg {background-color:#ffff77}.diff_sub {background-color:#ffaaaa}")
    changes_file.write(html)


if __name__ == "__main__":

    modules = get_module_list('COMSC')

    original_folder = os.path.join(os.getcwd(), 'comparisons', 'original')
    updated_folder = os.path.join(os.getcwd(), 'comparisons', 'shared_drive')
    diff_folder = os.path.join(os.getcwd(), 'comparisons', 'diffs-for-entry')

    fns = FN
    columns = []
    for fn in fns:
        if field_names.get(fn):
            columns.append(field_names[fn])
    for i in range(1,6):
        for fn, label in asssesment_names.items():
            columns.append('%s-%d' % (label, i))

    updated_data = pandas.DataFrame(index=columns)

    for module in modules:

        mcode = module['moduleCode']

        if os.path.exists(os.path.join(original_folder, mcode)) and os.path.exists(os.path.join(updated_folder, mcode)):
            print(mcode)

            module_data = pandas.Series(index=columns)

            subprocess.run(["pdftk", "comparisons/original/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "original.fdf"])
            subprocess.run(["pdftk", "comparisons/shared_drive/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "modified.fdf"])

            with open("original.fdf", 'r', encoding='utf-8') as original_input, open("modified.fdf", 'r', encoding='utf-8') as modified_input, open(os.path.join(diff_folder, '%s_changes.csv' % (mcode)), 'w', encoding='utf-8') as csv_output_file, open(os.path.join(diff_folder, '%s_changes.txt' % (mcode)), 'w', encoding='utf-8') as txt_output_file:
                original_data = parse_fdf(original_input)
                modified_data = parse_fdf(modified_input)

                with open("original.txt", 'w') as original_text:
                    convert_data_to_text(original_data, original_text)
                with open("modified.txt", 'w') as modified_text:
                    convert_data_to_text(modified_data, modified_text)

                # with open("original.txt", 'r') as ot, open("modified.txt", 'r') as mt, open("comparisons/diffs-mjc/%s_diff.txt" % (mcode, mcode), "w") as dfile, open("comparisons/diffs-mjc/%s/%s_diff.html" % (mcode, mcode), "w") as hdfile, open("comparisons/diffs-mjc/%s/%s_changes_only.html" % (mcode, mcode), "w") as chfile:
                #     create_diffs(ot, mt, dfile, hdfile, chfile)


                writer = csv.DictWriter(csv_output_file, field_names.values(), quoting=csv.QUOTE_ALL)
                writer.writeheader()

                row = {}
                for fn in na_field_names:
                    if original_data.get(fn) and modified_data.get(fn):
                        if original_data[fn] != modified_data[fn]:
                            label = field_names[fn]
                            row[label] = modified_data[fn]
                            module_data[label] = modified_data[fn]
                            txt_output_file.write('%s:\n' % label)
                            txt_output_file.write('----------------------------------------------\n')
                            txt_output_file.write('%s\n' % modified_data[fn])
                            txt_output_file.write('\n----------------------------------------------\n')

                txt_output_file.write('\nAssessment Breakdown\n')
                for i in range(6):
                    fn_type = '%d_assessment_type' % (i+1)
                    fn_cont = "%d_assessment_contribution" % (i+1)
                    fn_title = "%d_assessment_title" % (i+1)
                    fn_date = "%d_assessment_date" % (i+1)
                    if modified_data.get(fn_type) or modified_data.get(fn_cont) or modified_data.get(fn_title) or modified_data.get(fn_date):
                        txt_output_file.write('\nAssessment %d\n' % (i+1))
                        for fn, label in asssesment_names.items():
                            fn = '%d%s' % ((i+1), fn)
                            fn_label = '%s-%d' % (fn, (i+1))
                            if original_data.get(fn) or modified_data.get(fn):
                                txt_output_file.write('%s: ' % label)
                                if modified_data.get(fn):
                                    txt_output_file.write(' %s\n' % modified_data[fn])
                                    module_data[fn_label] = modified_data[fn]
                                elif original_data.get(fn):
                                    txt_output_file.write(' %s\n' % original_data[fn])
                                    module_data[fn_label] = original_data[fn]
                updated_data[mcode] = module_data
                writer.writerow(row)

    with open('test.csv', 'w') as out_file:
        out_file.write(updated_data.to_csv())

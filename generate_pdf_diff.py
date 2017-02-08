import os
import csv
import subprocess

from difflib import Differ, HtmlDiff
from bs4 import BeautifulSoup as bs

from lib.handbookdata import get_module_list
from lib.handbookdata import FIELD_NAMES as field_names


def parse_fdf(open_file):
    fields = []
    field = {}
    for line in open_file.readlines():
        if line == "---\n":
            fields.append(field)
            field = {}
        else:
            if line.startswith('Field'):
                current_field = line.split(':')[0].strip()
                field[current_field] = []
                field[current_field].append(line.split(':')[1])
            else:
                field[current_field].append(line)
    fields.append(field)
    data = {}
    for field in fields:
        if field.get('FieldName') and field.get('FieldValue'):
            field['FieldName'] = [s.strip() for s in field['FieldName']]
            data["".join(field['FieldName'])] = "".join(field['FieldValue'])
    return data

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
    updated_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader')
    diff_folder = os.path.join(os.getcwd(), 'comparisons', 'diffs')

    for module in modules:

        mcode = module['moduleCode']

        if os.path.exists(os.path.join(original_folder, mcode)) and os.path.exists(os.path.join(updated_folder, mcode)):
            print(mcode)

            if not os.path.exists(os.path.join(diff_folder, mcode)):
                os.makedirs(os.path.join(diff_folder, mcode))

            subprocess.run(["pdftk", "comparisons/original/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "original.fdf"])
            subprocess.run(["pdftk", "comparisons/module_leader/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "modified.fdf"])

            with open("original.fdf", 'r', encoding='utf-8') as original_input, open("modified.fdf", 'r', encoding='utf-8') as modified_input, open('comparisons/diffs/%s/%s_changes.csv' % (mcode, mcode), 'w', encoding='utf-8') as output_file:
                original_data = parse_fdf(original_input)
                modified_data = parse_fdf(modified_input)

                with open("original.txt", 'w') as original_text:
                    convert_data_to_text(original_data, original_text)
                with open("modified.txt", 'w') as modified_text:
                    convert_data_to_text(modified_data, modified_text)

                with open("original.txt", 'r') as ot, open("modified.txt", 'r') as mt, open("comparisons/diffs/%s/%s_diff.txt" % (mcode, mcode), "w") as dfile, open("comparisons/diffs/%s/%s_diff.html" % (mcode, mcode), "w") as hdfile, open("comparisons/diffs/%s/%s_changes_only.html" % (mcode, mcode), "w") as chfile:
                    create_diffs(ot, mt, dfile, hdfile, chfile)

                writer = csv.DictWriter(output_file, field_names, quoting=csv.QUOTE_ALL)
                writer.writeheader()

                row = {}
                for fn in field_names:
                    if original_data.get(fn) and modified_data.get(fn):
                        if original_data[fn] != modified_data[fn]:
                            row[fn] = modified_data[fn]
                writer.writerow(row)

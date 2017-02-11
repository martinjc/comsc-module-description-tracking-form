import os
import json

def get_fields_as_dict_from_pdf_datafile(fdf_data_file):

    """
    Returns a dict with keys representing the fields from a PDF form as represented
    by an fdf file. Obtain an fdf description of a PDF form using the command line
    pdftk tool: "pdftk PDF_FORM_FILE.pdf dump_data_fields_utf8 output OUTPUT_FILE.fdf"
    """
    fields = {}

    with open(fdf_data_file, 'r') as fdf_file:
        for line in fdf_file:
            if 'FieldName:' in line:
                key_value = line.split(' ')
                value = key_value[1].rstrip()
                fields[value] = None

    return fields


def parse_fdf(fdf_data_file):

    """
    Extracts all fields and values from an fdf file. Obtain an fdf description of a PDF form using the command line
    pdftk tool: "pdftk PDF_FORM_FILE.pdf dump_data_fields_utf8 output OUTPUT_FILE.fdf"
    """
    fields = []
    field = {}
    for line in fdf_data_file.readlines():
        if line == "---\n":
            fields.append(field)
            field = {}
        else:
            if line.startswith('Field'):
                current_field = line[:line.find(':')].strip()
                #print(current_field)
                #current_field = line.split(':')[0].strip()
                field[current_field] = []
                value = line[line.find(':')+1:].strip()
                #print(value)
                field[current_field].append(value)
            else:
                field[current_field].append(line)
    fields.append(field)
    data = {}
    for field in fields:
        if field.get('FieldName') and field.get('FieldValue'):
            field['FieldName'] = [s.strip() for s in field['FieldName']]
            data["".join(field['FieldName'])] = "".join(field['FieldValue'])
    return data

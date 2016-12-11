import os
import json

def get_fields_as_dict_from_pdf_datafile(fdf_data_file):

    """
    Returns a dict with keys representing the fields from a PDF form as represented
    by an fdf file. Obtain an fdf description of a PDF form using the command line
    pdftk tool: "pdftk PDF_FORM_FILE.pdf dump_data_fields output OUTPUT_FILE.fdf"
    """
    fields = {}

    with open(fdf_data_file, 'r') as fdf_file:
        for line in fdf_file:
            if 'FieldName:' in line:
                key_value = line.split(' ')
                value = key_value[1].rstrip()
                fields[value] = None

    return fields


if __name__ == "__main__":

    with open(os.path.join(os.getcwd(), 'lib', 'field_2_sims_mapping.json'), 'w') as output_mapping:
        input_file = os.path.join(os.getcwd(), 'templates', 'module_description_template.fdf')
        blank_mapping = get_fields_as_dict_from_pdf_datafile(input_file)
        json.dump(blank_mapping, output_mapping)

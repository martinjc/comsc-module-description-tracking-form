import os
import requests
import subprocess

from fdfgen import forge_fdf

SRC_DATA_DIR = os.path.join(os.getcwd(), 'src_data')
OUTPUT_DIR = os.path.join(os.getcwd(), 'dist')


def get_fields_as_dict_from_datafile(datafile):

    fdf_data_file = os.path.join(datafile)
    fields = {}

    with open(fdf_data_file, 'r') as fdf_file:
        for line in fdf_file:
            if 'FieldName:' in line:
                key_value = line.split(' ')
                value = key_value[1].rstrip()
                fields[value] = None

    return fields


if __name__ == "__main__":

    datafile = os.path.join(SRC_DATA_DIR, 'fields.fdf')
    fields = get_fields_as_dict_from_datafile(datafile)
    print(fields)

    filled_fields = []

    # for field, value in fields.items():
    #     if field != 'ModuleCode':
    #         print(field)
    #         filled_fields.append((field, ""))
    filled_fields.append(('ModuleCode', 'CMT112'))

    fdf = forge_fdf("", filled_fields, [], [], [])
    fdf_file = open(os.path.join(OUTPUT_DIR, 'data.fdf'), 'wb')
    fdf_file.write(fdf)
    fdf_file.close()

    subprocess.run(["pdftk", "src_data/TrackingForm.pdf",  "fill_form",  "dist/data.fdf", "output", "dist/output.pdf"])

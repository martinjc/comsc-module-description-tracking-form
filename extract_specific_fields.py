import os
import json
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list


if __name__ == "__main__":

    with open("COMSC_ReadingLists.txt", 'w') as reading_lists:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader-mjc')

        module_data = {}

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)
                reading_lists.write("%s\n\n" % mcode)

                module_data[mcode] = {}

                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "data.fdf"])

                with open("data.fdf", 'r', encoding='utf-8') as data_input:
                    data = parse_fdf(data_input)

                    reading_fields = ["essential_reading","background_reading"]

                    for field in reading_fields:
                        if data.get(field):
                            reading_lists.write("%s\n\n" % field)
                            reading_lists.write("%s\n" % data[field])
                            module_data[mcode][field] = data[field]

                reading_lists.write("-------------------------------------\n")

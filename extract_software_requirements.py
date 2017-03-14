import os
import csv
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list, TF_SUPPORT_FIELDS





if __name__ == "__main__":

    extract_dir = os.path.join(os.getcwd(), 'extracted')

    output_file = os.path.join(extract_dir, 'software-requirements.csv')

    with open(output_file, 'w') as out:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader-mjc')

        module_data = []
        keys = [
            "Module Code",
            "Software Requirements",
        ]

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)

                mdata = {"Module Code": mcode}

                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_tracking_form.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "data.fdf"])

                with open("data.fdf", 'r', encoding='utf-8') as data_input:
                    data = parse_fdf(data_input)

                    if data.get("5-textbox-software_lab_requirements"):
                        mdata["Software Requirements"] = data["5-textbox-software_lab_requirements"]#.strip()

                module_data.append(mdata)

        writer = csv.DictWriter(out, list(keys))
        writer.writeheader()
        writer.writerows(module_data)

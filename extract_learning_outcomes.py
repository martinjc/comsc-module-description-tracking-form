import os
import csv
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list, TF_SUPPORT_FIELDS





if __name__ == "__main__":

    extract_dir = os.path.join(os.getcwd(), 'extracted')

    output_file = os.path.join(extract_dir, 'learning_outcomes.csv')

    with open(output_file, 'w') as out:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'shared_drive')

        module_data = []
        keys = [
            "Module Code",
            "Learning Outcomes",
        ]

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)

                mdata = {"Module Code": mcode}

                subprocess.run(["pdftk", "comparisons/shared_drive/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "md_data.fdf"])

                with open("md_data.fdf", 'r', encoding='utf-8') as data_input:
                    data = parse_fdf(data_input)

                    if data.get("learning_outcomes"):
                        mdata["Learning Outcomes"] = data["learning_outcomes"]#.strip()

                module_data.append(mdata)

        writer = csv.DictWriter(out, list(keys))
        writer.writeheader()
        writer.writerows(module_data)

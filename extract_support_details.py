import os
import csv
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list, TF_SUPPORT_FIELDS





if __name__ == "__main__":

    extract_dir = os.path.join(os.getcwd(), 'extracted')

    output_file = os.path.join(extract_dir, 'support.csv')

    with open(output_file, 'w') as out:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader-mjc')

        module_data = []
        keys = set()

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)

                mdata = {"Module Code": mcode}
                keys.add("Module Code")

                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_tracking_form.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "data.fdf"])

                with open("data.fdf", 'r', encoding='utf-8') as data_input:
                    data = parse_fdf(data_input)

                    if data.get("3-radio-require_phd_support_tutorials"):
                        keys.add("Requires Tutorial Support")
                        if data["3-radio-require_phd_support_tutorials"].strip() == "0":
                            mdata["Requires Tutorial Support"] = "Yes"
                        else:
                            mdata["Requires Tutorial Support"] = "No"

                    if data.get("3-textbox-skills_for_tutorial_tutors"):
                        keys.add("Tutorial Skills Required")
                        mdata["Tutorial Skills Required"] = data["3-textbox-skills_for_tutorial_tutors"].strip()


                    if data.get("3-radio-no-require_phd_support_labs"):
                        keys.add("Requires Lab Support")
                        if data["3-radio-no-require_phd_support_labs"].strip() == "0":
                            mdata["Requires Lab Support"] = "Yes"
                        else:
                            mdata["Requires Lab Support"] = "No"

                    if data.get("3-textbox-skills_for_lab_tutors"):
                        keys.add("Lab Skills Required")
                        mdata["Lab Skills Required"] = data["3-textbox-skills_for_lab_tutors"].strip()

                module_data.append(mdata)

        writer = csv.DictWriter(out, list(keys))
        writer.writeheader()
        writer.writerows(module_data)

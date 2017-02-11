import os
import csv
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list, TF_SUPPORT_FIELDS





if __name__ == "__main__":

    extract_dir = os.path.join(os.getcwd(), 'extracted')

    output_file = os.path.join(extract_dir, 'kis-data.csv')

    with open(output_file, 'w') as out:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader-mjc')

        module_data = []
        keys = [
            "Module Code",
            "Classroom based lectures",
            "Classroom-based seminars and/or tutorials",
            "Scheduled online activities",
            "Practical classes and workshops",
            "Supervised time in studio/laboratory/workshop",
            "Fieldwork",
            "External Visits",
            "Work-based learning",
            "Scheduled Examination/Assessment",
            "Placement",
            "Total Scheduled Teaching"
        ]

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)

                mdata = {"Module Code": mcode}

                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_tracking_form.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "data.fdf"])

                with open("data.fdf", 'r', encoding='utf-8') as data_input:
                    data = parse_fdf(data_input)

                    if data.get("2-textbox-classroom_based_lectures"):
                        mdata["Classroom based lectures"] = data["2-textbox-classroom_based_lectures"].strip()
                    if data.get("2-textbox-classroom_based_seminars"):
                        mdata["Classroom-based seminars and/or tutorials"] = data["2-textbox-classroom_based_seminars"].strip()
                    if data.get("2-textbox-scheduled_online_activities"):
                        mdata["Scheduled online activities"] = data["2-textbox-scheduled_online_activities"].strip()
                    if data.get("2-textbox-practical_classes_and_workshops"):
                        mdata["Practical classes and workshops"] = data["2-textbox-practical_classes_and_workshops"].strip()
                    if data.get("2-textbox-supervised_laboratory_time"):
                        mdata["Supervised time in studio/laboratory/workshop"] = data["2-textbox-supervised_laboratory_time"].strip()
                    if data.get("2-textbox-fieldwork"):
                        mdata["Fieldwork"] = data["2-textbox-fieldwork"].strip()
                    if data.get("2-textbox-exernal_visits"):
                        mdata["External Visits"] = data["2-textbox-exernal_visits"].strip()
                    if data.get("2-textbox-work_based_learning"):
                        mdata["Work-based learning"] = data["2-textbox-work_based_learning"].strip()
                    if data.get("2-textbox-scheduled_examination_assessment"):
                        mdata["Scheduled Examination/Assessment"] = data["2-textbox-scheduled_examination_assessment"].strip()
                    if data.get("2-textbox-placement"):
                        mdata["Placement"] = data["2-textbox-placement"].strip()
                    if data.get("2-textbox-total_scheduled_teaching"):
                        mdata["Total Scheduled Teaching"] = data["2-textbox-total_scheduled_teaching"].strip()

                module_data.append(mdata)

        writer = csv.DictWriter(out, list(keys))
        writer.writeheader()
        writer.writerows(module_data)

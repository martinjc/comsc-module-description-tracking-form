import os
import csv
import subprocess

from lib.pdfdata import parse_fdf
from lib.handbookdata import get_module_list, TF_SUPPORT_FIELDS





if __name__ == "__main__":

    extract_dir = os.path.join(os.getcwd(), 'extracted')

    output_file = os.path.join(extract_dir, 'assessment-details.csv')

    with open(output_file, 'w') as out:

        modules = get_module_list('COMSC')

        description_folder = os.path.join(os.getcwd(), 'comparisons', 'module_leader-mjc')
        module_data = []
        keys = [
            "Module Code",
        ]
        keys.append("Assessment Title (MD)")
        keys.append("Assessment Type (MD)")
        keys.append("Assessment Contribution (MD)")
        keys.append("Assessment Date (MD)")

        keys.append("Assessment Title (TF)")
        keys.append("Assessment Type (TF)")
        keys.append("Assessment Contribution (TF)")
        keys.append("Assessment Duration (TF)")
        keys.append("Assessment Week Out (TF)")
        keys.append("Assessment Week In (TF)")
        keys.append("Assessment LO Coverage (TF)")

        for module in modules:

            mcode = module['moduleCode']

            if os.path.exists(os.path.join(description_folder, mcode)):
                print(mcode)



                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_tracking_form.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "tf_data.fdf"])
                subprocess.run(["pdftk", "comparisons/module_leader-mjc/%s/%s_module_description.pdf" % (mcode, mcode),  "dump_data_fields_utf8", "output", "md_data.fdf"])

                with open("md_data.fdf", 'r', encoding='utf-8') as md_data_input, open("tf_data.fdf", "r", encoding="utf-8") as tf_data_input:
                    md_data = parse_fdf(md_data_input)
                    tf_data = parse_fdf(tf_data_input)

                    for i in range(1,5):

                        mdata = {"Module Code": mcode}

                        if md_data.get("%d_assessment_title" % i):
                            mdata["Assessment Title (MD)"] = md_data["%d_assessment_title" % i].strip()
                        if md_data.get("%d_assessment_type" % i):
                            mdata["Assessment Type (MD)"] = md_data["%d_assessment_type" % i].strip()
                        if md_data.get("%d_assessment_contribution" % i):
                            mdata["Assessment Contribution (MD)"] = md_data["%d_assessment_contribution" %i].strip()
                        if md_data.get("%d_assessment_date" % i):
                            mdata["Assessment Date (MD)"] = md_data["%d_assessment_date" % i].strip()

                        if tf_data.get("4-textbox-assessment%d-title" % i):
                            mdata["Assessment Title (TF)"] = tf_data["4-textbox-assessment%d-title" % i].strip()
                        if tf_data.get("4-dropdown-assessment%d-type" % i):
                            mdata["Assessment Type (TF)"] = tf_data["4-dropdown-assessment%d-type" % i].strip()
                        if tf_data.get("4-textbox-assessment%d-weighting" % i):
                            mdata["Assessment Contribution (TF)"] = tf_data["4-textbox-assessment%d-weighting" % i].strip()
                        if tf_data.get("4-textbox-assessment%d-duration" % i):
                            mdata["Assessment Duration (TF)"] = tf_data["4-textbox-assessment%d-duration" % i].strip()
                        if tf_data.get("4-textbox-assessment%d-hand_out_week" % i):
                            mdata["Assessment Week Out (TF)"] = tf_data["4-textbox-assessment%d-hand_out_week" % i].strip()
                        if tf_data.get("4-textbox-assessment%d-hand_in_week" % i):
                            mdata["Assessment Week In (TF)"] = tf_data["4-textbox-assessment%d-hand_in_week" % i].strip()
                        if tf_data.get("4-textbox-assessment%d-learningoutcomes" % i):
                            mdata["Assessment LO Coverage (TF)"] = tf_data["4-textbox-assessment%d-learningoutcomes" % i].strip()

                        if mdata.get("Assessment Title (MD)"):
                            module_data.append(mdata)

        writer = csv.DictWriter(out, list(keys))
        writer.writeheader()
        writer.writerows(module_data)

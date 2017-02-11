from lib.handbookdata import *

def add_diff(diff_file, year_file):

    with open(year_file, 'a') as output_file, open(diff_file, 'r') as input_file:
        output_file.write(input_file.read())


if __name__ == "__main__":

    modules = get_module_list('COMSC')

    diff_folder = os.path.join(os.getcwd(), 'comparisons', 'diffs')

    for f in ['year1', 'year2', 'year3', 'msc', 'nsa_year1', 'nsa_year2', 'nsa_year3', 'msc_cmp', 'msc_cit', 'msc_dysa', 'msc_cdj', 'msc_isp', 'msc_acs']:

        if not os.path.exists(os.path.join(diff_folder, '%s_diff.html' % f)):
            open(os.path.join(diff_folder, '%s_diff.html' % f), 'w')

    for module in modules:

        mcode = module['moduleCode']

        if os.path.exists(os.path.join(diff_folder, mcode)):

            if mcode in YEAR1:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'year1_diff.html'))
            elif mcode in YEAR2:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'year2_diff.html'))
            elif mcode in YEAR3:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'year3_diff.html'))
            elif mcode in MSC:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_diff.html'))
                if mcode in PFMSADSA:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_acs_diff.html'))
                if mcode in PFMSCITA:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_cit_diff.html'))
                if mcode in PFMSCMPA:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_cmp_diff.html'))
                if mcode in PFMSDSYA:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_dysa_diff.html'))
                if mcode in PFMSISPA:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_isp_diff.html'))
                if mcode in PFMSCDJ:
                    add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'msc_cdj_diff.html'))
            elif mcode in NSA_YEAR1:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'nsa_year1_diff.html'))
            elif mcode in NSA_YEAR2:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'nsa_year2_diff.html'))
            elif mcode in NSA_YEAR3:
                add_diff(os.path.join(diff_folder, mcode, '%s_diff.html' % mcode), os.path.join(diff_folder, 'nsa_year3_diff.html'))

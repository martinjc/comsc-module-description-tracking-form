import os
import shutil

from tqdm import tqdm

from lib.handbookdata import get_module_list

SHARED_DRIVE_FOLDER = '/Volumes/shared/School Administration/Teaching Administration/2016-17/Module Description Review'
DIFF_FOLDER = os.path.join(os.getcwd(), 'comparisons', 'diffs-mjc')

modules = get_module_list('COMSC')

for module in tqdm(modules):

    mcode = module['moduleCode']

    if os.path.exists(os.path.join(DIFF_FOLDER, mcode)):

        shutil.copy(os.path.join(DIFF_FOLDER, mcode, '%s_diff.html' % mcode), os.path.join(SHARED_DRIVE_FOLDER, mcode))

import os

SHARED_FOLDER = "/Volumes/shared/School Administration/Teaching Administration/2016-17/Module Description Review/"

if __name__ == "__main__":

    module_folders = os.listdir(SHARED_FOLDER)
    for module_folder in module_folders:

        if os.path.isdir(os.path.join(SHARED_FOLDER, module_folder)):
            files = os.listdir(os.path.join(SHARED_FOLDER, module_folder))

            md_file = '%s_module_description.pdf' % module_folder
            tf_file = '%s_tracking_form.pdf' % module_folder

            files = [f for f in files if not f.startswith('.') and not f == 'Thumbs.db' ]

            if len(files) == 0:
                print(module_folder)
                print('no files')
            if len(files) == 2:
                if md_file not in files:
                    print('module description missing')
                if tf_file not in files:
                    print('tracking form missing')
            if len(files) > 2:
                print(files)
                print('too many files')

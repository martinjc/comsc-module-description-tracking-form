import os
import pandas

INPUT_DIR = os.path.join(os.getcwd(), 'src_data', 'feedback')

# where to put all the module feedback
OUTPUT_DIR = os.path.join(os.getcwd(), 'src_data', 'feedback', 'modules')

input_files = [
    'msc_autumn.csv',
    'msc_spring.csv',
    'yr1_autumn.csv',
    'yr2_autumn.csv',
    'yr3_autumn.csv',
    'yr1_spring.csv',
    'yr2_spring.csv',
    'yr3_spring.csv'
]

if __name__ == '__main__':

    for f in input_files:

        with open(os.path.join(INPUT_DIR, f), 'Ur') as data:
            print(f)
            feedback = pandas.read_csv(data)
            modules = feedback['Module'].unique()
            print(modules)
            for m in modules:
                print(m.split('/')[0])
                module_data = feedback.loc[feedback['Module'] == m].dropna(axis=1, how='all')

                with open(os.path.join(OUTPUT_DIR, '%s.csv' % m.split('/')[0]), 'w') as output_file:
                    module_data.to_csv(output_file)

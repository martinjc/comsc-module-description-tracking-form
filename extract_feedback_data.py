import os
import pandas

from urllib.parse import quote_plus
from matplotlib import pyplot as plt

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

non_plot_columns = [
    'Evaluation',
    'Module',
    'What did you particularly value about the module?',
    'How do you think the module could be improved?',
    'What proportion of the timetabled activities have you attended?',
    'On average, how many hours have you spent per week on this module, outside of the timetabled activities? Please note: there is no optimal answer for this question'
]

labels = {
    0: 'N/A',
    1: 'Definitely\nDisagree',
    2: 'Mostly\nDisagree',
    3: 'Neither Agree\nnor Disagree',
    4: 'Mostly\nAgree',
    5: 'Definitely\nAgree'
}

odd_plot_column_data = {
    'What proportion of the timetabled activities have you attended?': [
        '0-19%','20-39%','40-59%','60-79%','80-100%'
    ],
    'On average, how many hours have you spent per week on this module, outside of the timetabled activities? Please note: there is no optimal answer for this question': [
        '0', '1-3', '4-6', '7-9'
    ]
}


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

                for column in module_data.columns:
                    if not column in non_plot_columns:
                        fig = plt.figure()
                        bar_data = module_data[column].value_counts(sort=False)
                        column_labels = [0,1,2,3,4,5]
                        for c in column_labels:
                            if not c in bar_data.index:
                                bar_data.set_value(c, 0)
                        bar_data.sort_index(inplace=True)
                        bar_data.rename(labels, inplace=True)
                        ax = bar_data.plot.bar(alpha=0.5)
                        plt.ylabel('Number of Responses', fontsize=14)
                        plt.tight_layout()

                        fig.savefig(os.path.join(OUTPUT_DIR, quote_plus('%s-%s.png' % (m.split('/')[0], column[0:20].replace('/', '-').replace(':', '-').replace(',', '-').replace('(', '-').replace('(', '-').replace("'", "-")))))
                        plt.close()

                for column, column_labels in odd_plot_column_data.items():
                        fig = plt.figure()
                        bar_data = module_data[column].value_counts(sort=False)
                        for c in column_labels:
                            if not c in bar_data.index:
                                bar_data.set_value(c, 0)
                        bar_data.sort_index(inplace=True)
                        bar_data.plot.bar(alpha=0.5)
                        plt.ylabel('Number of Responses', fontsize=14)
                        plt.tight_layout()
                        fig.savefig(os.path.join(OUTPUT_DIR, quote_plus('%s-%s.png' % (m.split('/')[0], column[0:20].replace('/', '-').replace(':', '-').replace(',', '-').replace('(', '-').replace('(', '-').replace("'", "-")))))
                        plt.close()

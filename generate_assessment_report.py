import os

import pandas as pd
import seaborn as sns
import matplotlib as mpl

from weasyprint import HTML
from scipy.stats import pearsonr
from urllib.parse import quote_plus
from collections import defaultdict
from matplotlib import pyplot as plt
from jinja2 import Environment, FileSystemLoader

from lib.handbookdata import *

inline_rc = dict(mpl.rcParams)
plt.style.use('seaborn-muted')

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

TEMPLATE_PATH = os.path.join(os.getcwd(), 'templates')
TEMPLATE_ENVIRONMENT = Environment(autoescape=False, loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=False)
ASSESSMENT_RESULTS = os.path.join(os.getcwd(), 'src_data', 'assessment.csv')
MARK_COLUMN = 'Assessments (SAS).Agreed Mark'
DATA_OUTPUT_DIR = os.path.join(os.getcwd(), 'src_data', 'feedback', 'modules')
OUTPUT_DIR = os.path.join(os.getcwd(), 'dist')

a_d = pd.read_csv(ASSESSMENT_RESULTS, encoding='utf-8')
a_d_results = a_d.drop(['Student Number', 'Name', 'Study Programme', 'Level Code', 'Final Assessment Date (SMRS)', 'Current Process (SAS)', 'Period'], 1)
module_list = a_d['Module Code'].unique()

for module in module_list:
#for module in ['CMT112']:

    print(module)
    context = {'module': {'title': module}}

    module_data = a_d.loc[a_d['Module Code'] == module]
    module_data_by_student = module_data.groupby('Student Number')

    module_data_by_year = module_data.groupby('Academic Year')

    if '2015/6' in module_data_by_year.groups:

        combined_marks = module_data_by_year.get_group('2015/6')[['Student Number', 'Module Agreed Mark']].drop_duplicates()
        combined_marks.set_index(['Student Number'], inplace=True)

        assessment_data = module_data_by_year.get_group('2015/6').groupby(['Assessment Type', 'Percentage', 'Sequence'])
        assessments = assessment_data.groups.keys()

        for y, assessment in enumerate(assessments):
            assessment_marks = assessment_data.get_group(assessment)[['Student Number', MARK_COLUMN]]
            assessment_marks.columns = ['Student Number', assessment]
            assessment_marks.set_index(['Student Number'], inplace=True)
            combined_marks['%s - %s%% - %s' % (assessment[0], assessment[1], assessment[2])] = assessment_marks

        average_marks = a_d.loc[a_d['Module Code'] != module]
        average_marks = average_marks.loc[average_marks['Student Number'].isin(combined_marks.index)]
        average_marks_by_student = average_marks.groupby('Student Number')
        average_marks_by_student = pd.DataFrame({'Student Average': average_marks_by_student['Module Agreed Mark'].mean()})
        combined_marks['Student Average'] = average_marks_by_student['Student Average']
        combined_marks.dropna(inplace=True)
        column_labels = ['%s - %s%% - %s' % (assessment[0], assessment[1], assessment[2]) for assessment in assessments] + ['Module Agreed Mark', 'Student Average']
        combined_marks = combined_marks[column_labels]

        correlation_coeffs = pd.DataFrame(columns=column_labels, index=column_labels)
        context['correlations'] = {}
        context['correlations']['columns'] = combined_marks.columns
        for col1 in combined_marks.columns:
            context['correlations'][col1] = {}
            for col2 in combined_marks.columns:
                r, p = pearsonr(combined_marks[col1], combined_marks[col2])
                if col1 != col2:
                    if p < 0.5:
                        value = '<strong>r: %.2f, <br> p: %.2e</strong>' % (r, p)
                    else:
                        value = 'r: %.2f, <br> p: %.2e' % (r, p)
                else:
                    value = ''
                context['correlations'][col1][col2] = value
                correlation_coeffs[col1][col2] = (r, p)

        fpath = os.path.join(DATA_OUTPUT_DIR, '%s-correlations.csv' % module)
        correlation_coeffs.to_csv(fpath)

        if not combined_marks.empty:
            g = sns.pairplot(combined_marks, kind="reg")
            g.set(ylim=(-5,105))
            g.set(xlim=(-5,105))
            plot_path = os.path.join(DATA_OUTPUT_DIR, '%s-comparison.png' % module)
            context['comparison_image'] = 'file://' + plot_path
            plt.savefig(plot_path, bbox_inches='tight', facecolor='w', frameon=True)

        html = render_template('module_assessment_template.html', context)
        if not os.path.exists(os.path.join(OUTPUT_DIR, module)):
            os.makedirs(os.path.join(OUTPUT_DIR, module))
        HTML(string=html).write_pdf(os.path.join(OUTPUT_DIR, module, 'assessment_report.pdf'))

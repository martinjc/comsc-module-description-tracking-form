import os
import pandas

from weasyprint import HTML
from urllib.parse import quote_plus
from jinja2 import Environment, FileSystemLoader

from lib.handbookdata import *

TEMPLATE_PATH = os.path.join(os.getcwd(), 'templates')
TEMPLATE_ENVIRONMENT = Environment(autoescape=False, loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

DATA_FILES_DIR = os.path.join('src_data', 'feedback', 'modules')

OUTPUT_DIR = os.path.join(os.getcwd(), 'dist')

non_plot_columns = [
    'Unnamed: 0',
    'Evaluation',
    'Module',
    'What did you particularly value about the module?',
    'How do you think the module could be improved?',
    'What proportion of the timetabled activities have you attended?',
    'On average, how many hours have you spent per week on this module, outside of the timetabled activities? Please note: there is no optimal answer for this question'
]

# get the list of modules for the school
modules = get_module_list('COMSC')
for module in modules:
    mcode = module['moduleCode']
    print(mcode)
    context = {'module': {'title': mcode}}

    if os.path.exists(os.path.join(DATA_FILES_DIR, '%s.csv' % (mcode))):
        with open(os.path.join(DATA_FILES_DIR, '%s.csv' % (mcode)), 'r') as data_file:
            feedback_data = pandas.read_csv(data_file)
            columns = feedback_data.columns

            context['charts'] = []

            context['value'] = []
            context['improve'] = []

            if 'What did you particularly value about the module?' in feedback_data.columns:
                valued = feedback_data['What did you particularly value about the module?']
                for comment in valued.dropna():
                    context['value'].append(comment)

            if 'How do you think the module could be improved?' in feedback_data.columns:
                improved = feedback_data['How do you think the module could be improved?']
                for comment in improved.dropna():
                    context['improve'].append(comment)

            images_file_dir = os.path.join(os.getcwd(), DATA_FILES_DIR)
            for column in columns:
                if not column in non_plot_columns:
                    context['charts'].append({
                        'title': column,
                        'image': 'file://' + os.path.join(images_file_dir, quote_plus('%s-%s.png' % (mcode, column[0:20].replace('/', '-').replace(':', '-').replace(',', '-').replace('(', '-').replace('(', '-').replace("'", "-"))))
                    })

            html = render_template('module_feedback_template.html', context)
            HTML(string=html).write_pdf(os.path.join(OUTPUT_DIR, mcode, 'feedback_report.pdf'))

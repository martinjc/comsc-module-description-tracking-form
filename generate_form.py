import os

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

TEMPLATE_PATH = os.path.join(os.getcwd(), 'form', 'templates')
TEMPLATE_ENVIRONMENT = Environment(autoescape=False, loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=False)

def render_template(template_fname, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_fname).render(context)

context = {}

out_path = os.path.join(os.getcwd(), 'dist', 'output.html')
with open(out_path, 'w') as f:
    html = render_template('module-description-tracking-form--template.html', context)
    f.write(html)
    HTML(string=html).write_pdf(os.path.join(os.getcwd(), 'dist','output.pdf'))

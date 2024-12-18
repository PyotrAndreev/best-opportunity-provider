from jinja2 import Template
import codecs


TEMPLATES_PATH = 'DBL/templates/'
CARD_TEMPLATE_FNAME = 'card.md'


def render_card(opportunity_info):
    with open(f'{TEMPLATES_PATH}{CARD_TEMPLATE_FNAME}', 'r') as file:
        template = Template(file.read(), trim_blocks=True)
    return template.render(opp=opportunity_info)


def save_md(opportunity_info, output_fname):
    """
    Renders a markdown file for a given opportunity and saves it to a specified output file.

    This function uses the `render_card` function to render the opportunity information into a markdown file.
    It then saves the rendered content to a file with the specified `output_fname`.

    Args:
        opportunity_info (dict): A dictionary containing information about the opportunity that will be rendered
                                  into the template.
        output_fname (str): The name of the output file where the rendered markdown will be saved.
    """

    rendered_file = render_card(opportunity_info)
    output_file = codecs.open(output_fname, 'w', 'utf-8')
    output_file.write(rendered_file)
    output_file.close()

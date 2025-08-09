import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

templates_dir = os.path.dirname(__file__)

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"])
)

def render_email_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)

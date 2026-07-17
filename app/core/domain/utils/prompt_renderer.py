from dataclasses import asdict
from app.core.domain.models.turn_context import TurnContext
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
jinja_env = Environment(loader=FileSystemLoader(PROMPTS_DIR))


def render_template(template_name: str, context:TurnContext) -> str:
    """Helper to load and render templates from the prompts directory."""
    template = jinja_env.get_template(template_name)
    return template.render(**asdict(context))
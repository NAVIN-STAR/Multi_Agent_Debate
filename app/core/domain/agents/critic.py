from app.core.domain.agents.base import Agent
from app.core.domain.models.turn_context import TurnContext
from app.core.domain.utils.prompt_renderer import render_template

class Critic(Agent):
    def build_prompt(self,context:TurnContext) -> str:
        return render_template("critic_prompt.j2",context=context)
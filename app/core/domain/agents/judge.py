from app.core.domain.agents.base import Agent
from app.core.domain.models.turn_context import TurnContext
from app.core.domain.utils.prompt_renderer import render_template


class Judge(Agent):


    @property
    def name(self)->str:
        return "judge"

    def build_prompt(self,turn_context:TurnContext) -> str:
        return render_template("judge_prompt.j2",context=turn_context)

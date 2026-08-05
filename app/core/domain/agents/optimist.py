from app.core.domain.agents.base import Agent
from app.core.domain.models.models import Speaker, TurnContext
from app.core.domain.utils.prompt_renderer import render_template


class Optimist(Agent):

    @property
    def name(self)->Speaker:
        return Speaker.OPTIMIST

    
    def build_prompt(self,turn_context:TurnContext) -> str:
        return render_template("optimist_prompt.j2",context=turn_context)
        

        

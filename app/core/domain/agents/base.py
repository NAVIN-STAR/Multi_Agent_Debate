from abc import ABC, abstractmethod

from app.core.domain.models.turn_context import TurnContext
from app.core.domain.ports.llm_port import LLMPort


class Agent(ABC):
    def __init__(self,llm:LLMPort) -> None:
        self.llm=llm
        super().__init__()


    @property
    @abstractmethod
    def name(self) -> str:
        ...

    async def take_turn(self,turn_context:TurnContext):
        prompt = self.build_prompt(turn_context)
        response = await self.llm.generate(prompt)
        self.validate_response(response) #Needs implementation
        return self.parse_response(response)# Needs Implementation


    @abstractmethod
    def build_prompt(self,turn_context:TurnContext) -> str:
        ...
    

    def validate_response(self,response:str):
        if not response.strip():
            raise ValueError("LLM returned an empty response.")

    def parse_response(self,response: str):
        return response


from dataclasses import field
from dataclasses import dataclass


@dataclass
class DebateMessage:
    speaker: str
    content: str

@dataclass
class TurnContext:
    topic:str
    history: list[DebateMessage] = field(default_factory=list)
    round_number:int=1
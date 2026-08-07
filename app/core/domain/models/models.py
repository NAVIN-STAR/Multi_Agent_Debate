from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict


#Holds current turn of a speaker and its response
@dataclass
class DebateMessage:
    speaker: Speaker
    content: str

#Context known to each agent
@dataclass
class TurnContext:
    topic: str
    history: list[DebateMessage] = field(default_factory=list)
    round_number: int = 1
    

class Speaker(Enum):
    OPTIMIST = "optimist"
    CRITIC = "critic"
    JUDGE = "judge"

#Memory state for Langraph nodes to decide which node to invoke next
class DebateState(TypedDict):
    turn_context: TurnContext
    current_speaker: Speaker
    verdict: str | None
    max_rounds:int



    

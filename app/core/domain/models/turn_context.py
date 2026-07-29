from dataclasses import dataclass, field
from typing import TypedDict


#Holds current turn of a speaker and its response
@dataclass
class DebateMessage:
    speaker: str
    content: str

#Context known to each agent
@dataclass
class TurnContext:
    topic: str
    history: list[DebateMessage] = field(default_factory=list)
    round_number: int = 1

#Memory state for Langraph nodes to decide which node to invoke next
class DebateState(TypedDict):
    turn_context: TurnContext
    verdict: str | None

from dataclasses import dataclass
from enum import Enum

from app.core.domain.models.models import Speaker


class DebateEventType(Enum):
    STARTED="started"
    RESPONSE = "response"
    FINISHED = "finished"


@dataclass
class DebateEvent:
    round_number: int
    speaker: Speaker
    content: str
    event_type:DebateEventType
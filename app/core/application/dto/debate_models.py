from dataclasses import dataclass

from app.core.domain.models.models import DebateMessage, Speaker


@dataclass
class DebateRequest:
    topic: str
    max_rounds: int = 2

@dataclass
class DebateResponse:
    topic:str
    history:list[DebateMessage]
    verdict:str|None


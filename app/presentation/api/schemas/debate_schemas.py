from pydantic import BaseModel


class DebateRequestSchema(BaseModel):
    topic:str
    max_rounds:int=2

class DebateMessageSchema(BaseModel):
    speaker: str
    content: str

class DebateResponseSchema(BaseModel):
    topic:str
    history:list[DebateMessageSchema]
    verdict:str|None

class DebateEventSchema(BaseModel):
    round_number: int
    speaker: str
    content: str
    event_type:str
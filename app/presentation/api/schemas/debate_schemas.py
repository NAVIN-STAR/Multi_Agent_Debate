from pydantic import BaseModel, Field, field_validator


class DebateRequestSchema(BaseModel):
    topic: str = Field(..., min_length=1)
    max_rounds: int = Field(default=2, ge=1, le=10)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Topic cannot be empty")

        return value

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
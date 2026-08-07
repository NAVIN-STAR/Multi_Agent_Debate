from app.core.application.dto.debate_models import DebateRequest, DebateResponse
from app.presentation.api.schemas.debate_schemas import (
    DebateMessageSchema,
    DebateRequestSchema,
    DebateResponseSchema,
)


def workflow_response_to_api_response(
    response: DebateResponse,
) -> DebateResponseSchema:
    return DebateResponseSchema(
        topic=response.topic,
        verdict=response.verdict,
        history=[
            DebateMessageSchema(
                speaker=message.speaker.value,
                content=message.content,
            )
            for message in response.history
        ],
    )




def api_request_to_workflow_request(
    request: DebateRequestSchema,
) -> DebateRequest:
    return DebateRequest(
        topic=request.topic,
        max_rounds=request.max_rounds,
    )
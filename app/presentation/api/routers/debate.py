from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.presentation.api.dependencies import get_workflow
from app.presentation.api.mappers.api_mapper import (
    api_request_to_workflow_request,
    workflow_event_to_api_event,
    workflow_response_to_api_response,
)
from app.presentation.api.schemas.debate_schemas import (
    DebateRequestSchema,
    DebateResponseSchema,
)

router=APIRouter(
    prefix="/debates",
    tags=["Debates"],
)

@router.post('/',response_model=DebateResponseSchema)
async def debate(
    request: DebateRequestSchema,
    workflow: DebateWorkflow = Depends(get_workflow),  # noqa: B008
): 
    response = await workflow.run(
        api_request_to_workflow_request(request)
    )
    return workflow_response_to_api_response(response)


@router.post('/stream')
async def stream_debate(
    request: DebateRequestSchema,
    workflow: DebateWorkflow = Depends(get_workflow),  # noqa: B008
): 
    workflow_request = api_request_to_workflow_request(request)

    async def event_generator():
        async for event in workflow.stream(workflow_request):
            api_event = workflow_event_to_api_event(event)

            yield f"data: {api_event.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

    
    
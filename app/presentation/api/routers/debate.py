from fastapi import APIRouter, Depends

from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.presentation.api.dependencies import get_workflow
from app.presentation.api.mappers.api_mapper import (
    api_request_to_workflow_request,
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


    
    
from fastapi import Depends

from app.core.adapters.GroqAdapter import GroqAdapter
from app.core.application.workflows.debate.workflow import DebateWorkflow
from app.core.domain.ports.llm_port import LLMPort


def get_llm()-> LLMPort:
    return GroqAdapter()


def get_workflow(llm:LLMPort=Depends(get_llm))->DebateWorkflow:
    return DebateWorkflow(llm)
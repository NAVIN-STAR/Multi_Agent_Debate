from fastapi import FastAPI

from app.presentation.api.routers.debate import router as debate_router

app = FastAPI(
    title="Multi-Agent Debate API",
    description="Production-grade multi-agent debate system built with LangGraph.",
    version="1.0.0",
)

app.include_router(router=debate_router)
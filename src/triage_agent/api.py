"""Local HTTP transport; all triage decisions belong to the shared agent."""

from fastapi import FastAPI, HTTPException

from triage_agent.agent import triage_batch
from triage_agent.config import ConfigurationError
from triage_agent.knowledge.database import KnowledgeError
from triage_agent.schemas import Ticket

app = FastAPI(title="Support Ticket Triage Prototype")


@app.get("/health")
def health() -> dict:
    return {"status": "alive"}


@app.post("/triage")
def triage(payload: Ticket | list[Ticket]) -> dict:
    try:
        return triage_batch(payload)
    except (ConfigurationError, KnowledgeError):
        raise HTTPException(503, "Runtime configuration unavailable.") from None
    except (ValueError, TypeError):
        raise HTTPException(422, "Invalid ticket batch.") from None

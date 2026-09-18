from pydantic import BaseModel
from typing import Any, Optional


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    status: str
    question: str
    corrected_question: Optional[str] = None
    intent: Optional[str] = None
    sql: Optional[str] = None
    results: Optional[list[dict[str, Any]]] = None
    clarification_question: Optional[str] = None
    message: Optional[str] = None
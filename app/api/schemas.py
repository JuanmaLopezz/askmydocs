from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentResponse(BaseModel):
    id: str
    filename: str
    chunks: int
    uploaded_at: datetime


class QueryRequest(BaseModel):
    question: str
    top_k: int = 4


class Source(BaseModel):
    document: str
    page: Optional[int]
    chunk: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]

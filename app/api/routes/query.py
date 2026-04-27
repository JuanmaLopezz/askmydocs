from fastapi import APIRouter, HTTPException
from app.api.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def ask_question(request: QueryRequest) -> QueryResponse:
    """Ask a question against indexed documents."""
    # TODO: Fase B — implement RAG chain
    raise HTTPException(status_code=501, detail="Fase B pendiente de implementación")

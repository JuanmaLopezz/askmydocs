from fastapi import APIRouter, HTTPException
from app.api.schemas import QueryRequest, QueryResponse
from app.retrieval.chain import run_query

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def ask_question(request: QueryRequest) -> QueryResponse:
    try:
        return run_query(request.question, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

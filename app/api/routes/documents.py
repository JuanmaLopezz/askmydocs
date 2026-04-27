from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schemas import DocumentResponse

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    """Upload and index a document into ChromaDB."""
    # TODO: Fase A — implement ingestion pipeline
    raise HTTPException(status_code=501, detail="Fase A pendiente de implementación")


@router.get("/", response_model=list[DocumentResponse])
async def list_documents() -> list[DocumentResponse]:
    """List all indexed documents."""
    # TODO: Fase C — implement
    raise HTTPException(status_code=501, detail="Fase C pendiente de implementación")


@router.delete("/{document_id}")
async def delete_document(document_id: str) -> dict:
    """Delete a document and its chunks from ChromaDB."""
    # TODO: Fase C — implement
    raise HTTPException(status_code=501, detail="Fase C pendiente de implementación")

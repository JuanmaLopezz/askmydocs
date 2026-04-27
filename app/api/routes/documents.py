import uuid
import tempfile
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schemas import DocumentResponse
from app.config import settings
from app.ingestion.loaders import load_document
from app.ingestion.chunker import chunk_documents
from app.ingestion.embeddings import embed_and_store, delete_by_document_id
from app.storage import registry

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in settings.supported_extensions_list:
        raise HTTPException(status_code=400, detail=f"Extension .{ext} not supported")

    if file.size and file.size > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds max size")

    doc_id = str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        documents = load_document(tmp_path)
        for doc in documents:
            doc.metadata["document_id"] = doc_id
            doc.metadata["filename"] = file.filename
        chunks = chunk_documents(documents)
        chunk_count = embed_and_store(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        tmp_path.unlink(missing_ok=True)

    return registry.register(doc_id, file.filename, chunk_count)


@router.get("/", response_model=list[DocumentResponse])
async def list_documents() -> list[DocumentResponse]:
    return registry.list_all()


@router.delete("/{document_id}", status_code=200)
async def delete_document(document_id: str) -> dict:
    if not registry.exists(document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    delete_by_document_id(document_id)
    registry.remove(document_id)
    return {"deleted": document_id}

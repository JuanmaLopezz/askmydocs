import json
from pathlib import Path
from datetime import datetime, timezone
from app.api.schemas import DocumentResponse

REGISTRY_PATH = Path("./data/documents.json")


def _load() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, default=str, indent=2), encoding="utf-8")


def register(doc_id: str, filename: str, chunks: int) -> DocumentResponse:
    data = _load()
    uploaded_at = datetime.now(timezone.utc).isoformat()
    data[doc_id] = {"id": doc_id, "filename": filename, "chunks": chunks, "uploaded_at": uploaded_at}
    _save(data)
    return DocumentResponse(**data[doc_id])


def list_all() -> list[DocumentResponse]:
    return [DocumentResponse(**v) for v in _load().values()]


def remove(doc_id: str) -> bool:
    data = _load()
    if doc_id not in data:
        return False
    del data[doc_id]
    _save(data)
    return True


def exists(doc_id: str) -> bool:
    return doc_id in _load()

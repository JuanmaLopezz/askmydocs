import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_unsupported_extension():
    response = client.post(
        "/documents/upload",
        files={"file": ("data.csv", b"a,b,c", "text/csv")},
    )
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]


def test_upload_txt():
    content = b"Este es un documento de prueba con contenido suficiente para indexar."
    with patch("app.api.routes.documents.embed_and_store", return_value=3), \
         patch("app.api.routes.documents.registry.register") as mock_reg:
        from app.api.schemas import DocumentResponse
        from datetime import datetime, timezone
        mock_reg.return_value = DocumentResponse(
            id="test-id", filename="test.txt", chunks=3,
            uploaded_at=datetime.now(timezone.utc)
        )
        response = client.post(
            "/documents/upload",
            files={"file": ("test.txt", content, "text/plain")},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "test.txt"
    assert body["chunks"] == 3


def test_list_documents_empty():
    with patch("app.api.routes.documents.registry.list_all", return_value=[]):
        response = client.get("/documents/")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_document_not_found():
    with patch("app.api.routes.documents.registry.exists", return_value=False):
        response = client.delete("/documents/nonexistent-id")
    assert response.status_code == 404


def test_delete_document_ok():
    with patch("app.api.routes.documents.registry.exists", return_value=True), \
         patch("app.api.routes.documents.delete_by_document_id"), \
         patch("app.api.routes.documents.registry.remove"):
        response = client.delete("/documents/some-doc-id")
    assert response.status_code == 200
    assert response.json()["deleted"] == "some-doc-id"


def test_query_endpoint():
    from app.api.schemas import QueryResponse, Source
    mock_response = QueryResponse(
        answer="El documento habla sobre X.",
        sources=[Source(document="test.pdf", page=1, chunk="contenido relevante")]
    )
    with patch("app.api.routes.query.run_query", return_value=mock_response):
        response = client.post("/query/", json={"question": "¿De qué trata el documento?", "top_k": 4})
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert len(body["sources"]) == 1

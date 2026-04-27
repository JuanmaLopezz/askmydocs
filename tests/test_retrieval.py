import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from app.api.schemas import QueryResponse


def test_format_docs_with_page():
    from app.retrieval.chain import _format_docs
    docs = [
        Document(page_content="Texto del chunk.", metadata={"filename": "doc.pdf", "page": 2}),
    ]
    result = _format_docs(docs)
    assert "doc.pdf" in result
    assert "p.3" in result
    assert "Texto del chunk." in result


def test_format_docs_no_page():
    from app.retrieval.chain import _format_docs
    docs = [
        Document(page_content="Contenido sin página.", metadata={"filename": "doc.txt"}),
    ]
    result = _format_docs(docs)
    assert "doc.txt" in result
    assert "Contenido sin página." in result


def test_run_query_returns_response():
    mock_docs = [
        Document(
            page_content="El producto cuesta 100 euros.",
            metadata={"filename": "catalogo.pdf", "page": 0, "document_id": "abc"}
        )
    ]
    mock_answer = "El producto cuesta 100 euros. [catalogo.pdf, p.1]"

    with patch("app.retrieval.chain.get_retriever") as mock_retriever, \
         patch("app.retrieval.chain.ChatAnthropic") as mock_llm_class:
        mock_ret = MagicMock()
        mock_ret.invoke.return_value = mock_docs
        mock_retriever.return_value = mock_ret

        mock_chain_result = MagicMock()
        mock_chain_result.__or__ = MagicMock(return_value=mock_chain_result)
        mock_llm_instance = MagicMock()
        mock_llm_class.return_value = mock_llm_instance

        with patch("app.retrieval.chain.RAG_PROMPT") as mock_prompt, \
             patch("app.retrieval.chain.StrOutputParser") as mock_parser:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = mock_answer
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_chain.__or__ = MagicMock(return_value=mock_chain)

            from app.retrieval.chain import run_query
            result = run_query("¿Cuánto cuesta el producto?")

        assert isinstance(result, QueryResponse)

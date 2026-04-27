from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from app.api.schemas import QueryResponse, Source
from app.config import settings
from app.ingestion.embeddings import COLLECTION_NAME
from app.observability.tracing import get_langfuse_callback
from app.retrieval.prompts import RAG_PROMPT, NO_INFO_PHRASE
from app.retrieval.retriever import get_retriever


def _format_docs(docs) -> str:
    parts = []
    for doc in docs:
        meta = doc.metadata
        filename = meta.get("filename", meta.get("source", "unknown"))
        page = meta.get("page", "")
        page_info = f" (p.{page + 1})" if page != "" else ""
        parts.append(f"[{filename}{page_info}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def run_query(question: str, collection_name: str = COLLECTION_NAME, top_k: int = 4) -> QueryResponse:
    retriever = get_retriever(collection_name, top_k)
    docs = retriever.invoke(question)

    llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=settings.anthropic_api_key)
    chain = RAG_PROMPT | llm | StrOutputParser()
    callback = get_langfuse_callback()
    invoke_cfg = {"callbacks": [callback], "run_name": "rag-query"} if callback else {}
    answer = chain.invoke({"context": _format_docs(docs), "question": question}, config=invoke_cfg)

    if NO_INFO_PHRASE in answer:
        return QueryResponse(answer=NO_INFO_PHRASE, sources=[])

    sources = []
    seen: set = set()
    for doc in docs:
        meta = doc.metadata
        filename = meta.get("filename", meta.get("source", "unknown"))
        page = meta.get("page")
        key = (filename, page)
        if key not in seen:
            seen.add(key)
            sources.append(Source(
                document=filename,
                page=(page + 1) if page is not None else None,
                chunk=doc.page_content[:200],
            ))

    return QueryResponse(answer=answer, sources=sources)

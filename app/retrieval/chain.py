from app.api.schemas import QueryResponse


def build_rag_chain(collection_name: str, top_k: int = 4):
    """Build the full RAG chain: retriever + prompt + LLM."""
    # TODO: Fase B — implement LangChain RAG chain
    raise NotImplementedError("Fase B pendiente")


def run_query(question: str, collection_name: str = "default") -> QueryResponse:
    """Run a question through the RAG chain and return answer with sources."""
    # TODO: Fase B — implement
    raise NotImplementedError("Fase B pendiente")

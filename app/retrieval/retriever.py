from langchain_core.vectorstores import VectorStoreRetriever
from app.ingestion.embeddings import get_vectorstore, COLLECTION_NAME


def get_retriever(collection_name: str = COLLECTION_NAME, top_k: int = 4) -> VectorStoreRetriever:
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": top_k})

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

COLLECTION_NAME = "documents"

_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=_embeddings,
        persist_directory=settings.chroma_persist_path,
    )


def embed_and_store(chunks: list[Document], collection_name: str = COLLECTION_NAME) -> int:
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=_embeddings,
        persist_directory=settings.chroma_persist_path,
    )
    vectorstore.add_documents(chunks)
    return len(chunks)

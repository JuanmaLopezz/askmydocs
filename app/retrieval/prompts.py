from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are a document assistant. Answer the question using ONLY the provided context.
Always cite the exact source (document name and page number).
If the answer is not in the context, say: "No encontré información sobre esto en los documentos disponibles."

Context:
{context}

Question: {question}

Answer (with source citation):"""
)

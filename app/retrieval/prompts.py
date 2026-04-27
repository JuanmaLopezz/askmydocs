from langchain_core.prompts import ChatPromptTemplate

NO_INFO_PHRASE = "No encontré información sobre esto en los documentos disponibles."

RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are a document assistant. Answer the question using ONLY the provided context.
Always cite the exact source (document name and page number).
If the answer is not clearly present in the context, respond ONLY with this exact sentence and nothing else:
"No encontré información sobre esto en los documentos disponibles."
Do NOT mention document names, do NOT add explanations, do NOT reference what the documents are about.

Context:
{context}

Question: {question}

Answer (with source citation):"""
)

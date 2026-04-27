from fastapi import FastAPI
from app.api.routes import documents, query

app = FastAPI(
    title="AskMyDocs",
    description="Inteligencia documental universal — pregunta a tus documentos",
    version="0.1.0",
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(query.router, prefix="/query", tags=["query"])


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

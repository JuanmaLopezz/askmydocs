# AskMyDocs

Sube cualquier documento (PDF, Word, Excel, TXT) y hazle preguntas en lenguaje natural. Respuestas precisas con la fuente exacta citada — página incluida.

Proyecto portfolio de Data AI Engineering. Demuestra un stack RAG completo en producción.

---

## Demo

**Subir documento → preguntar → respuesta con fuente citada**

```
POST /documents/upload  →  { "id": "...", "filename": "informe.pdf", "chunks": 6 }
POST /query             →  { "answer": "La facturación fue 487.320 EUR [informe.pdf, p.1]",
                             "sources": [{ "document": "informe.pdf", "page": 1, "chunk": "..." }] }
```

---

## Stack técnico

| Capa | Tecnología |
|------|------------|
| LLM | Claude Sonnet (Anthropic API) |
| Orquestación | LangChain 0.3 + LCEL |
| Vector store | ChromaDB (local, persistente) |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace, local) |
| API | FastAPI + Pydantic v2 |
| Observabilidad | LangFuse v3 (tokens, coste, latencia por query) |
| UI | Streamlit |
| Infra | Docker + docker-compose |

---

## Arquitectura RAG

```
Documento (PDF/DOCX/XLSX/TXT)
    │
    ▼
Loaders (LangChain)  →  Chunker (1000 tokens, overlap 200)
    │
    ▼
Embeddings (all-MiniLM-L6-v2)  →  ChromaDB (persistente en ./data/chroma)
    │
    ▼
Query  →  Retriever (top-k semántico)  →  Prompt  →  Claude  →  Respuesta + Fuentes
                                                          │
                                                          ▼
                                                    LangFuse (traza completa)
```

---

## Instalación local

**Requisitos:** Python 3.9+, API key de Anthropic

```bash
git clone https://github.com/JuanmaLopezz/askmydocs.git
cd askmydocs

cp .env.example .env
# Añadir ANTHROPIC_API_KEY en .env
# (Opcional) Añadir LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY para observabilidad

pip install -r requirements.txt

# Terminal 1 — API
uvicorn app.main:app --reload

# Terminal 2 — UI
streamlit run app/ui/streamlit_app.py
```

- API + Swagger: http://localhost:8000/docs
- UI: http://localhost:8501

---

## Docker

```bash
docker-compose up --build
```

- API: http://localhost:8000/docs
- UI: http://localhost:8501

---

## Tests

```bash
pytest tests/ -v
# 15/15 passing
```

---

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health` | Estado de la API |
| `POST` | `/documents/upload` | Subir e indexar documento |
| `GET` | `/documents/` | Listar documentos indexados |
| `DELETE` | `/documents/{id}` | Eliminar documento y sus chunks |
| `POST` | `/query` | Preguntar sobre los documentos |

---

## Estructura

```
app/
├── api/routes/        # Endpoints FastAPI
├── ingestion/         # Loaders, chunker, embeddings
├── retrieval/         # Retriever, prompt, cadena RAG
├── observability/     # LangFuse tracing
├── storage/           # Registry de documentos (JSON)
└── ui/                # Streamlit app
tests/                 # 15 tests unitarios
docs/                  # Roadmap, arquitectura, batería de pruebas
```

---

## Fases completadas

- ✅ Fase A — Ingestión (PDF, DOCX, XLSX, TXT → ChromaDB)
- ✅ Fase B — Motor RAG (retrieval semántico + Claude + fuentes citadas)
- ✅ Fase C — API REST completa (CRUD documentos + queries)
- ✅ Fase D — Observabilidad LangFuse (tokens, coste, latencia por query)
- ✅ Fase E — UI Streamlit + Docker

---

## Autor

**Juanma López** — [GitHub](https://github.com/JuanmaLopezz) · [LinkedIn](https://linkedin.com/in/juanmalopez)

Data AI Engineer en construcción. Este proyecto es parte de mi portfolio de transición hacia roles de AI Engineering.

---

## Licencia

MIT

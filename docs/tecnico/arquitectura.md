# Arquitectura técnica — AskMyDocs

## Diagrama de flujo

```
[Usuario]
    │
    ├─── POST /documents/upload ──→ [Loaders] ──→ [Chunker] ──→ [Embeddings] ──→ [ChromaDB]
    │
    └─── POST /query ──────────→ [Retriever] ──→ [RAG Chain] ──→ [Claude API] ──→ Respuesta
                                      │               │
                                 [ChromaDB]      [LangFuse]
                                 (búsqueda        (trazas)
                                 semántica)
```

## Componentes principales

### Ingestion Pipeline (Fase A)
- **Qué hace:** Carga, trocea e indexa documentos
- **Tecnología:** LangChain document loaders + RecursiveCharacterTextSplitter
- **Entrada:** Archivo (PDF/DOCX/XLSX/TXT)
- **Salida:** Chunks con embeddings persistidos en ChromaDB

### Retrieval + RAG Chain (Fase B)
- **Qué hace:** Recupera contexto relevante y genera respuesta con cita
- **Tecnología:** ChromaDB retriever + LangChain RetrievalQA + Claude API
- **Entrada:** Pregunta en lenguaje natural
- **Salida:** Respuesta + fuente (documento + página)

### FastAPI (Fase C)
- **Qué hace:** Expone funcionalidad como API REST
- **Tecnología:** FastAPI + Pydantic
- **Endpoints principales:** POST /documents/upload, POST /query, GET /documents, DELETE /documents/{id}

### Observabilidad (Fase D)
- **Qué hace:** Traza cada consulta con métricas completas
- **Tecnología:** LangFuse via LangChain callback
- **Captura:** input, output, tokens, latencia, modelo

### Streamlit UI (Fase E)
- **Qué hace:** Interfaz para usuarios no técnicos
- **Tecnología:** Streamlit
- **Funciones:** subir documentos, hacer preguntas, ver fuentes

## Decisiones de arquitectura
Ver: `.claude/memory/decisions.md`

## Puntos de extensión futuros
- Swap ChromaDB → Pinecone para escala mayor
- Swap Claude → cualquier LangChain-compatible LLM
- Auth layer (FastAPI middleware) sin tocar lógica de negocio
- Multi-tenant por colecciones ChromaDB

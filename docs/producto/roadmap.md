# Roadmap — AskMyDocs

## Fase 0 — Scaffolding ✅
**Estado:** Completado — 2026-04-27

- Estructura del proyecto
- CLAUDE.md, README.md, .env.example
- Archivos de memoria inicializados
- Stubs de módulos
- requirements.txt, docker-compose.yml base

---

## Fase A — Ingestión de documentos
**Estado:** Pendiente
**Objetivo:** Subir cualquier documento → procesarlo → guardarlo en ChromaDB

### Tareas
- [ ] `app/ingestion/loaders.py` — PDF, Word, Excel, TXT
- [ ] `app/ingestion/chunker.py` — RecursiveCharacterTextSplitter
- [ ] `app/ingestion/embeddings.py` — generación y persistencia ChromaDB
- [ ] `app/config.py` — variables de entorno con pydantic-settings
- [ ] `app/main.py` — FastAPI app base
- [ ] Endpoint `POST /documents/upload`

**Criterio de éxito:** PDF de 10 páginas indexado y visible en ChromaDB

---

## Fase B — Motor de preguntas
**Estado:** Pendiente
**Objetivo:** Pregunta → respuesta con fuente citada

### Tareas
- [ ] `app/retrieval/retriever.py` — búsqueda semántica
- [ ] `app/retrieval/prompts.py` — prompt template con obligación de citar
- [ ] `app/retrieval/chain.py` — RAG chain completa
- [ ] Manejo de "no encontrado" sin alucinaciones
- [ ] Endpoint `POST /query`

**Criterio de éxito:** Respuesta con cita (documento + página) verificable

---

## Fase C — API REST con FastAPI
**Estado:** Pendiente
**Objetivo:** API documentada y robusta

### Tareas
- [ ] `app/api/schemas.py` — modelos Pydantic completos
- [ ] `app/api/routes/documents.py` — CRUD documentos
- [ ] `app/api/routes/query.py` — endpoint consultas
- [ ] `GET /documents` — listar documentos indexados
- [ ] `DELETE /documents/{id}` — eliminar documento
- [ ] Manejo de errores con HTTP codes correctos

**Criterio de éxito:** Swagger en /docs cubre todo sin leer código

---

## Fase D — Observabilidad con LangFuse
**Estado:** Pendiente
**Objetivo:** Trazas completas de cada consulta

### Tareas
- [ ] `app/observability/tracing.py` — integración LangFuse
- [ ] LangFuse callback en LangChain chain
- [ ] Dashboard activo en cloud.langfuse.com
- [ ] Evaluación manual de respuestas

**Criterio de éxito:** Cada consulta visible en LangFuse con tokens + latencia

---

## Fase E — Interfaz y Docker
**Estado:** Pendiente
**Objetivo:** Deploy en un comando

### Tareas
- [ ] `app/ui/streamlit_app.py` — subir docs + preguntar + ver fuentes
- [ ] `Dockerfile` para FastAPI
- [ ] `Dockerfile.streamlit` para UI
- [ ] `docker-compose.yml` completo
- [ ] README con instalación en 3 pasos

**Criterio de éxito:** `docker-compose up` funciona en máquina limpia

---

## Backlog — Ideas futuras

- Soporte para URLs (scraping web)
- Múltiples colecciones / proyectos
- Autenticación básica
- Historial de conversaciones por documento
- Export de respuestas a PDF

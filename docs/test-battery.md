# Batería de Pruebas — AskMyDocs

Ejecutar con app corriendo: `uvicorn app.main:app --reload`
Swagger en: http://localhost:8000/docs

---

## 0. Prerequisitos

- [ ] `.env` creado con `ANTHROPIC_API_KEY` real
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Directorio `data/` creado o se crea automáticamente al primer upload

---

## 1. Infraestructura

| # | Test | Comando | Esperado |
|---|------|---------|----------|
| 1.1 | Health check | `GET /health` | `{"status": "ok"}` — 200 |
| 1.2 | Swagger accesible | Abrir http://localhost:8000/docs | UI Swagger carga sin errores |
| 1.3 | pytest unitarios | `pytest tests/ -v` | Todos pasan |

---

## 2. Ingestión (Fase A)

### 2.1 Upload PDF
- [ ] Subir PDF de ≥5 páginas via `POST /documents/upload`
- Esperado: 200, `chunks > 0`, `filename` correcto

### 2.2 Upload DOCX
- [ ] Subir fichero `.docx` con texto
- Esperado: 200, `chunks > 0`

### 2.3 Upload XLSX
- [ ] Subir fichero `.xlsx` con ≥2 hojas y datos
- Esperado: 200, `chunks > 0`

### 2.4 Upload TXT
- [ ] Subir fichero `.txt` con texto largo (>1000 chars)
- Esperado: 200, `chunks > 1` (chunking funciona)

### 2.5 Extensión no soportada
- [ ] Subir fichero `.csv`
- Esperado: **400**, `"Extension .csv not supported"`

### 2.6 Fichero vacío / corrupto
- [ ] Subir PDF vacío (0 bytes) o corrupto
- Esperado: **500** con detalle del error (no crash silencioso)

---

## 3. Listado y borrado (Fase C)

### 3.1 Listar documentos
- [ ] `GET /documents/` tras subir 2+ docs
- Esperado: array con todos los docs subidos, campos `id`, `filename`, `chunks`, `uploaded_at`

### 3.2 Listar vacío
- [ ] `GET /documents/` con ChromaDB limpio
- Esperado: `[]` — 200

### 3.3 Borrar documento existente
- [ ] `DELETE /documents/{id}` con id válido
- Esperado: 200, `{"deleted": "{id}"}`

### 3.4 Borrar documento inexistente
- [ ] `DELETE /documents/id-que-no-existe`
- Esperado: **404**, `"Document not found"`

### 3.5 Verificar borrado en listado
- [ ] `GET /documents/` tras borrar
- Esperado: doc borrado no aparece

---

## 4. Motor RAG (Fase B)

### 4.1 Pregunta con respuesta en documento
- [ ] Subir PDF con contenido conocido
- [ ] `POST /query` con pregunta cuya respuesta está en el doc
- Esperado: respuesta coherente + `sources` con `document` y `page` correctos

### 4.2 Pregunta sin respuesta en documentos
- [ ] `POST /query` con pregunta fuera del contexto indexado
- Esperado: respuesta contiene "No encontré información"

### 4.3 Fuentes verificables
- [ ] Tomar una respuesta del test 4.1
- [ ] Abrir el PDF en la página indicada en `sources[].page`
- Esperado: el texto del chunk coincide con el contenido real del PDF

### 4.4 top_k funciona
- [ ] `POST /query` con `top_k: 2` vs `top_k: 6`
- Esperado: `sources` tiene ≤2 y ≤6 entradas respectivamente

### 4.5 Documento borrado no aparece en fuentes
- [ ] Subir 2 docs, borrar uno, preguntar sobre contenido del borrado
- Esperado: respuesta dice "No encontré información" o fuentes solo del doc activo

---

## 5. Observabilidad LangFuse (Fase D)

> Requiere keys reales en `.env` (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`).
> Sin keys: tracing se omite silenciosamente — app funciona igual.

### 5.1 Sin keys configuradas
- [ ] `.env` con `pk-lf-...` (placeholder)
- [ ] `POST /query` con cualquier pregunta
- Esperado: respuesta normal, **sin error**, tracing simplemente no ocurre

### 5.2 Con keys reales
- [ ] Configurar cuenta en https://cloud.langfuse.com (tier gratuito)
- [ ] Añadir `LANGFUSE_PUBLIC_KEY` y `LANGFUSE_SECRET_KEY` reales al `.env`
- [ ] Reiniciar app y hacer `POST /query`
- Esperado: traza visible en cloud.langfuse.com con nombre `rag-query`

### 5.3 Contenido de la traza
- [ ] Abrir traza en LangFuse dashboard
- Esperado: tokens de entrada/salida, latencia, prompt enviado, respuesta recibida

### 5.4 Múltiples queries
- [ ] Hacer 3+ queries distintas
- Esperado: 3+ trazas en LangFuse, cada una con su pregunta

---

## 6. UI Streamlit + Docker (Fase E)

### 6.1 UI local (sin Docker)
- [ ] `streamlit run app/ui/streamlit_app.py`
- [ ] Con app FastAPI corriendo en `:8000`
- Esperado: UI carga en http://localhost:8501, columna izquierda y derecha visibles

### 6.2 Upload desde UI
- [ ] Arrastrar PDF al file uploader → click "Indexar"
- Esperado: spinner → mensaje ✅ con nombre y chunks → doc aparece en lista

### 6.3 Lista de documentos en UI
- [ ] Subir 2 docs
- Esperado: ambos aparecen con nombre + número de chunks + botón 🗑

### 6.4 Borrar desde UI
- [ ] Click en 🗑 en un doc de la lista
- Esperado: doc desaparece de la lista tras rerun

### 6.5 Query desde UI
- [ ] Escribir pregunta → click "Preguntar"
- Esperado: respuesta aparece en markdown + sección "Fuentes" con expanders

### 6.6 Docker build
- [ ] `docker build -t askmydocs-api .`
- [ ] `docker build -f Dockerfile.streamlit -t askmydocs-ui .`
- Esperado: ambas imágenes construyen sin errores

### 6.7 Docker Compose completo
- [ ] `docker-compose up --build`
- Esperado: API en :8000, UI en :8501, `/health` devuelve 200

### 6.8 Flujo completo en Docker
- [ ] Con docker-compose corriendo: subir doc desde UI → preguntar
- Esperado: respuesta con fuentes, mismo comportamiento que local

---

## 7. Casos borde

| # | Test | Esperado |
|---|------|----------|
| 5.1 | Pregunta vacía `""` | 422 o respuesta genérica |
| 5.2 | PDF con solo imágenes (sin texto extraíble) | 200 pero `chunks: 0` o error descriptivo |
| 5.3 | Upload mismo fichero dos veces | Dos `document_id` distintos, ambos indexados |
| 5.4 | Pregunta muy larga (>500 chars) | Responde sin error |

---

## Estado de cobertura por fase

| Fase | Pytest | Manual |
|------|--------|--------|
| A — Ingestión | ✅ `test_ingestion.py` | Pendiente ejecución |
| B — RAG | ✅ `test_retrieval.py` | Pendiente ejecución |
| C — CRUD API | ✅ `test_api.py` | Pendiente ejecución |
| D — LangFuse | N/A (integración externa) | Pendiente ejecución |
| E — Docker/UI | N/A | Pendiente ejecución |

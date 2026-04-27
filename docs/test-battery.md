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

## 5. Casos borde

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
| D — LangFuse | Pendiente | Pendiente |
| E — Docker/UI | Pendiente | Pendiente |

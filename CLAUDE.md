# AskMyDocs — CLAUDE.md

## Qué es este proyecto

AskMyDocs es una herramienta de inteligencia documental universal.
Permite a cualquier usuario subir documentos (PDF, Word, Excel, TXT)
y hacerles preguntas en lenguaje natural, obteniendo respuestas
precisas con la fuente exacta citada.

Proyecto público en GitHub como portfolio técnico de Juanma López Tech.
Demuestra dominio del stack profesional que piden las ofertas de
Data AI Engineer en España (2025-2026).

---

## Stack técnico

- **Python 3.11** — lenguaje base
- **LangChain** — orquestación del pipeline RAG y agente
- **ChromaDB** — base de datos vectorial local
- **LangFuse** — observabilidad, trazas y evaluación de calidad
- **FastAPI** — API REST con documentación automática
- **Streamlit** — interfaz web para usuarios no técnicos
- **Docker + docker-compose** — deploy con un solo comando
- **Claude API (Anthropic)** — modelo de lenguaje principal

---

## Estructura del proyecto

```
askmydocs/
├── CLAUDE.md                  # Este fichero
├── README.md                  # Documentación pública
├── docker-compose.yml         # Deploy completo
├── .env.example               # Variables de entorno requeridas
├── requirements.txt           # Dependencias Python
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Punto de entrada FastAPI
│   ├── config.py              # Configuración y variables de entorno
│   │
│   ├── ingestion/             # Fase A: ingestión de documentos
│   │   ├── __init__.py
│   │   ├── loaders.py         # Carga PDF, Word, Excel, TXT
│   │   ├── chunker.py         # Estrategia de chunking
│   │   └── embeddings.py      # Generación y almacenamiento vectorial
│   │
│   ├── retrieval/             # Fase B: motor de preguntas
│   │   ├── __init__.py
│   │   ├── retriever.py       # Recuperación de chunks relevantes
│   │   ├── chain.py           # LangChain RAG chain
│   │   └── prompts.py         # Prompt templates
│   │
│   ├── api/                   # Fase C: API REST
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── documents.py   # Endpoints subida y gestión de docs
│   │   │   └── query.py       # Endpoint de preguntas
│   │   └── schemas.py         # Modelos Pydantic
│   │
│   ├── observability/         # Fase D: LangFuse
│   │   ├── __init__.py
│   │   └── tracing.py         # Integración LangFuse
│   │
│   └── ui/                    # Fase E: interfaz Streamlit
│       └── streamlit_app.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_api.py
│
└── docs/
    └── architecture.md        # Diagrama de arquitectura
```

---

## Variables de entorno requeridas

```env
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# LangFuse (obtener en cloud.langfuse.com, tier gratuito)
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com

# ChromaDB
CHROMA_PERSIST_PATH=./data/chroma

# App
APP_ENV=development
MAX_FILE_SIZE_MB=50
SUPPORTED_EXTENSIONS=pdf,docx,xlsx,txt
```

---

## Fases de construcción

### Fase A — Ingestión de documentos
**Objetivo:** Subir cualquier documento → procesarlo → guardarlo en ChromaDB

Tareas:
- [ ] Configurar LangChain document loaders para PDF, Word, Excel, TXT
- [ ] Implementar estrategia de chunking (RecursiveCharacterTextSplitter)
- [ ] Generar embeddings con Claude o OpenAI embeddings
- [ ] Persistir en ChromaDB con metadatos (nombre fichero, página, fecha)
- [ ] Endpoint FastAPI POST /documents/upload

Criterio de éxito: subir un PDF de 10 páginas y verlo indexado en ChromaDB

---

### Fase B — Motor de preguntas
**Objetivo:** Pregunta en lenguaje natural → respuesta con fuente citada

Tareas:
- [ ] Implementar retriever con búsqueda semántica
- [ ] Construir RAG chain con LangChain (retriever + LLM + prompt)
- [ ] Prompt template que obliga a citar fuente exacta (documento + página)
- [ ] Manejo de caso "no encontrado" sin alucinaciones
- [ ] Endpoint FastAPI POST /query

Criterio de éxito: preguntar sobre el PDF y obtener respuesta con cita exacta

---

### Fase C — API REST con FastAPI
**Objetivo:** API documentada, robusta y lista para producción

Tareas:
- [ ] Endpoints completos con validación Pydantic
- [ ] Documentación automática en /docs (Swagger)
- [ ] Manejo de errores con códigos HTTP correctos
- [ ] Endpoint GET /documents para listar documentos indexados
- [ ] Endpoint DELETE /documents/{id} para eliminar documentos

Criterio de éxito: cualquier desarrollador puede usar la API sin leer el código

---

### Fase D — Observabilidad con LangFuse
**Objetivo:** Ver cada traza, detectar fallos y medir calidad de respuestas

Tareas:
- [ ] Integrar LangFuse callback en LangChain chain
- [ ] Trazas automáticas de cada consulta (input, output, tokens, latencia)
- [ ] Dashboard en cloud.langfuse.com funcionando
- [ ] Añadir evaluación manual de respuestas desde el dashboard

Criterio de éxito: cada pregunta aparece como traza en LangFuse con métricas

---

### Fase E — Interfaz y Docker
**Objetivo:** Cualquier usuario lo usa sin tocar código, deploy en un comando

Tareas:
- [ ] Interfaz Streamlit: subir documentos + hacer preguntas + ver fuentes
- [ ] Dockerfile para la app FastAPI
- [ ] Dockerfile para Streamlit
- [ ] docker-compose.yml que levanta todo (app + chromadb + streamlit)
- [ ] README con instrucciones de instalación en 3 pasos

Criterio de éxito: `docker-compose up` y funciona en cualquier máquina

---

## Reglas de trabajo — LEER SIEMPRE ANTES DE ACTUAR

1. Leer `.claude/memory/context.md` → estado actual del proyecto
2. Leer `.claude/memory/decisions.md` → decisiones ya tomadas
3. Leer `.claude/memory/errors.md` → errores previos a evitar
4. Nunca repetir un error documentado en errors.md
5. Nunca credenciales ni secrets en el repo — solo en `.env`
6. Antes de crear algo nuevo, verificar que no existe ya
7. Al finalizar cada sesión: actualizar context.md con el estado actual
8. Si se resuelve un error: documentarlo en errors.md
9. Si se toma una decisión técnica: documentarla en decisions.md
10. Construir fase por fase — no avanzar sin cumplir criterio de éxito

## Principios de desarrollo

- **Código y comentarios en inglés**
- **Type hints obligatorios en todas las funciones**
- **Una responsabilidad por fichero**
- **Nunca hardcodear credenciales** — siempre variables de entorno
- **Commits descriptivos:** `feat:`, `fix:`, `docs:`, `refactor:`
- **Simplicidad sobre sofisticación innecesaria**
- **Funciona primero, optimiza después**

## Archivos de memoria — leer al inicio de cada sesión

- Estado actual → `.claude/memory/context.md`
- Decisiones técnicas → `.claude/memory/decisions.md`
- Errores resueltos → `.claude/memory/errors.md`
- Patrones de código → `.claude/memory/patterns.md`
- Lecciones aprendidas → `tasks/lessons.md`

## Prompt de inicio de sesión estándar

Ver: `.claude/prompts/inicio-sesion.md`

## Convenciones de código

- Todo el código en inglés (variables, funciones, comentarios)
- Docstrings en todas las funciones públicas
- Type hints obligatorios en todas las funciones
- Un fichero = una responsabilidad clara
- Sin hardcodear credenciales, siempre variables de entorno
- Commits descriptivos: `feat:`, `fix:`, `docs:`, `refactor:`

## Contexto del autor

Juanma López Tech — consultor de IA y tecnología para PyMEs.
Este proyecto es portfolio público y herramienta de aprendizaje activo.
Cada fase completada se publica como contenido en LinkedIn y GitHub.

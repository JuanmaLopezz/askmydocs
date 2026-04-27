# AskMyDocs

Herramienta de inteligencia documental universal. Sube documentos (PDF, Word, Excel, TXT) y hazles preguntas en lenguaje natural — respuestas precisas con la fuente exacta citada.

## Stack

- Python 3.11 + FastAPI + LangChain + ChromaDB + LangFuse + Streamlit + Docker
- Claude API (Anthropic) como LLM principal

## Requisitos

- Python 3.11+
- Docker y docker-compose
- API keys: Anthropic + LangFuse (tier gratuito en cloud.langfuse.com)

## Instalación

```bash
git clone https://github.com/JuanmaLopezz/askmydocs.git
cd askmydocs

cp .env.example .env
# Editar .env con las API keys reales

pip install -r requirements.txt
```

## Uso rápido (Docker)

```bash
docker-compose up
```

Acceder a:
- API: http://localhost:8000/docs
- UI: http://localhost:8501

## Uso local (desarrollo)

```bash
# API
uvicorn app.main:app --reload

# UI (terminal separada)
streamlit run app/ui/streamlit_app.py
```

## Estructura del proyecto

Ver `CLAUDE.md` para documentación completa de arquitectura y fases.

## Estado del proyecto

- [ ] Fase A — Ingestión de documentos
- [ ] Fase B — Motor de preguntas
- [ ] Fase C — API REST
- [ ] Fase D — Observabilidad LangFuse
- [ ] Fase E — Interfaz y Docker

## Autor

[Juanma López Tech](https://github.com/JuanmaLopezz) — portfolio de Data AI Engineering

## Licencia

MIT

# Estado actual de AskMyDocs

## Última actualización
2026-04-27 — Proyecto iniciado. Scaffolding completado.

## Fase actual
FASE 0 — Scaffolding completado. Pendiente arrancar Fase A.

## Lo que está hecho

### Infraestructura
- [x] Estructura de carpetas creada
- [x] CLAUDE.md con fases, stack y convenciones
- [x] README.md
- [x] .env.example con todas las variables requeridas
- [x] .gitignore
- [x] Archivos de memoria inicializados
- [x] Stubs de todos los módulos (app/, tests/)
- [x] requirements.txt
- [x] docker-compose.yml (estructura base)

### Pendiente — Fase A
- [ ] Implementar loaders.py (PDF, Word, Excel, TXT)
- [ ] Implementar chunker.py (RecursiveCharacterTextSplitter)
- [ ] Implementar embeddings.py (ChromaDB)
- [ ] Implementar app/main.py y app/config.py
- [ ] Endpoint POST /documents/upload

## Cómo arrancar el proyecto

```bash
cp .env.example .env
# Editar .env con API keys reales

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Notas importantes
- Usar Python 3.11
- LangFuse tier gratuito en cloud.langfuse.com
- ChromaDB persiste en ./data/chroma (gitignoreado)

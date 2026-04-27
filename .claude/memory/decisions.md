# Decisiones técnicas de AskMyDocs

## Formato de entrada
### [FECHA] — [Título de la decisión]
**Decisión:** qué se decidió
**Alternativas descartadas:** qué otras opciones había
**Motivo:** por qué se eligió esta opción
**Impacto:** qué afecta esta decisión

---

## Registro

### 2026-04-27 — ChromaDB como vector store local
**Decisión:** ChromaDB con persistencia local en ./data/chroma
**Alternativas descartadas:** Pinecone, Weaviate, pgvector
**Motivo:** Sin coste, sin dependencias externas, suficiente para portfolio
**Impacto:** Deploy sencillo con Docker, no requiere servicios externos

### 2026-04-27 — Claude API como LLM principal
**Decisión:** claude-sonnet-4-6 para generación de respuestas
**Alternativas descartadas:** OpenAI GPT-4, Gemini
**Motivo:** Portfolio demuestra stack Anthropic, coherente con marca personal
**Impacto:** Requiere ANTHROPIC_API_KEY, coste por token

### 2026-04-27 — LangChain para orquestación RAG
**Decisión:** LangChain como framework de orquestación
**Alternativas descartadas:** LlamaIndex, código custom
**Motivo:** Estándar de mercado, aparece en todas las ofertas Data AI Engineer
**Impacto:** Facilita integración con LangFuse via callbacks nativos

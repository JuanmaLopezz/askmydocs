# Visión del producto — AskMyDocs

## Problema que resuelve
Empresas y profesionales acumulan documentos (contratos, informes, manuales) que
no pueden consultar eficientemente. Buscar información específica requiere leer
documentos enteros o depender de memoria humana.

## Solución
Sistema RAG que indexa cualquier documento y permite hacer preguntas en lenguaje
natural, devolviendo respuestas precisas con la fuente exacta citada.

## Usuario objetivo
- Data AI Engineers buscando referencia de implementación RAG
- PyMEs con volumen de documentación que necesitan consultar
- Juanma López Tech como portfolio público de competencias

## Propuesta de valor
- Respuestas en segundos sobre cualquier documento
- Fuente exacta citada — sin alucinaciones sin respaldo
- Deploy en un comando — cualquier equipo lo levanta
- Observable — cada consulta trazada en LangFuse

## Lo que NO es este proyecto
- No es un sistema de gestión documental completo
- No reemplaza búsqueda full-text para documentos simples
- No está diseñado para escala empresarial (sin autenticación multi-tenant)

## Métricas de éxito
- Fase A: PDF de 10 páginas indexado en ChromaDB
- Fase B: Pregunta respondida con cita exacta (documento + página)
- Fase C: API usable sin leer el código (Swagger completo)
- Fase D: Cada consulta visible en LangFuse con métricas
- Fase E: `docker-compose up` funciona en máquina limpia

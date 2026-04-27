from pathlib import Path
from langchain_core.documents import Document


def load_document(file_path: Path) -> list[Document]:
    """Load a document from disk. Supports PDF, DOCX, XLSX, TXT."""
    # TODO: Fase A — implement per-extension loaders
    raise NotImplementedError("Fase A pendiente")

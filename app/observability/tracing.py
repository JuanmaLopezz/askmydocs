from __future__ import annotations
import os
from langchain_core.callbacks import BaseCallbackHandler
from app.config import settings


def get_langfuse_callback() -> BaseCallbackHandler | None:
    pk = settings.langfuse_public_key
    sk = settings.langfuse_secret_key
    if not pk or pk.startswith("pk-lf-...") or not sk or sk.startswith("sk-lf-..."):
        return None
    try:
        os.environ["LANGFUSE_PUBLIC_KEY"] = pk
        os.environ["LANGFUSE_SECRET_KEY"] = sk
        os.environ["LANGFUSE_HOST"] = settings.langfuse_host
        from langfuse.langchain import CallbackHandler
        return CallbackHandler()
    except Exception:
        return None

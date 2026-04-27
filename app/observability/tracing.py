from langchain_core.callbacks import BaseCallbackHandler
from app.config import settings


def get_langfuse_callback() -> BaseCallbackHandler | None:
    pk = settings.langfuse_public_key
    sk = settings.langfuse_secret_key
    if not pk or pk.startswith("pk-lf-...") or not sk or sk.startswith("sk-lf-..."):
        return None
    try:
        from langfuse.callback import CallbackHandler
        return CallbackHandler(
            public_key=pk,
            secret_key=sk,
            host=settings.langfuse_host,
        )
    except Exception:
        return None

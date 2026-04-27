from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    chroma_persist_path: str = "./data/chroma"
    app_env: str = "development"
    max_file_size_mb: int = 50
    supported_extensions: str = "pdf,docx,xlsx,txt"

    class Config:
        env_file = ".env"

    @property
    def supported_extensions_list(self) -> list[str]:
        return self.supported_extensions.split(",")


settings = Settings()

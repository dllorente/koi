from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    intent_confidence_threshold: float = 0.60
    langchain_api_key: str | None = None
    langchain_tracing: bool = False
    langchain_project: str = "koi"
    langchain_endpoint: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    llm_vendor: str = Field(default='groq', alias='LLM_VENDOR')
    llm_model: str = Field(default='groq/llama-3.1-8b-instant', alias='LLM_MODEL')

    groq_api_key: str | None = Field(default=None, alias='GROQ_API_KEY')
    openai_api_key: str | None = Field(default=None, alias='OPENAI_API_KEY')
    anthropic_api_key: str | None = Field(default=None, alias='ANTHROPIC_API_KEY')

    groq_base_url: str = Field(default='https://api.groq.com/openai/v1', alias='GROQ_BASE_URL')
    openai_base_url: str = Field(default='https://api.openai.com/v1', alias='OPENAI_BASE_URL')
    ollama_base_url: str = Field(default='http://localhost:11434', alias='OLLAMA_BASE_URL')

    app_name: str = Field(default='UAE Hiring Intelligence Copilot', alias='APP_NAME')


def get_settings() -> Settings:
    return Settings()

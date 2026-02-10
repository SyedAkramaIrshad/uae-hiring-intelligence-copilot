from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = Field(default='UAE Hiring Intelligence Copilot', alias='APP_NAME')
    app_env: str = Field(default='dev', alias='APP_ENV')
    backend_host: str = Field(default='0.0.0.0', alias='BACKEND_HOST')
    backend_port: int = Field(default=8000, alias='BACKEND_PORT')

    llm_vendor: str = Field(default='groq', alias='LLM_VENDOR')
    llm_model: str = Field(default='groq/llama-3.1-8b-instant', alias='LLM_MODEL')

    groq_api_key: str | None = Field(default=None, alias='GROQ_API_KEY')
    openai_api_key: str | None = Field(default=None, alias='OPENAI_API_KEY')
    anthropic_api_key: str | None = Field(default=None, alias='ANTHROPIC_API_KEY')

    groq_base_url: str = Field(default='https://api.groq.com/openai/v1', alias='GROQ_BASE_URL')
    openai_base_url: str = Field(default='https://api.openai.com/v1', alias='OPENAI_BASE_URL')
    ollama_base_url: str = Field(default='http://localhost:11434', alias='OLLAMA_BASE_URL')

    rule_based_default: bool = Field(default=True, alias='RULE_BASED_DEFAULT')

    # Throughput controls (tunable for cost/rate limits)
    candidate_batch_size: int = Field(default=1, alias='CANDIDATE_BATCH_SIZE')
    candidate_batch_pause_seconds: float = Field(default=1.5, alias='CANDIDATE_BATCH_PAUSE_SECONDS')
    llm_call_pause_seconds: float = Field(default=5.0, alias='LLM_CALL_PAUSE_SECONDS')

    # Retry controls
    llm_retry_attempts: int = Field(default=3, alias='LLM_RETRY_ATTEMPTS')
    llm_retry_base_seconds: float = Field(default=2.0, alias='LLM_RETRY_BASE_SECONDS')
    llm_retry_max_seconds: float = Field(default=12.0, alias='LLM_RETRY_MAX_SECONDS')

    # Token controls
    llm_jd_chars: int = Field(default=700, alias='LLM_JD_CHARS')
    llm_cv_chars: int = Field(default=700, alias='LLM_CV_CHARS')
    llm_max_tokens: int = Field(default=500, alias='LLM_MAX_TOKENS')

    def llm_available(self) -> bool:
        vendor = self.llm_vendor.lower().strip()
        if vendor == 'groq':
            return bool(self.groq_api_key)
        if vendor == 'openai':
            return bool(self.openai_api_key)
        if vendor == 'anthropic':
            return bool(self.anthropic_api_key)
        if vendor == 'ollama':
            return True
        return False


settings = Settings()

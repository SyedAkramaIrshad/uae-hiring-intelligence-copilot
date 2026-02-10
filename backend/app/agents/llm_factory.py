from strands import models

from backend.app.core.config import settings


def _require(value: str | None, name: str) -> str:
    if not value:
        raise ValueError(f'Missing required environment variable: {name}')
    return value


def build_model():
    vendor = settings.llm_vendor.lower().strip()

    if vendor == 'groq':
        return models.LiteLLMModel(
            model_id=settings.llm_model,
            params={
                'api_key': _require(settings.groq_api_key, 'GROQ_API_KEY'),
                'api_base': settings.groq_base_url,
                'temperature': 0.2,
                'max_tokens': settings.llm_max_tokens,
            },
        )
    if vendor == 'openai':
        return models.LiteLLMModel(
            model_id=settings.llm_model,
            params={
                'api_key': _require(settings.openai_api_key, 'OPENAI_API_KEY'),
                'api_base': settings.openai_base_url,
                'temperature': 0.2,
                'max_tokens': settings.llm_max_tokens,
            },
        )
    if vendor == 'anthropic':
        return models.LiteLLMModel(
            model_id=settings.llm_model,
            params={
                'api_key': _require(settings.anthropic_api_key, 'ANTHROPIC_API_KEY'),
                'temperature': 0.2,
                'max_tokens': settings.llm_max_tokens,
            },
        )
    if vendor == 'ollama':
        return models.LiteLLMModel(
            model_id=settings.llm_model,
            params={'api_base': settings.ollama_base_url, 'temperature': 0.2, 'max_tokens': settings.llm_max_tokens},
        )

    raise ValueError('Unsupported LLM_VENDOR. Use one of: groq | openai | anthropic | ollama')

from strands import Agent

from .config import Settings
from .llm_factory import build_model

SYSTEM_PROMPT = """
You are a senior UAE hiring copilot focused on AI/ML roles.
Be concise, practical, and recruiter-friendly.
When evaluating profiles/projects, prioritize:
1) production readiness
2) measurable business impact
3) clarity of architecture
4) deployment and observability
5) cost awareness.
""".strip()


def build_agent(settings: Settings) -> Agent:
    model = build_model(settings)
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        name=settings.app_name,
    )

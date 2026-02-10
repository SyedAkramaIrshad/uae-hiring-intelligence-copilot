from __future__ import annotations

import logging
import random
import time

from strands import Agent

from backend.app.agents.llm_factory import build_model
from backend.app.core.config import settings

SYSTEM_ORCHESTRATOR = (
    'You are an orchestrator for UAE hiring. Combine scorer and interviewer outputs into concise recruiter-ready notes.'
)
SYSTEM_SCORER = 'You are a strict recruiting scorer. Explain fit, risks, and UAE market relevance.'
SYSTEM_INTERVIEWER = 'You generate targeted interview questions for weak areas and role-critical skills.'

logger = logging.getLogger(__name__)


def _safe_agent(system_prompt: str) -> Agent | None:
    if not settings.llm_available():
        return None
    return Agent(model=build_model(), system_prompt=system_prompt, name='UAE-Hiring-Agent')


class MultiAgentFlow:
    def __init__(self) -> None:
        self.orchestrator = _safe_agent(SYSTEM_ORCHESTRATOR)
        self.scorer = _safe_agent(SYSTEM_SCORER)
        self.interviewer = _safe_agent(SYSTEM_INTERVIEWER)

    @property
    def active(self) -> bool:
        return all([self.orchestrator, self.scorer, self.interviewer])

    def _invoke_with_retry(self, agent: Agent, prompt: str) -> str:
        attempts = max(1, settings.llm_retry_attempts)
        base = max(0.1, settings.llm_retry_base_seconds)
        max_sleep = max(base, settings.llm_retry_max_seconds)

        last_error: Exception | None = None
        for i in range(attempts):
            try:
                return str(agent(prompt))
            except Exception as e:
                last_error = e
                if i == attempts - 1:
                    break
                sleep_s = min(max_sleep, base * (2**i))
                sleep_s += random.uniform(0, 0.5)
                logger.warning('LLM call failed (attempt %s/%s). Retrying in %.2fs. Error: %s', i + 1, attempts, sleep_s, e)
                time.sleep(sleep_s)

        raise RuntimeError(f'LLM call failed after {attempts} attempts: {last_error}')

    def generate_explanation(self, jd_text: str, cv_text: str, score: float, missing_skills: list[str]) -> str:
        if not self.active:
            miss = ', '.join(missing_skills[:5]) if missing_skills else 'none'
            return f'Rule-based summary: candidate scored {score}/100. Missing skills: {miss}.'

        scorer_prompt = (
            f'JD:\n{jd_text[:settings.llm_jd_chars]}\n\nCV:\n{cv_text[:settings.llm_cv_chars]}\n\nScore: {score}. '
            f'Missing skills: {missing_skills}. Provide concise rationale and risks in under 80 words.'
        )
        scorer_out = self._invoke_with_retry(self.scorer, scorer_prompt)

        orchestration_prompt = (
            'Merge into recruiter-ready explanation under 70 words. '
            f'Input analysis: {scorer_out[:1200]}'
        )
        return self._invoke_with_retry(self.orchestrator, orchestration_prompt)

    def generate_questions(self, jd_text: str, cv_text: str, missing_skills: list[str]) -> list[str]:
        if not self.active:
            base = [
                'Walk me through a project where you owned production deployment end-to-end.',
                'How would you prioritize trade-offs between model quality, latency, and cost?',
            ]
            if missing_skills:
                base.append(f'You mention limited exposure to {missing_skills[0]}. How would you ramp up in 30 days?')
            return base[:4]

        prompt = (
            f'JD:\n{jd_text[:settings.llm_jd_chars]}\n\nCV:\n{cv_text[:settings.llm_cv_chars]}\n\n'
            f'Missing skills: {missing_skills}. Generate 4 targeted interview questions as bullet points, each under 18 words.'
        )
        raw = self._invoke_with_retry(self.interviewer, prompt)
        lines = [line.strip('-• \t') for line in raw.splitlines() if line.strip()]
        return lines[:4] if lines else ['Describe one project demonstrating role-critical depth.']

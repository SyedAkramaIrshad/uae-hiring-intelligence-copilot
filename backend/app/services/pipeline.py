from __future__ import annotations

import time

from backend.app.agents.multi_agent import MultiAgentFlow
from backend.app.core.config import settings
from backend.app.core.schemas import CandidateResult
from backend.app.services.parser import parse_bytes
from backend.app.services.scoring import score_candidate


class HiringPipeline:
    def __init__(self) -> None:
        self.agent_flow = MultiAgentFlow()

    def evaluate(self, jd_name: str, jd_bytes: bytes, cvs: list[tuple[str, bytes]], shortlist_top_n: int = 3):
        jd_text = parse_bytes(jd_name, jd_bytes)
        results: list[CandidateResult] = []

        batch_size = max(1, settings.candidate_batch_size)
        pause_seconds = max(0.0, settings.candidate_batch_pause_seconds)

        for idx, (filename, content) in enumerate(cvs, start=1):
            cv_text = parse_bytes(filename, content)
            scored = score_candidate(jd_text, cv_text)
            explanation = self.agent_flow.generate_explanation(jd_text, cv_text, scored.score, scored.missing_skills)

            # Pause between LLM calls per candidate to reduce TPM bursts (esp. Groq free tier)
            if self.agent_flow.active and settings.llm_call_pause_seconds > 0:
                time.sleep(settings.llm_call_pause_seconds)

            questions = self.agent_flow.generate_questions(jd_text, cv_text, scored.missing_skills)

            results.append(
                CandidateResult(
                    candidate_name=filename.rsplit('.', 1)[0],
                    score=scored.score,
                    score_breakdown=scored.score_breakdown,
                    matched_skills=scored.matched_skills,
                    missing_skills=scored.missing_skills,
                    explanation=explanation,
                    interview_questions=questions,
                )
            )

            if idx % batch_size == 0 and idx < len(cvs):
                time.sleep(pause_seconds)

        ranked = sorted(results, key=lambda x: x.score, reverse=True)
        mode = 'llm' if self.agent_flow.active else 'rule-based'
        return mode, ranked[:shortlist_top_n], ranked

from pydantic import BaseModel, Field


class CandidateResult(BaseModel):
    candidate_name: str
    score: float = Field(ge=0, le=100)
    score_breakdown: dict[str, float]
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: str
    interview_questions: list[str]


class AnalyzeResponse(BaseModel):
    mode: str
    shortlist_top_n: int
    ranked_candidates: list[CandidateResult]


class HealthResponse(BaseModel):
    status: str
    app: str

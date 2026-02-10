from __future__ import annotations

from dataclasses import dataclass

from .features import extract_features


@dataclass
class ScoreResult:
    score: float
    score_breakdown: dict[str, float]
    matched_skills: list[str]
    missing_skills: list[str]


def score_candidate(jd_text: str, cv_text: str) -> ScoreResult:
    jd = extract_features(jd_text)
    cv = extract_features(cv_text)

    required = set(jd.skills)
    has = set(cv.skills)

    matched = sorted(required & has)
    missing = sorted(required - has)

    skill_score = (len(matched) / len(required) * 70.0) if required else 35.0

    jd_years = max(jd.years_experience, 1)
    exp_ratio = min(cv.years_experience / jd_years, 1.2)
    experience_score = min(exp_ratio * 20.0, 20.0)

    edu_map = {'unknown': 0, 'bachelors': 1, 'masters': 2, 'phd': 3}
    edu_bonus = 10.0 if edu_map.get(cv.education_level, 0) >= edu_map.get(jd.education_level, 0) else 5.0

    total = max(0.0, min(100.0, skill_score + experience_score + edu_bonus))

    return ScoreResult(
        score=round(total, 2),
        score_breakdown={
            'skills': round(skill_score, 2),
            'experience': round(experience_score, 2),
            'education': round(edu_bonus, 2),
        },
        matched_skills=matched,
        missing_skills=missing,
    )

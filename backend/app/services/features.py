from __future__ import annotations

import re
from dataclasses import dataclass

STOPWORDS = {
    'and', 'or', 'the', 'for', 'with', 'to', 'in', 'of', 'a', 'an', 'on', 'at', 'is', 'are',
    'be', 'as', 'by', 'from', 'that', 'this', 'will', 'can', 'you', 'we', 'our', 'their',
}


@dataclass
class ExtractedFeatures:
    skills: list[str]
    years_experience: int
    education_level: str


_SKILL_HINTS = [
    'python', 'fastapi', 'django', 'flask', 'sql', 'postgres', 'mysql', 'aws', 'azure',
    'gcp', 'docker', 'kubernetes', 'llm', 'nlp', 'machine learning', 'deep learning',
    'pytorch', 'tensorflow', 'spark', 'airflow', 'etl', 'streamlit', 'react', 'vite',
]


def normalize_tokens(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def extract_features(text: str) -> ExtractedFeatures:
    lower = text.lower()
    skills = []
    for skill in _SKILL_HINTS:
        if skill in lower:
            skills.append(skill)

    years = 0
    for m in re.findall(r"(\d+)\+?\s*(?:years|yrs)", lower):
        years = max(years, int(m))

    education = 'unknown'
    if 'phd' in lower or 'doctorate' in lower:
        education = 'phd'
    elif 'master' in lower or 'msc' in lower or 'm.s' in lower:
        education = 'masters'
    elif 'bachelor' in lower or 'bsc' in lower or 'b.e' in lower:
        education = 'bachelors'

    return ExtractedFeatures(skills=sorted(set(skills)), years_experience=years, education_level=education)

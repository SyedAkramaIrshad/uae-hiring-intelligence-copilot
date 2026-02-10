from backend.app.services.scoring import score_candidate


def test_score_candidate_orders_by_relevance():
    jd = 'We need Python FastAPI AWS Docker with 5 years experience and masters preferred.'
    strong_cv = 'Python FastAPI AWS Docker engineer with 7 years experience and Masters degree.'
    weak_cv = 'Frontend designer with figma and 1 year exp.'

    strong = score_candidate(jd, strong_cv)
    weak = score_candidate(jd, weak_cv)

    assert strong.score > weak.score
    assert 'python' in strong.matched_skills
    assert strong.score <= 100

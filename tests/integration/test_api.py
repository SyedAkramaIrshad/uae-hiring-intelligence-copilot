from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_analyze_endpoint():
    jd_text = b'Need Python FastAPI Docker AWS 5 years masters'
    cv1 = b'Python FastAPI AWS Docker 6 years masters'
    cv2 = b'Sales manager crm 3 years'

    files = [
        ('jd_file', ('jd.txt', jd_text, 'text/plain')),
        ('cv_files', ('ali.txt', cv1, 'text/plain')),
        ('cv_files', ('sara.txt', cv2, 'text/plain')),
    ]

    response = client.post('/analyze', data={'shortlist_top_n': '2'}, files=files)

    assert response.status_code == 200
    payload = response.json()
    assert 'ranked_candidates' in payload
    assert len(payload['ranked_candidates']) == 2
    assert payload['ranked_candidates'][0]['score'] >= payload['ranked_candidates'][1]['score']

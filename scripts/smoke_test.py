from pathlib import Path
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.main import app  # noqa: E402


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    samples = root / 'data' / 'samples'

    jd = (samples / 'sample_jd.txt').read_bytes()
    cv1 = (samples / 'candidate_ahmed.txt').read_bytes()
    cv2 = (samples / 'candidate_sana.txt').read_bytes()
    cv3 = (samples / 'candidate_omar.txt').read_bytes()

    client = TestClient(app)
    files = [
        ('jd_file', ('sample_jd.txt', jd, 'text/plain')),
        ('cv_files', ('candidate_ahmed.txt', cv1, 'text/plain')),
        ('cv_files', ('candidate_sana.txt', cv2, 'text/plain')),
        ('cv_files', ('candidate_omar.txt', cv3, 'text/plain')),
    ]
    r = client.post('/analyze', data={'shortlist_top_n': '3'}, files=files)
    print('status:', r.status_code)
    if r.status_code != 200:
        print(r.text)
        return 1

    data = r.json()
    print('mode:', data['mode'])
    for idx, row in enumerate(data['ranked_candidates'], start=1):
        print(f"{idx}. {row['candidate_name']}: {row['score']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

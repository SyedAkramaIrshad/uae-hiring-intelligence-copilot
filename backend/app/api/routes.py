from fastapi import APIRouter, File, Form, UploadFile

from backend.app.core.config import settings
from backend.app.core.schemas import AnalyzeResponse, HealthResponse
from backend.app.services.pipeline import HiringPipeline

router = APIRouter()
pipeline = HiringPipeline()


@router.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status='ok', app=settings.app_name)


@router.post('/analyze', response_model=AnalyzeResponse)
async def analyze(
    jd_file: UploadFile = File(...),
    cv_files: list[UploadFile] = File(...),
    shortlist_top_n: int = Form(3),
) -> AnalyzeResponse:
    jd_content = await jd_file.read()
    cvs = []
    for f in cv_files:
        cvs.append((f.filename, await f.read()))

    mode, _, ranked = pipeline.evaluate(jd_file.filename, jd_content, cvs, shortlist_top_n=shortlist_top_n)
    return AnalyzeResponse(mode=mode, shortlist_top_n=shortlist_top_n, ranked_candidates=ranked)

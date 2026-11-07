from fastapi import APIRouter, HTTPException

from app.models import database
from app.schemas.analysis import AnalysisRecord, AnalyzeRequest
from app.services.analyzer import AnalysisError, analyze_idea

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisRecord)
async def analyze(body: AnalyzeRequest) -> AnalysisRecord:
    try:
        result = await analyze_idea(body.idea)
    except AnalysisError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    return database.save_analysis(body.idea, result)

from fastapi import APIRouter, HTTPException, Query

from app.models import database
from app.schemas.analysis import AnalysisRecord, HistoryItem

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=list[HistoryItem])
def history(limit: int = Query(default=20, ge=1, le=100)) -> list[HistoryItem]:
    return database.list_analyses(limit)


@router.get("/{record_id}", response_model=AnalysisRecord)
def history_detail(record_id: int) -> AnalysisRecord:
    record = database.get_analysis(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="분석 기록을 찾을 수 없습니다.")
    return record

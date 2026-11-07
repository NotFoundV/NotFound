import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from app import config
from app.schemas.analysis import AnalysisRecord, AnalysisResult, HistoryItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""


@contextmanager
def _connect(db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path or config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.execute(SCHEMA)


def save_analysis(idea: str, result: AnalysisResult) -> AnalysisRecord:
    created_at = datetime.now(timezone.utc)
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO analyses (idea, result_json, created_at) VALUES (?, ?, ?)",
            (idea, result.model_dump_json(), created_at.isoformat()),
        )
        record_id = cursor.lastrowid
    return AnalysisRecord(id=record_id, idea=idea, created_at=created_at, **result.model_dump())


def list_analyses(limit: int = 20) -> list[HistoryItem]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, idea, result_json, created_at FROM analyses ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        HistoryItem(
            id=row["id"],
            idea=row["idea"],
            created_at=row["created_at"],
            service_names=[s["name"] for s in json.loads(row["result_json"])["services"]],
        )
        for row in rows
    ]


def get_analysis(record_id: int) -> AnalysisRecord | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, idea, result_json, created_at FROM analyses WHERE id = ?",
            (record_id,),
        ).fetchone()
    if row is None:
        return None
    return AnalysisRecord(
        id=row["id"],
        idea=row["idea"],
        created_at=row["created_at"],
        **json.loads(row["result_json"]),
    )

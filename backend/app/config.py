import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")


def _env(name: str, default: str) -> str:
    # .env.example을 복사하면 빈 값(KEY=)이 남으므로 빈 문자열도 기본값으로 처리한다
    return os.getenv(name, "").strip() or default


ANTHROPIC_API_KEY: str = _env("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL: str = _env("CLAUDE_MODEL", "claude-opus-5-5")
DB_PATH: Path = Path(_env("DB_PATH", str(BACKEND_DIR / "found.db")))
# 웹 검색과 분석을 합친 전체 제한 시간(초). 웹 검색 단계가 대부분을 차지한다.
ANALYZE_TIMEOUT_SECONDS: float = float(_env("ANALYZE_TIMEOUT_SECONDS", "240"))

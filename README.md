# NotFound — AI 경쟁 서비스 비교 분석 시스템

창업 아이디어를 입력하면 **유사 서비스를 자동으로 탐색**하고, 각 서비스를 AI가 분석해
경쟁 구도를 한눈에 보여주는 서비스입니다.

## 핵심 흐름

1. **아이디어 입력** — 사용자가 창업 아이디어를 자연어로 입력
2. **유사 서비스 탐색** — 아이디어와 유사한 기존 서비스를 자동 검색·수집
3. **AI 분석** — 각 서비스에 대해 아래 항목을 AI가 분석
   - 비즈니스 모델
   - 핵심 기능
   - 수익 구조
   - 차별점
4. **비교 리포트** — 서비스 간 비교표와 인사이트를 제공

## 기술 스택

| 영역 | 스택 |
|------|------|
| 백엔드 | Python, FastAPI |
| 프론트엔드 | React (Vite) |
| DB | SQLite |

## 프로젝트 구조

```
NotFound/
├── backend/    # FastAPI 서버 (API, AI 분석, DB)
├── frontend/   # React(Vite) 웹 클라이언트
├── README.md
└── CLAUDE.md   # 개발 컨벤션 (Claude Code용)
```

## 시작하기

> 아직 초기 세팅 단계입니다. `backend/`와 `frontend/`에는 앱 코드가 없으며,
> 아래 명령어는 앱 초기화 후 사용할 실행 예시입니다. 현재 상태에서는 실행할 수 없습니다.

개발 환경은 Python 3.11 이상과 Node.js/npm을 사용하도록 계획되어 있습니다.
`requirements.txt`, `package.json` 및 앱 진입점은 각 앱을 초기화할 때 추가해야 합니다.

```bash
# 백엔드 (예정)
cd backend
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# 프론트엔드 (예정)
cd frontend
npm install
npm run dev
```

## 문서 안내

| 문서 | 내용 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 개발 방식, 코딩 컨벤션, 실행 명령어 |
| [backend/README.md](backend/README.md) | 백엔드 예정 구조와 개발 안내 |
| [frontend/README.md](frontend/README.md) | 프론트엔드 예정 구조와 개발 안내 |

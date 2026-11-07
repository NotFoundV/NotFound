# NotFound — AI 경쟁 서비스 비교 분석 시스템

창업 아이디어를 입력하면 **유사 서비스를 자동으로 탐색**하고, 각 서비스를 AI가 분석해
경쟁 구도를 한눈에 보여주는 서비스입니다.

## 핵심 흐름

1. **아이디어 입력** — 사용자가 창업 아이디어를 자연어로 입력
2. **유사 서비스 탐색** — 아이디어와 유사한 기존 서비스를 자동 검색·수집
3. **AI 분석** — 각 서비스에 대해 아래 항목을 AI가 분석
   - 비즈니스 모델 — 누구에게 어떤 가치를 어떤 방식으로 제공하는지
   - 핵심 기능 — 사용자가 이 서비스를 쓰는 주된 이유가 되는 기능
   - 수익 구조 — 구독, 수수료, 광고 등 실제로 돈을 버는 방식
   - 차별점 — 다른 유사 서비스와 구별되는 강점
4. **비교 리포트** — 서비스 간 비교표와 인사이트를 제공

## 개발 현황

- [x] 모노레포 구조, 개발 가이드, `.gitignore` 초기 세팅
- [x] 백엔드·프론트엔드 예정 구조 문서화
- [x] 백엔드 앱 초기화 (FastAPI) — `feature/backend` 브랜치
- [x] 프론트엔드 앱 초기화 (React + Vite) — `feature/frontend` 브랜치
- [x] 분석 API(`POST /api/analyze`)와 이력 API(`GET /api/history`, `GET /api/history/{id}`)
- [x] 웹 검색 기반 유사 서비스 탐색 + 4개 항목 분석 + 빈틈 인사이트
- [x] 결과 카드, 항목 비교표, 인사이트 박스, 최근 분석 이력 화면
- [x] 랜딩 페이지(`landing/index.html`)와 배포 문서(`docs/deploy.md`)
- [ ] 실제 API 키로 분석 품질 검증 (키 없이 오류 처리와 화면만 확인함)
- [ ] 분석 진행 단계를 서버 실제 진행 상황과 연동 (현재는 경과 시간 기준 표시)

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

Python 3.11 이상과 Node.js 20 이상이 필요합니다.
백엔드는 `feature/backend`, 프론트엔드와 랜딩은 `feature/frontend` 브랜치에 있으니
두 브랜치가 `main`에 병합된 뒤 아래 순서로 실행합니다.

```bash
# 백엔드 (http://127.0.0.1:8000)
cd backend
python -m venv .venv
.venv/Scripts/activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements-dev.txt
cp .env.example .env              # ANTHROPIC_API_KEY 채워 넣기
uvicorn app.main:app --reload
pytest                            # API 테스트

# 프론트엔드 (http://localhost:5173/app/)
cd frontend
npm install
npm run dev                       # /api 요청은 Vite 프록시가 8000번 백엔드로 넘김
```

- 분석 한 번에 웹 검색을 포함해 1~3분이 걸리고 Anthropic API 사용료가 나갑니다.
- 키가 없으면 `/api/analyze`는 503과 안내 문구를 돌려줍니다. 이력 조회는 키 없이 동작합니다.
- 서버 배포 구성은 [docs/deploy.md](docs/deploy.md)를 참고하세요.

## 문서 안내

| 문서 | 내용 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 개발 방식, 코딩 컨벤션, 실행 명령어 |
| [backend/README.md](backend/README.md) | 백엔드 예정 구조와 개발 안내 |
| [frontend/README.md](frontend/README.md) | 프론트엔드 예정 구조와 개발 안내 |

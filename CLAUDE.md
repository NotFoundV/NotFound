# CLAUDE.md — NotFound 개발 가이드

AI 경쟁 서비스 비교 분석 시스템. 사용자가 창업 아이디어를 입력하면 유사 서비스를
자동 탐색하고, 각 서비스의 비즈니스 모델/핵심 기능/수익 구조/차별점을 AI가 분석한다.

## 기술 스택

- **백엔드**: Python 3.11+, FastAPI, SQLite (SQLAlchemy 사용 여부는 스키마 설계 때 결정)
- **프론트엔드**: React + Vite + TypeScript
- **모노레포**: `backend/` `frontend/` 두 폴더로 분리. 루트에 공통 문서·설정만 둔다.

## 개발 방식

- **하나씩 쪼개서 상의하면서 개발한다.** 큰 기능은 설계를 먼저 논의하고 합의 후 구현.
- 커밋·배포는 사용자가 요청할 때만 한다.

## 코딩 컨벤션

### 공통
- 주석·문서·커밋 메시지는 한국어로 쓴다.
- 주석은 코드만으로 알 수 없는 제약·의도만 적는다.
- 시크릿(.env)은 절대 커밋하지 않는다. 필요한 키는 `.env.example`에 이름만 남긴다.

### 커밋 메시지
- `분류: 변경 내용` 형식으로 한 줄 요약을 쓴다 (예: `문서: 백엔드 예정 구조와 개발 안내 추가`).
- 분류 예시: `초기 세팅`, `문서`, `기능`, `수정`, `리팩터링`.
- 한 커밋에는 하나의 목적만 담는다.

### 백엔드 (backend/)
- 구조: `app/main.py` 진입점, `app/routers/` API 라우터, `app/services/` 비즈니스 로직,
  `app/models/` DB 모델, `app/schemas/` Pydantic 스키마.
- 네이밍: 파일·함수·변수 `snake_case`, 클래스 `PascalCase`.
- 모든 함수에 타입 힌트를 붙인다. API 입출력은 Pydantic 모델로 정의한다.
- 라우터는 도메인 단위로 나눈다 (예: `ideas`, `services`, `analysis`).

### 프론트엔드 (frontend/)
- 구조: `src/components/` 공용 컴포넌트, `src/pages/` 페이지, `src/api/` 백엔드 호출,
  `src/types/` 공용 타입.
- 네이밍: 컴포넌트 파일·이름 `PascalCase`, 훅·유틸 `camelCase`.
- 함수형 컴포넌트 + 훅만 사용. 백엔드 응답 타입은 `src/types/`에 정의해 공유한다.

### DB (SQLite)
- DB 파일(`*.db`)은 git에 올리지 않는다 (.gitignore 처리됨).
- 스키마 변경은 마이그레이션 스크립트 또는 문서로 기록한다.

## 실행 명령어

```bash
# 백엔드
cd backend && uvicorn app.main:app --reload   # 기본 포트 8000

# 프론트엔드
cd frontend && npm run dev                     # 기본 포트 5173
```

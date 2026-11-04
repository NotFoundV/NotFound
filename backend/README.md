# 백엔드

FastAPI 기반 API 서버를 위한 폴더입니다. 현재 앱 초기화 전이며,
아래 구조는 [개발 가이드](../CLAUDE.md)에 정의된 예정 구조입니다.

| 경로 | 역할 |
|------|------|
| `app/main.py` | FastAPI 앱 진입점 |
| `app/routers/` | 도메인별 API 라우터 |
| `app/services/` | 비즈니스 로직 |
| `app/models/` | DB 모델 |
| `app/schemas/` | API 입출력 스키마 |

Python 3.11 이상을 사용합니다. 의존성 목록과 앱 진입점이 추가된 후
[프로젝트 README](../README.md#시작하기)의 실행 예시를 참고하세요.

로컬 환경변수와 SQLite DB 파일은 커밋하지 않습니다.
필요한 환경변수 이름은 값 없이 `.env.example`에 기록합니다.

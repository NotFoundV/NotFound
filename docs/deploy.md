# 배포 안내

한 서버에서 `404.semo3.com` 하나로 아래 세 가지를 함께 제공한다.

| 경로 | 내용 |
|------|------|
| `/` | 랜딩 페이지 (`landing/index.html`) |
| `/app` | 프론트엔드 빌드 결과 (`frontend/dist`) |
| `/api` | FastAPI 백엔드 |

## 1. 백엔드 실행

```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # ANTHROPIC_API_KEY 채워 넣기
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

운영에서는 pm2나 systemd로 uvicorn이 계속 돌도록 등록한다.
분석 한 번에 웹 검색을 포함해 1~3분이 걸리므로 프록시 타임아웃을 넉넉히 잡는다.

## 2. 프론트엔드 빌드

```bash
cd frontend
npm ci
npm run build                 # vite base가 /app/ 이므로 dist는 /app 경로 기준으로 만들어진다
```

## 3. 정적 파일 배치

```
/srv/found/
├── index.html                # landing/index.html 복사
└── app/                      # frontend/dist 내용 복사
```

## 4. nginx 설정 예시

```nginx
server {
    listen 80;
    server_name 404.semo3.com;

    root /srv/found;

    # API: FastAPI로 전달
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;   # 웹 검색 포함 분석이 오래 걸린다
    }

    # 프론트엔드: /app 아래 단일 페이지 앱
    location /app/ {
        try_files $uri $uri/ /app/index.html;
    }
    location = /app {
        return 301 /app/;
    }

    # 랜딩 페이지
    location / {
        try_files $uri $uri/ =404;
    }
}
```

HTTPS는 Cloudflare 프록시나 certbot으로 붙인다.

## 현재 운영 서버 구성

운영 서버는 nginx 대신 Cloudflare 터널의 경로 규칙으로 같은 구조를 만든다.

| 규칙 | 연결 대상 |
|------|-----------|
| `404.semo3.com` + 경로 `^/api(/|$)` | FastAPI (`127.0.0.1:3013`) |
| `404.semo3.com` 나머지 | 정적 파일 서버 (`127.0.0.1:3014`, 랜딩 + `/app`) |

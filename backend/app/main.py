from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.models.database import init_db
from app.routers import analysis, history


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Found API", lifespan=lifespan)
app.include_router(analysis.router)
app.include_router(history.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

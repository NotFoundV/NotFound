from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import config
from app.routers import analysis as analysis_router
from app.schemas.analysis import AnalysisResult, ServiceAnalysis
from app.services import analyzer
from app.services.analyzer import AnalysisError


def _service(name: str) -> ServiceAnalysis:
    return ServiceAnalysis(
        name=name,
        url=None,
        summary="요약",
        business_model="모델",
        core_features="기능",
        revenue_model="수익",
        differentiation="차별점",
    )


SAMPLE = AnalysisResult(services=[_service("A"), _service("B"), _service("C")], insight="빈틈")


@pytest.fixture()
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "test.db")
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


def test_analyze_saves_history(client, monkeypatch) -> None:
    async def fake_analyze(idea: str) -> AnalysisResult:
        return SAMPLE

    monkeypatch.setattr(analysis_router, "analyze_idea", fake_analyze)
    res = client.post("/api/analyze", json={"idea": "반려동물 산책 대행 매칭 앱"})
    assert res.status_code == 200
    body = res.json()
    assert [s["name"] for s in body["services"]] == ["A", "B", "C"]

    history = client.get("/api/history").json()
    assert history[0]["id"] == body["id"]
    assert history[0]["service_names"] == ["A", "B", "C"]
    assert client.get(f"/api/history/{body['id']}").json()["insight"] == "빈틈"
    assert client.get("/api/history/9999").status_code == 404


def test_analyze_rejects_short_idea(client) -> None:
    assert client.post("/api/analyze", json={"idea": "  앱 "}).status_code == 422


def test_analyze_maps_errors(client, monkeypatch) -> None:
    async def failing(idea: str) -> AnalysisResult:
        raise AnalysisError(504, "시간 초과")

    monkeypatch.setattr(analysis_router, "analyze_idea", failing)
    res = client.post("/api/analyze", json={"idea": "반려동물 산책 대행 매칭 앱"})
    assert res.status_code == 504
    assert res.json()["detail"] == "시간 초과"


def test_missing_api_key_is_503(monkeypatch) -> None:
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", "")
    with pytest.raises(AnalysisError) as exc:
        analyzer._client()
    assert exc.value.status_code == 503


class _FakeMessages:
    def __init__(self, outputs: list[AnalysisResult]) -> None:
        self.outputs = outputs
        self.prompts: list[str] = []

    async def parse(self, **kwargs) -> SimpleNamespace:
        self.prompts.append(kwargs["messages"][0]["content"])
        return SimpleNamespace(stop_reason="end_turn", parsed_output=self.outputs.pop(0))


async def test_structure_retries_when_services_missing() -> None:
    too_few = AnalysisResult(services=[_service("A")], insight="빈틈")
    fake = SimpleNamespace(messages=_FakeMessages([too_few, SAMPLE]))
    result = await analyzer.structure_analysis(fake, "아이디어", "메모")
    assert len(result.services) == 3
    assert "이전 응답의 문제" in fake.messages.prompts[1]

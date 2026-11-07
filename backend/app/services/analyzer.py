"""유사 서비스 탐색과 항목별 분석.

웹 검색 결과에는 인용(citations)이 붙는데, 인용은 구조화 출력(output_format)과 함께 쓸 수 없다.
그래서 1단계(웹 검색으로 실제 서비스 조사)와 2단계(조사 내용을 정해진 JSON 스키마로 정리)를
별도 요청으로 나눈다.
"""

import asyncio

import anthropic
from pydantic import ValidationError

from app import config
from app.schemas.analysis import AnalysisResult

MAX_PAUSE_CONTINUATIONS = 3
MAX_STRUCTURE_ATTEMPTS = 3
MIN_SERVICES = 3
MAX_SERVICES = 5

SEARCH_SYSTEM = """당신은 스타트업 경쟁 분석가입니다. 사용자의 창업 아이디어와 유사한 실제 서비스를 웹 검색으로 찾습니다.
- 실제로 운영 중이거나 운영됐던 서비스만 고르고, 지어내지 마세요.
- 국내외를 가리지 않되 아이디어와 가장 가까운 서비스 3~5개를 고르세요.
- 서비스마다 공식 사이트 주소, 비즈니스 모델, 핵심 기능, 수익 구조, 차별점을 검색 결과에 근거해 정리하세요.
- 확인하지 못한 내용은 추정이라고 밝히세요.
- 한국어로 답하세요."""

STRUCTURE_SYSTEM = """당신은 경쟁 분석 리포트를 정해진 JSON 형식으로 정리합니다.
- 조사 메모에 있는 서비스만 사용하고, 메모에 없는 사실을 지어내지 마세요.
- services에는 3~5개 서비스를 넣고, 모든 항목(name, summary, business_model, core_features, revenue_model, differentiation)을 빠짐없이 한국어 1~3문장으로 채우세요.
- url은 메모에 공식 주소가 있으면 넣고, 없으면 null로 두세요.
- insight에는 경쟁 서비스들이 놓치고 있어 사용자 아이디어가 파고들 수 있는 빈틈을 1~2문장으로 쓰세요."""


class AnalysisError(Exception):
    """분석 실패. status_code는 API 응답 코드로 그대로 쓴다."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def _client() -> anthropic.AsyncAnthropic:
    if not config.ANTHROPIC_API_KEY:
        raise AnalysisError(503, "서버에 ANTHROPIC_API_KEY가 설정되지 않았습니다.")
    return anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY, timeout=180.0, max_retries=2)


def _text_of(content: list) -> str:
    return "\n".join(block.text for block in content if getattr(block, "type", None) == "text").strip()


async def search_similar_services(client: anthropic.AsyncAnthropic, idea: str) -> str:
    """웹 검색으로 유사 서비스를 조사해 자유 형식 메모로 돌려준다."""
    messages: list[dict] = [{"role": "user", "content": f"창업 아이디어:\n{idea}\n\n이 아이디어와 유사한 서비스를 조사해 주세요."}]
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]

    for _ in range(MAX_PAUSE_CONTINUATIONS + 1):
        response = await client.beta.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=16000,
            system=SEARCH_SYSTEM,
            tools=tools,
            messages=messages,
            output_config={"effort": "medium"},
            # 안전 분류기가 거절하면 서버가 다른 모델로 이어서 처리한다
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason == "refusal":
            raise AnalysisError(422, "이 아이디어는 분석할 수 없습니다. 내용을 바꿔 다시 시도해 주세요.")
        if response.stop_reason != "pause_turn":
            break
        # 서버 측 검색 루프가 한도에 걸려 멈춘 경우: 응답을 그대로 붙여 다시 보내면 이어서 진행한다
        messages = [messages[0], {"role": "assistant", "content": response.content}]

    notes = _text_of(response.content)
    if not notes:
        raise AnalysisError(502, "유사 서비스를 찾지 못했습니다. 아이디어를 더 구체적으로 적어 주세요.")
    return notes


def _check_result(result: AnalysisResult) -> list[str]:
    problems: list[str] = []
    if not MIN_SERVICES <= len(result.services) <= MAX_SERVICES:
        problems.append(f"services는 {MIN_SERVICES}~{MAX_SERVICES}개여야 하는데 {len(result.services)}개입니다.")
    for service in result.services:
        for field in ("name", "summary", "business_model", "core_features", "revenue_model", "differentiation"):
            if not getattr(service, field).strip():
                problems.append(f"'{service.name or '?'}'의 {field} 항목이 비어 있습니다.")
    if not result.insight.strip():
        problems.append("insight가 비어 있습니다.")
    return problems


async def structure_analysis(client: anthropic.AsyncAnthropic, idea: str, notes: str) -> AnalysisResult:
    """조사 메모를 스키마에 맞춘 결과로 정리한다. 형식이 어긋나면 문제점을 알려주고 다시 요청한다."""
    prompt = f"창업 아이디어:\n{idea}\n\n조사 메모:\n{notes}"
    feedback = ""
    for _ in range(MAX_STRUCTURE_ATTEMPTS):
        try:
            response = await client.messages.parse(
                model=config.CLAUDE_MODEL,
                max_tokens=8000,
                system=STRUCTURE_SYSTEM,
                messages=[{"role": "user", "content": prompt + feedback}],
                output_config={"effort": "low"},
                output_format=AnalysisResult,
            )
        except ValidationError as exc:
            feedback = f"\n\n이전 응답이 형식 검증에 실패했습니다: {exc.errors()[:3]}. 모든 항목을 채워 다시 작성하세요."
            continue
        if response.stop_reason == "refusal":
            raise AnalysisError(422, "이 아이디어는 분석할 수 없습니다. 내용을 바꿔 다시 시도해 주세요.")
        result = response.parsed_output
        if result is None:
            feedback = "\n\n이전 응답을 JSON으로 읽을 수 없었습니다. 형식에 맞춰 다시 작성하세요."
            continue
        problems = _check_result(result)
        if not problems:
            return result
        feedback = "\n\n이전 응답의 문제: " + " ".join(problems) + " 고쳐서 다시 작성하세요."
    raise AnalysisError(502, "분석 결과 형식을 맞추지 못했습니다. 잠시 후 다시 시도해 주세요.")


async def analyze_idea(idea: str) -> AnalysisResult:
    client = _client()

    async def run() -> AnalysisResult:
        notes = await search_similar_services(client, idea)
        return await structure_analysis(client, idea, notes)

    try:
        return await asyncio.wait_for(run(), timeout=config.ANALYZE_TIMEOUT_SECONDS)
    except asyncio.TimeoutError as exc:
        raise AnalysisError(504, "분석 시간이 너무 오래 걸렸습니다. 잠시 후 다시 시도해 주세요.") from exc
    except anthropic.AuthenticationError as exc:
        raise AnalysisError(503, "서버의 Anthropic API 키가 올바르지 않습니다.") from exc
    except anthropic.RateLimitError as exc:
        raise AnalysisError(429, "요청이 많아 잠시 처리할 수 없습니다. 잠시 후 다시 시도해 주세요.") from exc
    except anthropic.APITimeoutError as exc:
        raise AnalysisError(504, "AI 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.") from exc
    except anthropic.APIConnectionError as exc:
        raise AnalysisError(502, "AI 서버에 연결하지 못했습니다.") from exc
    except anthropic.APIStatusError as exc:
        raise AnalysisError(502, f"AI 서버 오류가 발생했습니다 ({exc.status_code}).") from exc

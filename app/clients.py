# ----------------------------
# 파일명 : clients.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : 비동기 API 호출과 asyncio.gather 동시 처리
# ----------------------------

"""SKALA Async API Data Pipeline - 외부 API 비동기 수집 모듈."""

import asyncio
from typing import Any

import httpx

from app.config import COUNTRY_URL, IP_URL, WEATHER_URL

API_LABELS = {
    "weather": "서울 날씨",
    "country": "한국 국가 정보",
    "ip": "IP 지역 정보",
}


async def fetch_json(client: httpx.AsyncClient, name: str, url: str) -> dict[str, Any]:
    # 공통 HTTP 요청 함수로 상태 코드 검증과 JSON 변환을 한 곳에서 처리한다.
    # 같은 요청 코드를 API마다 반복하지 않도록 이름과 URL만 전달받는다.
    response = await client.get(url)
    response.raise_for_status()
    # 응답이 JSON으로 변환되지 않으면 여기서 예외가 발생해 잘못된 데이터를
    # 검증 단계로 넘기지 않는다.
    payload = response.json()
    label = API_LABELS.get(name, name)
    print(f"[{label}] API 연결 성공 (상태 코드: {response.status_code})")
    return payload


async def collect_all() -> dict[str, dict[str, Any]]:
    # 세 API를 동시에 호출해 전체 수집 시간을 줄인다.
    async with httpx.AsyncClient(timeout=15.0) as client:
        # 하나의 AsyncClient를 공유해 연결을 재사용하고, gather로 세 요청을
        # 동시에 실행한다. 결과의 순서는 gather에 전달한 순서와 같다.
        weather, country, ip_info = await asyncio.gather(
            fetch_json(client, "weather", WEATHER_URL),
            fetch_json(client, "country", COUNTRY_URL),
            fetch_json(client, "ip", IP_URL),
        )
    return {"weather": weather, "country": country, "ip": ip_info}


async def main() -> None:
    results = await collect_all()
    for name, payload in results.items():
        print(f"[{name}] top-level keys={list(payload)[:10]}")


if __name__ == "__main__":
    asyncio.run(main())

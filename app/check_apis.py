# ----------------------------
# 파일명 : check_apis.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : 외부 API 연결 상태 확인
# ----------------------------

"""SKALA Async API Data Pipeline - API 연결 확인 모듈."""

import httpx

from app.config import COUNTRY_URL, IP_URL, WEATHER_URL

API_URLS = {
    "weather": WEATHER_URL,
    "country": COUNTRY_URL,
    "ip": IP_URL,
}

API_LABELS = {
    "weather": "서울 날씨",
    "country": "한국 국가 정보",
    "ip": "IP 지역 정보",
}


def main() -> None:
    # 각 외부 API가 정상적으로 응답하는지만 빠르게 확인한다.
    with httpx.Client(timeout=15.0) as client:
        for name, url in API_URLS.items():
            try:
                # 상태 코드와 JSON 변환을 모두 확인해 연결 문제를 즉시 표시한다.
                response = client.get(url)
                response.raise_for_status()
                payload = response.json()
                label = API_LABELS.get(name, name)
                print(f"[{label}] API 연결 성공 (상태 코드: {response.status_code})")
                print(f"[{label}] 응답 필드 확인: {list(payload)[:10]}")
            except (httpx.HTTPError, ValueError) as exc:
                label = API_LABELS.get(name, name)
                print(f"[{label}] API 연결 실패: {exc}")


if __name__ == "__main__":
    main()

# ----------------------------
# 파일명 : main.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : 파일 I/O, 예외 처리, Pydantic 검증 파이프라인
# ----------------------------

"""SKALA Async API Data Pipeline - 전체 파이프라인 실행 모듈."""

import asyncio

import pandas as pd

from app.clients import collect_all
from app.pipeline import validate_country, validate_ip, validate_weather
from app.storage import save_and_benchmark


async def run() -> None:
    # 수집 → Pydantic 검증 → DataFrame 변환 → 파일 저장 순서로 처리한다.
    raw = await collect_all()
    # API별 응답 구조가 다르므로 전용 검증 함수로 필요한 필드만 추출한다.
    # 검증에 실패한 값은 저장 단계로 넘어가지 않는다.
    weather = validate_weather(raw["weather"])
    country = validate_country(raw["country"])
    ip_info = validate_ip(raw["ip"])

    # 모델을 dict로 바꾼 뒤 DataFrame으로 변환하면 CSV와 Parquet에
    # 동일한 컬럼 구조로 저장할 수 있다.
    weather_df = pd.DataFrame([item.model_dump() for item in weather])
    metadata_df = pd.DataFrame([{**country.model_dump(), **ip_info.model_dump()}])

    # 두 데이터셋을 같은 함수로 저장해 포맷별 성능을 일관되게 비교한다.
    weather_times = save_and_benchmark(weather_df, "weather")
    metadata_times = save_and_benchmark(metadata_df, "metadata")

    print(f"검증 완료 - 서울 날씨 데이터: {len(weather_df)}건")
    print(f"검증 완료 - 메타데이터: {len(metadata_df)}건")
    print("서울 날씨 저장 성능(초):", weather_times)
    print("메타데이터 저장 성능(초):", metadata_times)


if __name__ == "__main__":
    asyncio.run(run())

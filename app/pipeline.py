# ----------------------------
# 파일명 : pipeline.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : API 응답 데이터 정제와 Pydantic 검증
# ----------------------------

from typing import Any

from app.models import CountryInfo, IpInfo, WeatherHour


def validate_weather(payload: dict[str, Any]) -> list[WeatherHour]:
    # Open-Meteo는 시간, 기온, 강수확률을 각각 배열로 반환하므로 같은
    # 위치의 값들을 하나의 시간별 모델로 묶는다.
    hourly = payload["hourly"]
    return [
        WeatherHour(
            time=time,
            temperature_2m=temperature,
            precipitation_probability=probability,
        )
        for time, temperature, probability in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["precipitation_probability"],
            strict=True,
        )
    ]


def validate_country(payload: dict[str, Any]) -> CountryInfo:
    # 국가 API마다 국가명과 국가 코드의 필드명이 다를 수 있어 여러 후보를
    # 순서대로 확인하고, 저장 전에 국가 코드를 대문자로 표준화한다.
    raw_name = payload.get("name", "South Korea")
    name = raw_name["common"] if isinstance(raw_name, dict) else raw_name
    cca3 = (
        payload.get("cca3")
        or payload.get("alpha3")
        or payload.get("alpha3Code")
        or payload.get("iso3")
        or payload.get("code")
    )
    if not cca3:
        raise ValueError(
            f"Countries.dev response has no country code. keys={list(payload)}"
        )
    return CountryInfo(name=str(name), cca3=str(cca3).upper())


def validate_ip(payload: dict[str, Any]) -> IpInfo:
    # 응답에서 저장에 필요한 위치 정보만 골라내고, 위도·경도 범위와 자료형은
    # Pydantic 모델에 맡겨 검증한다.
    return IpInfo(
        query=payload["query"],
        country=payload["country"],
        city=payload["city"],
        lat=payload["lat"],
        lon=payload["lon"],
    )

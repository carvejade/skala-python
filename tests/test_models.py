# ----------------------------
# 파일명 : test_models.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : Pydantic 모델 유효성 검증 테스트
# ----------------------------

import pytest
from pydantic import ValidationError

from app.models import IpInfo, WeatherHour


def test_weather_probability_range() -> None:
    weather = WeatherHour(
        time="2026-08-06T00:00",
        temperature_2m=25.0,
        precipitation_probability=50,
    )
    assert weather.precipitation_probability == 50


def test_invalid_weather_probability() -> None:
    with pytest.raises(ValidationError):
        WeatherHour(
            time="2026-08-06T00:00",
            temperature_2m=25.0,
            precipitation_probability=120,
        )


def test_invalid_ip_coordinates() -> None:
    with pytest.raises(ValidationError):
        IpInfo(query="8.8.8.8", country="US", city="", lat=100, lon=0)

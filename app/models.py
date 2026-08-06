# ----------------------------
# 파일명 : models.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : Pydantic 데이터 모델 정의와 필드 검증
# ----------------------------

from pydantic import BaseModel, ConfigDict, Field


class WeatherHour(BaseModel):
    """Open-Meteo의 한 시간 단위 날씨 데이터."""

    model_config = ConfigDict(extra="ignore")

    time: str
    temperature_2m: float
    precipitation_probability: int = Field(ge=0, le=100)


class CountryInfo(BaseModel):
    """Countries.dev의 한국 국가 정보에서 사용할 필드."""

    model_config = ConfigDict(extra="ignore")

    name: str
    cca3: str = Field(min_length=3, max_length=3)


class IpInfo(BaseModel):
    """ip-api 응답에서 사용할 IP 지역 정보."""

    model_config = ConfigDict(extra="ignore")

    query: str
    country: str
    city: str
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

# ----------------------------
# 파일명 : config.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : 외부 API URL 설정 관리
# ----------------------------

"""SKALA Async API Data Pipeline - 외부 설정 모듈."""

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=37.5665&longitude=126.9780&"
    "hourly=temperature_2m,precipitation_probability&"
    "forecast_days=3&timezone=Asia/Seoul"
)
COUNTRY_URL = "https://countries.dev/alpha/KOR"
IP_URL = "http://ip-api.com/json/8.8.8.8"

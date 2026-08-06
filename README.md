# Day 1 종합실습 - 비동기 API 데이터 파이프라인

서울 날씨, 한국 국가 정보, IP 지역 정보를 3개 API에서 동시에 수집하고,
Pydantic v2로 검증한 뒤 CSV와 Parquet으로 저장하는 실습 프로젝트입니다.

## 실습 목표

- `httpx.AsyncClient`와 `asyncio.gather()`를 이용한 비동기 API 수집
- Pydantic v2 모델을 이용한 타입·범위 검증
- pandas를 이용한 CSV·Parquet 파일 저장
- 두 저장 형식의 읽기·쓰기 성능 측정
- pytest 테스트와 Ruff 코드 품질 검사

## 사용 API

| 데이터 | API | 수집 내용 |
|---|---|---|
| 서울 날씨 | [Open-Meteo](https://api.open-meteo.com/v1/forecast) | 서울 3일 시간대별 기온·강수확률 |
| 한국 국가 정보 | [Countries.dev](https://countries.dev/alpha/KOR) | 국가명·ISO 국가 코드 |
| IP 지역 정보 | [ip-api](http://ip-api.com/json/8.8.8.8) | IP·국가·도시·위도·경도 |

API 주소와 쿼리 파라미터는 [app/config.py](app/config.py)에서 관리합니다.

## 처리 흐름

```text
3개 API 동시 요청
        ↓
JSON 응답 수집
        ↓
Pydantic 모델 검증
        ↓
pandas DataFrame 변환
        ↓
CSV·Parquet 저장 및 재읽기 성능 측정
```

## 환경 설정

Windows PowerShell 기준입니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 실행

프로젝트 루트에서 모듈 방식으로 실행합니다.

```powershell
python -m app.main
```

정상 실행 예시:

```text
[서울 날씨] API 연결 성공 (상태 코드: 200)
[한국 국가 정보] API 연결 성공 (상태 코드: 200)
[IP 지역 정보] API 연결 성공 (상태 코드: 200)
검증 완료 - 서울 날씨 데이터: 72건
검증 완료 - 메타데이터: 1건
서울 날씨 저장 성능(초): ...
메타데이터 저장 성능(초): ...
```

API 연결만 확인하려면 다음 명령을 사용합니다.

```powershell
python -m app.check_apis
```

## 검증 모델

- `WeatherHour`: 시간, 기온, 강수확률(0~100)
- `CountryInfo`: 국가명, 3자리 국가 코드
- `IpInfo`: IP, 국가, 도시, 위도(-90~90), 경도(-180~180)

검증에 필요한 필드만 추출하며, 범위를 벗어난 값이나 잘못된 자료형은
Pydantic 검증 예외로 처리합니다.

## 출력 파일

실행 후 다음 파일이 생성됩니다.

- `data/output/weather.csv`
- `data/output/weather.parquet`
- `data/output/metadata.csv`
- `data/output/metadata.parquet`
- `reports/execution_results.md`: 실행·성능·검사 결과 기록

CSV와 Parquet 각각에 대해 쓰기 시간과 읽기 시간을 초 단위로 출력합니다.
측정값은 네트워크와 디스크 상태에 따라 달라질 수 있습니다.

## 테스트 및 코드 검사

```powershell
pytest -q
ruff check .
```

현재 테스트는 날씨 강수확률 범위, 잘못된 날씨 값, 잘못된 IP 좌표를 검증합니다.

## 프로젝트 구조

```text
skala-python/
├─ app/
│  ├─ check_apis.py    # API 연결 확인
│  ├─ clients.py       # 비동기 API 수집
│  ├─ config.py        # API URL 설정
│  ├─ main.py          # 전체 파이프라인 실행
│  ├─ models.py        # Pydantic 모델
│  ├─ pipeline.py      # 데이터 추출·검증
│  └─ storage.py       # CSV·Parquet 저장 및 성능 측정
├─ data/output/        # 실행 결과 파일
├─ reports/            # 실행 결과 기록
├─ tests/              # pytest 테스트
├─ requirements.txt
└─ pyproject.toml
```

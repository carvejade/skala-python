# Day 1 종합실습 실행 결과

## 메인 파이프라인 실행

실행 명령:

```text
python -m app.main
```

실행 결과:

```text
[IP 지역 정보] API 연결 성공 (상태 코드: 200)
[한국 국가 정보] API 연결 성공 (상태 코드: 200)
[서울 날씨] API 연결 성공 (상태 코드: 200)
검증 완료 - 서울 날씨 데이터: 72건
검증 완료 - 메타데이터: 1건
```

## 파일 저장 및 성능 측정

### Weather

| 작업 | 소요 시간(초) |
|---|---:|
| CSV 쓰기 | 0.0022459 |
| Parquet 쓰기 | 0.0144885 |
| CSV 읽기 | 0.0009200 |
| Parquet 읽기 | 0.0223186 |

### Metadata

| 작업 | 소요 시간(초) |
|---|---:|
| CSV 쓰기 | 0.0009589 |
| Parquet 쓰기 | 0.0017030 |
| CSV 읽기 | 0.0008878 |
| Parquet 읽기 | 0.0019380 |

## 테스트 및 코드 검사

실행 명령:

```text
pytest -q
ruff check .
```

결과:

```text
3 passed in 0.08s
All checks passed!
```

## 생성된 결과 파일

- `data/output/weather.csv`
- `data/output/weather.parquet`
- `data/output/metadata.csv`
- `data/output/metadata.parquet`

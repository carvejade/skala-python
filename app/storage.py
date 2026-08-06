# ----------------------------
# 파일명 : storage.py
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : CSV/Parquet 파일 I/O와 성능 측정
# ----------------------------

from pathlib import Path
from time import perf_counter

import pandas as pd

OUTPUT_DIR = Path("data/output")


def save_and_benchmark(df: pd.DataFrame, stem: str) -> dict[str, float]:
    # 출력 폴더와 파일 경로를 먼저 준비해, 실행 위치가 프로젝트 루트일 때
    # 항상 같은 위치에 결과가 쌓이도록 한다.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / f"{stem}.csv"
    parquet_path = OUTPUT_DIR / f"{stem}.parquet"

    # 같은 DataFrame을 두 포맷으로 저장하면서 각각의 소요 시간을 측정한다.
    start = perf_counter()
    df.to_csv(csv_path, index=False)
    csv_write = perf_counter() - start

    # 저장 직후 다시 읽어 실제로 생성된 파일을 사용할 수 있는지도 확인한다.
    start = perf_counter()
    df.to_parquet(parquet_path, index=False)
    parquet_write = perf_counter() - start

    start = perf_counter()
    pd.read_csv(csv_path)
    csv_read = perf_counter() - start

    start = perf_counter()
    pd.read_parquet(parquet_path)
    parquet_read = perf_counter() - start

    return {
        "csv_write": csv_write,
        "parquet_write": parquet_write,
        "csv_read": csv_read,
        "parquet_read": parquet_read,
    }

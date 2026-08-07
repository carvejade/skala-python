"""Practice 2 쉬운 문법 예시

VS Code에서 # %% 단위로 실행하면서
Practice 2에 필요한 문법을 작은 데이터로 확인합니다.

참고
- 실습 가이드의 date 표기는 실제 제공 데이터의 필드명인
  month의 오타로 보고, 이 예시에서는 month를 사용합니다.
"""

# %% 0. 필요한 모듈

import csv
import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


# %% 1. try-except-finally 기본 구조

try:
    number = int("1000")
    print("변환 성공:", number)

except ValueError as error:
    print("변환 실패:", error)

finally:
    print("작업 종료")


# %% 2. 작은 JSON 파일 만들기

sample_file = Path("sample_sales.json")

sample_sales = [
    {
        "month": "2024-01",
        "region": "서울",
        "amount": 1500,
        "category": "전자",
    },
    {
        "month": "2024-01",
        "region": "부산",
        "amount": 800,
        "category": "의류",
    },
]

sample_file.write_text(
    json.dumps(
        sample_sales,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print(sample_file.read_text(encoding="utf-8"))


# %% 3. logging

logger.info("정상적인 처리 내용을 기록합니다.")
logger.error("오류 상황을 기록합니다.")


# %% 4. 안전한 파일 읽기

def safe_load_csv(
    file_path: str | Path,
) -> list[dict] | None:
    """JSON 파일을 안전하게 읽는다."""

    path = Path(file_path)

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        logger.info(
            "파일 로딩 성공: %s (%d건)",
            path.name,
            len(data),
        )

        return data

    except FileNotFoundError:
        logger.error(
            "파일을 찾을 수 없습니다: %s",
            path,
        )
        return None

    except json.JSONDecodeError as error:
        logger.error(
            "JSON 형식 오류: %s",
            error,
        )
        return None

    finally:
        print("로딩 종료")


loaded_sales = safe_load_csv(sample_file)

print(loaded_sales)


# %% 5. 존재하지 않는 파일

missing_result = safe_load_csv(
    "not_found.json"
)

print("없는 파일 결과:", missing_result)

assert missing_result is None


# %% 6. Pydantic 모델 정의

class SalesRecord(BaseModel):
    """판매 데이터 한 건의 검증 규칙이다."""

    month: str = Field(min_length=1)
    region: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str | None = None


# %% 7. 정상 데이터 검증

normal_row = {
    "month": "2024-01",
    "region": "서울",
    "amount": 1500,
    "category": "전자",
}

normal_record = SalesRecord.model_validate(
    normal_row
)

print(normal_record)


# %% 8. category가 없어도 정상

optional_category_row = {
    "month": "2024-02",
    "region": "부산",
    "amount": 800,
}

optional_record = SalesRecord.model_validate(
    optional_category_row
)

print(optional_record)


# %% 9. ValidationError 확인

invalid_row = {
    "month": "",
    "region": "서울",
    "amount": -100,
    "category": "전자",
}

try:
    SalesRecord.model_validate(
        invalid_row
    )

except ValidationError as error:
    print("ValidationError 발생")
    print(error)


# %% 10. valid와 errors로 분리

raw_data = [
    {
        "month": "2024-01",
        "region": "서울",
        "amount": 1500,
        "category": "전자",
    },
    {
        "month": "2024-01",
        "region": "부산",
        "amount": 800,
    },
    {
        "month": "",
        "region": "대구",
        "amount": 500,
        "category": "의류",
    },
    {
        "month": "2024-02",
        "region": "",
        "amount": 700,
        "category": "식품",
    },
]

valid = []
errors = []

for row in raw_data:
    try:
        record = SalesRecord.model_validate(
            row
        )

        valid.append(record)

    except ValidationError as error:
        errors.append({
            "row": row,
            "error": error.errors(),
        })

print("valid:", len(valid))
print("errors:", len(errors))


# %% 11. model_dump()
# Pydantic 모델을 일반 dict로 변환한다.

for record in valid:
    print(record.model_dump())


# %% 12. valid를 CSV로 저장

valid_file = Path("sample_valid.csv")

with valid_file.open(
    "w",
    encoding="utf-8",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "month",
            "region",
            "amount",
            "category",
        ],
    )

    writer.writeheader()

    writer.writerows(
        record.model_dump()
        for record in valid
    )

print(
    valid_file.read_text(
        encoding="utf-8"
    )
)


# %% 13. errors를 JSON으로 저장

error_file = Path("sample_errors.json")

with error_file.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        errors,
        file,
        ensure_ascii=False,
        indent=2,
    )

print(
    error_file.read_text(
        encoding="utf-8"
    )
)


# %% 14. CSV 재로딩

with valid_file.open(
    "r",
    encoding="utf-8",
    newline="",
) as file:

    reloaded = list(
        csv.DictReader(file)
    )

print(reloaded)
print("재로딩 건수:", len(reloaded))


# %% 15. 쉬운 예제 체크포인트

assert missing_result is None
assert len(valid) == 2
assert len(errors) == 2
assert len(reloaded) == 2

print(
    "쉬운 문법 예시의 "
    "모든 체크포인트를 통과했습니다."
)
# %%

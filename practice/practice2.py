
# ----------------------------
# 파일명 : Practice_2
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원
# 실습 내용 : 파일 I/O, 예외 처리, Pydantic 검증 파이프라인
# ----------------------------
from __future__ import annotations

import ast
import csv
import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

SOURCE_DATA_PATH = Path(__file__).with_name("Python_Practice1_Data.json")
OUTPUT_DIR = Path(__file__).with_name("practice2_output")


class SalesRecord(BaseModel):
    # month와 region은 비어 있으면 안 되고, amount는 0보다 커야 한다.
    month: str = Field(min_length=1)
    region: str = Field(min_length=1)
    amount: float = Field(gt=0)
    # category는 없어도 된다.
    category: str | None = None


def safe_load_csv(path: str | Path) -> list[dict] | None:
    """JSON, CSV, 또는 sales = [...] 형식 파일을 안전하게 읽는다.

    - 파일이 없으면 None 반환 + logger.error
    - 성공하면 dict 리스트 반환 + logger.info
    - finally에서 항상 '로딩 종료' 출력
    """
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            text = file.read().strip()

        try:
            rows = json.loads(text)
            if isinstance(rows, dict):
                rows = rows.get("sales")
            if not isinstance(rows, list):
                raise ValueError("JSON 데이터는 리스트여야 합니다.")
            logger.info("JSON 로드 성공: %d건", len(rows))
            return rows
        except json.JSONDecodeError:
            try:
                module = ast.parse(text, filename=str(path), mode="exec")
                sales_nodes = [
                    node
                    for node in module.body
                    if isinstance(node, ast.Assign)
                    and any(
                        isinstance(target, ast.Name) and target.id == "sales"
                        for target in node.targets
                    )
                ]
                if len(sales_nodes) == 1:
                    rows = ast.literal_eval(sales_nodes[0].value)
                    if not isinstance(rows, list):
                        raise ValueError("sales는 리스트여야 합니다.")
                    logger.info("파이썬 sales 로드 성공: %d건", len(rows))
                    return rows
            except SyntaxError:
                pass

            if path.suffix.lower() == ".csv":
                with path.open("r", encoding="utf-8-sig", newline="") as file:
                    rows = list(csv.DictReader(file))
                logger.info("CSV 로드 성공: %d건", len(rows))
                return rows

            raise ValueError("지원하지 않는 파일 형식입니다.")
    except FileNotFoundError:
        logger.error("파일을 찾을 수 없습니다: %s", path)
        return None
    except (OSError, ValueError) as error:
        logger.error("파일을 읽는 중 오류가 발생했습니다: %s", error)
        return None
    finally:
        print("로딩 종료")


def validate_sales_rows(raw_data: list[dict]) -> tuple[list[dict], list[dict]]:
    """raw_data를 순회하며 valid와 errors를 분리한다."""
    valid: list[dict] = []
    errors: list[dict] = []

    # 각 row를 Pydantic 모델로 검증하고, 성공/실패를 분리한다.
    for row in raw_data:
        try:
            record = SalesRecord.model_validate(row)
            # model_dump()로 검증된 데이터를 dict로 꺼낸다.
            row_data = record.model_dump()
            if row_data["category"] is None:
                row_data["category"] = ""
            valid.append(row_data)
        except ValidationError as exc:
            logger.error("ValidationError: %s", exc.errors())
            errors.append({"row": row, "error": exc.errors()})

    return valid, errors


def write_csv_rows(path: Path, records: list[dict]) -> None:
    """레코드 목록을 CSV로 저장한다."""
    fieldnames = ["month", "region", "amount", "category"]

    # 저장할 컬럼 순서를 고정해서 CSV를 쓴다.
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def save_errors(path: Path, errors: list[dict]) -> None:
    """errors를 JSON으로 저장한다."""
    # 한글이 깨지지 않도록 ensure_ascii=False로 저장한다.
    with path.open("w", encoding="utf-8") as file:
        json.dump(errors, file, ensure_ascii=False, indent=2)


def make_raw_data(source_sales: list[dict]) -> list[dict]:
    """원본 데이터 일부를 이용해 valid 4건, errors 3건을 만든다."""
    return [
        {
            "month": source_sales[0]["month"],
            "region": source_sales[0]["region"],
            "amount": source_sales[0]["amount"],
            "category": source_sales[0]["category"],
        },
        {
            "month": source_sales[1]["month"],
            "region": source_sales[1]["region"],
            "amount": source_sales[1]["amount"],
        },
        {
            "month": source_sales[2]["month"],
            "region": source_sales[2]["region"],
            "amount": source_sales[2]["amount"],
            "category": source_sales[2]["category"],
        },
        {
            "month": source_sales[3]["month"],
            "region": source_sales[3]["region"],
            "amount": source_sales[3]["amount"],
            "category": source_sales[3]["category"],
        },
        {
            "month": "",
            "region": source_sales[4]["region"],
            "amount": source_sales[4]["amount"],
            "category": source_sales[4]["category"],
        },
        {
            "month": source_sales[5]["month"],
            "region": "",
            "amount": source_sales[5]["amount"],
            "category": source_sales[5]["category"],
        },
        {
            "month": source_sales[6]["month"],
            "region": source_sales[6]["region"],
            "amount": 0,
            "category": source_sales[6]["category"],
        },
    ]


def main() -> None:
    # --------------------------------------------------------
    # 1번 : 예외 처리 + 파일 읽기
    # 파일 없음 처리, 원본 데이터 로딩, 입력 JSON 생성, 재로딩 확인
    # --------------------------------------------------------
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 파일이 없을 때 None이 반환되는지 확인한다.
    missing_path = OUTPUT_DIR / "missing_sales.json"
    assert safe_load_csv(missing_path) is None

    # 실제 원본 파일을 읽는다.
    source_rows = safe_load_csv(SOURCE_DATA_PATH)
    if source_rows is None:
        raise ValueError("원본 데이터를 읽지 못했습니다.")
    logger.info("원본 데이터 로드 성공: %d건", len(source_rows))

    # 입력 파일은 이름만 .csv이고, 내용은 JSON으로 저장한다.
    input_path = OUTPUT_DIR / "sales_input.csv"
    raw_data = make_raw_data(source_rows)
    with input_path.open("w", encoding="utf-8") as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=2)

    loaded_rows = safe_load_csv(input_path)
    assert loaded_rows is not None

    # --------------------------------------------------------
    # 2번 : Pydantic v2 스키마 정의 + 검증 파이프라인
    # 로드한 데이터를 SalesRecord로 검증해 valid / errors로 분리
    # --------------------------------------------------------
    valid, errors = validate_sales_rows(loaded_rows)
    assert len(valid) == 4
    assert len(errors) == 3

    # --------------------------------------------------------
    # 3번 : 결과 파일 저장
    # valid는 CSV로, errors는 JSON으로 저장
    # --------------------------------------------------------
    valid_path = OUTPUT_DIR / "valid_sales.csv"
    errors_path = OUTPUT_DIR / "validation_errors.json"
    write_csv_rows(valid_path, valid)
    save_errors(errors_path, errors)

    # --------------------------------------------------------
    # 4번 : 재로딩 확인
    # 저장한 valid CSV를 다시 읽어서 건수 검증
    # --------------------------------------------------------
    reloaded = safe_load_csv(valid_path)
    assert reloaded is not None
    assert len(reloaded) == 4

    print("valid 건수:", len(valid))
    print("errors 건수:", len(errors))
    print("재로딩 건수:", len(reloaded))
    print("저장 경로:", valid_path)
    print("오류 경로:", errors_path)


if __name__ == "__main__":
    main()

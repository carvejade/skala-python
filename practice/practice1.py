# ----------------------------
# 파일명 : Practice_1
# 작성일자 : 2026.08.06
# 작성자 : P329 서지원 
# 데이터 분석을 위한 Python 이해
# ----------------------------

import ast
import json
from collections import Counter, defaultdict
from pathlib import Path
from sys import getsizeof


data_path = Path(__file__).with_name("Python_Practice1_Data.json")


def load_sales(path):
    text = path.read_text(encoding="utf-8-sig").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        module = ast.parse(text, filename=str(path), mode="exec")
        sales_nodes = [
            node
            for node in module.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "sales" for target in node.targets)
        ]
        if len(sales_nodes) != 1:
            raise ValueError("sales 데이터를 찾지 못했습니다.")
        data = ast.literal_eval(sales_nodes[0].value)

    if isinstance(data, dict):
        data = data.get("sales")

    if not isinstance(data, list):
        raise ValueError("sales는 리스트여야 합니다.")

    return data


def high_value_sales(rows, threshold=1000):
    # amount가 threshold보다 큰 거래만 하나씩 yield한다.
    for sale in rows:
        if sale["amount"] > threshold:
            yield sale


def build_region_total(sales):
    # amount >= 1000 인 거래만 모은 뒤 지역별 총매출을 구한다.
    filtered_sales = [sale for sale in sales if sale["amount"] >= 1000]
    return {
        region: sum(
            sale["amount"] for sale in filtered_sales if sale["region"] == region
        )
        for region in sorted({sale["region"] for sale in filtered_sales})
    }, filtered_sales


def build_counter_and_category_lists(sales):
    # 지역별 거래 건수는 Counter로, 카테고리별 amount 목록은 defaultdict로 만든다.
    region_counts = Counter(sale["region"] for sale in sales)
    amounts_by_category = defaultdict(list)

    for sale in sales:
        amounts_by_category[sale["category"]].append(sale["amount"])

    return region_counts, amounts_by_category


def build_generator_memory_report(sales):
    # 리스트와 제너레이터의 메모리 크기를 비교한다.
    high_sales_list = [sale for sale in sales if sale["amount"] > 1000]
    high_sales_gen = high_value_sales(sales)
    top3_sales = sorted(sales, key=lambda sale: sale["amount"], reverse=True)[:3]

    return {
        "high_sales_count": len(high_sales_list),
        "list_size": getsizeof(high_sales_list),
        "generator_size": getsizeof(high_sales_gen),
        "top3_sales": top3_sales,
    }


def build_month_category_sales(sales):
    # month와 category 기준으로 총매출을 집계한다.
    monthly_category_sales = defaultdict(lambda: defaultdict(int))

    for sale in sales:
        monthly_category_sales[sale["month"]][sale["category"]] += sale["amount"]

    return {
        month: {
            category: total
            for category, total in sorted(category_totals.items())
        }
        for month, category_totals in sorted(monthly_category_sales.items())
    }


def main():
    sales = load_sales(data_path)

    # 1) 리스트 / 딕셔너리 컴프리헨션
    region_total, filtered_sales = build_region_total(sales)

    # 2) Counter + defaultdict
    region_counts, amounts_by_category = build_counter_and_category_lists(sales)

    # 3) 제너레이터 - 메모리 비교
    memory_report = build_generator_memory_report(sales)

    # 4) 종합 - 월별 카테고리 매출 집계
    monthly_category_sales = build_month_category_sales(sales)

    print("1) 리스트 / 딕셔너리 컴프리헨션")
    print("   amount >= 1000 거래 수:", len(filtered_sales))
    print("   지역별 총매출:", region_total)

    print("2) Counter + defaultdict")
    print("   지역별 거래 건수:", region_counts)
    print("   카테고리별 amount 리스트:", dict(amounts_by_category))

    print("3) 제너레이터 - 메모리 비교")
    print("   amount > 1000 거래 수(리스트):", memory_report["high_sales_count"])
    print("   리스트 크기(bytes):", memory_report["list_size"])
    print("   제너레이터 크기(bytes):", memory_report["generator_size"])
    print("   top3 금액 내림차순:", memory_report["top3_sales"])

    print("4) 종합 - 월별 카테고리 매출 집계")
    print("   월별 카테고리 매출:", monthly_category_sales)


if __name__ == "__main__":
    main()

"""Practice 1 쉬운 문법 예시

VS Code에서 # %% 단위로 실행하면서
Practice 1에 필요한 문법을 작은 데이터로 확인합니다.
"""

# %% 0. 필요한 모듈
import sys
from collections import Counter, defaultdict

# %% 1. 리스트 컴프리헨션
# 조건에 맞는 값만 새로운 리스트로 만든다.

numbers = [100, 500, 1200, 2000]

filtered_numbers = [
    number
    for number in numbers
    if number >= 1000
]

print(filtered_numbers)
# [1200, 2000]


# %% 2. 리스트 컴프리헨션을 일반 for문으로 풀어보기
# 위 코드가 실제로 어떤 흐름인지 확인한다.

filtered_numbers_for = []

for number in numbers:
    if number >= 1000:
        filtered_numbers_for.append(number)

print(filtered_numbers_for)

assert filtered_numbers == filtered_numbers_for


# %% 3. 집합 컴프리헨션
# 중복된 값을 제거한다.

region_names = [
    "서울",
    "부산",
    "서울",
    "대구",
    "부산",
]

unique_regions = {
    region
    for region in region_names
}

print(unique_regions)


# %% 4. 딕셔너리 컴프리헨션
# 반복하면서 key: value 구조를 만든다.

region_zero = {
    region: 0
    for region in unique_regions
}

print(region_zero)


# %% 5. 연습용 판매 데이터
# 이후 예제에서 공통으로 사용할 작은 데이터다.

sales = [
    {
        "region": "서울",
        "category": "전자",
        "amount": 1000,
        "month": "2024-01",
    },
    {
        "region": "부산",
        "category": "식품",
        "amount": 800,
        "month": "2024-01",
    },
    {
        "region": "서울",
        "category": "전자",
        "amount": 1500,
        "month": "2024-02",
    },
    {
        "region": "대구",
        "category": "의류",
        "amount": 1200,
        "month": "2024-02",
    },
]

print("거래 수:", len(sales))
print("첫 번째 거래:", sales[0])


# %% 6. 실제 데이터 구조에서 리스트 컴프리헨션
# amount >= 1000인 거래만 선택한다.

high_amount_sales = [
    sale
    for sale in sales
    if sale["amount"] >= 1000
]

print(high_amount_sales)


# %% 7. 조건에 맞는 값의 합계
# 서울 거래의 amount만 골라 합산한다.

seoul_total = sum(
    sale["amount"]
    for sale in sales
    if sale["region"] == "서울"
)

print("서울 총매출:", seoul_total)
# 2500


# %% 8. 지역별 총매출 계산
# 집합 컴프리헨션으로 지역을 추출하고,
# 딕셔너리 컴프리헨션으로 지역별 합계를 만든다.

regions = {
    sale["region"]
    for sale in sales
}

region_total = {
    region: sum(
        sale["amount"]
        for sale in sales
        if sale["region"] == region
    )
    for region in regions
}

print(region_total)


# %% 9. 지역별 총매출을 일반 for문으로 풀어보기
# 딕셔너리 컴프리헨션이 어려울 때 흐름을 확인한다.

region_total_for = {}

for region in regions:
    total = sum(
        sale["amount"]
        for sale in sales
        if sale["region"] == region
    )

    region_total_for[region] = total

print(region_total_for)

assert region_total == region_total_for


# %% 10. Counter
# 지역 이름이 몇 번 등장하는지 계산한다.

region_count = Counter(
    sale["region"]
    for sale in sales
)

print(region_count)
print(region_count.most_common())


# %% 11. defaultdict(list)
# 처음 등장하는 카테고리에도 빈 리스트가 자동으로 생성된다.

category_amounts = defaultdict(list)

for sale in sales:
    category = sale["category"]
    amount = sale["amount"]

    category_amounts[category].append(amount)

print(dict(category_amounts))


# %% 12. 일반 dict를 사용할 경우와 비교
# defaultdict가 없다면 key 존재 여부를 직접 검사해야 한다.

category_amounts_normal = {}

for sale in sales:
    category = sale["category"]
    amount = sale["amount"]

    if category not in category_amounts_normal:
        category_amounts_normal[category] = []

    category_amounts_normal[category].append(amount)

print(category_amounts_normal)

assert dict(category_amounts) == category_amounts_normal


# %% 13. 제너레이터 함수
# yield를 사용하면 값을 요청할 때 하나씩 반환한다.

def generate_high_amount(
    data,
    threshold=1000,
):
    for sale in data:
        if sale["amount"] > threshold:
            yield sale


generator_result = generate_high_amount(sales)

print(generator_result)
print(type(generator_result))


# %% 14. next()로 제너레이터 값 확인
# next()가 호출되는 순간 함수 본문이 실행된다.

generator_for_debug = generate_high_amount(sales)

first_item = next(generator_for_debug)
print("첫 번째 값:", first_item)

second_item = next(generator_for_debug)
print("두 번째 값:", second_item)


# %% 15. 리스트와 제너레이터 메모리 비교

list_result = [
    sale
    for sale in sales
    if sale["amount"] > 1000
]

generator_result = generate_high_amount(sales)

list_size = sys.getsizeof(list_result)
generator_size = sys.getsizeof(generator_result)

print("리스트 크기:", list_size, "bytes")
print("제너레이터 크기:", generator_size, "bytes")
print("제너레이터가 더 작은가:", generator_size < list_size)

# 주의: 이렇게 작은 데이터에서는 결과가 False로 나올 수 있다.
# 제너레이터 객체 자체가 고정 오버헤드(약 200바이트)를 가지기 때문에,
# 걸러진 원소가 몇 개뿐이면 리스트가 오히려 더 작다.
# 리스트는 원소가 늘수록 메모리가 함께 커지지만
# 제너레이터는 값을 한 건씩 만들어 메모리가 거의 일정하다.
# 실제 체크포인트(generator < list)는 아래 대량 데이터 셀에서 확인한다.


# %% 15-2. 대량 데이터에서 메모리 차이 확인
# 데이터를 크게 늘리면 리스트만 메모리가 커지고,
# 제너레이터 크기는 거의 그대로여서 generator < list가 성립한다.

large_sales = sales * 10000  # 4건 -> 40,000건

large_list = [
    sale
    for sale in large_sales
    if sale["amount"] > 1000
]

large_generator = generate_high_amount(large_sales)

large_list_size = sys.getsizeof(large_list)
large_generator_size = sys.getsizeof(large_generator)

print("대량 리스트 크기:", large_list_size, "bytes")
print("대량 제너레이터 크기:", large_generator_size, "bytes")

assert large_generator_size < large_list_size

print("대량 데이터 메모리 체크 통과")


# %% 16. 제너레이터 결과 검증
# 메모리 비교와 별도로 새 제너레이터를 리스트로 변환한다.

generated_sales = list(
    generate_high_amount(sales)
)

print(generated_sales)

assert generated_sales == list_result


# %% 17. defaultdict(int)
# 존재하지 않는 key를 처음 사용할 때 0이 자동 생성된다.

month_category_total = defaultdict(int)

for sale in sales:
    key = (
        sale["month"],
        sale["category"],
    )

    month_category_total[key] += sale["amount"]

print(dict(month_category_total))


# %% 18. 튜플 key 확인
# key는 (month, category), value는 총매출이다.

for key, total in month_category_total.items():
    print("key:", key, "/ total:", total)


# %% 19. sorted()로 내림차순 정렬

sorted_result = sorted(
    month_category_total.items(),
    key=lambda item: item[1],
    reverse=True,
)

print(sorted_result)


# %% 20. 상위 3개만 선택

top3 = sorted(
    month_category_total.items(),
    key=lambda item: item[1],
    reverse=True,
)[:3]

print(top3)


# %% 21. Top 3 출력 구조 풀어보기

for rank, item in enumerate(
    top3,
    start=1,
):
    key, amount = item
    month, category = key

    print(
        f"{rank}위: "
        f"{month} / {category} / {amount}"
    )


# %% 22. assert
# 계산 결과가 예상한 값 또는 조건과 일치하는지 검사한다.

assert filtered_numbers == [1200, 2000]
assert seoul_total == 2500
assert region_count["서울"] == 2
assert dict(category_amounts)["전자"] == [1000, 1500]
# generator < list 검증은 대량 데이터 셀(15-2)에서 수행한다.

top3_amounts = [
    amount
    for _, amount in top3
]

assert top3_amounts == sorted(
    top3_amounts,
    reverse=True,
)

print("모든 쉬운 문법 예시를 통과했습니다.")


# %% 23. 간단한 예외 처리
# 정상적인 문자열은 정수로 변환된다.

try:
    value = int("1000")
    print("변환 결과:", value)

except ValueError as error:
    print("숫자로 변환할 수 없습니다:", error)


# %% 24. 예외가 발생하는 경우 확인
# "천원"은 int로 변환할 수 없으므로 ValueError가 발생한다.

try:
    value = int("천원")
    print("변환 결과:", value)

except ValueError as error:
    print("숫자로 변환할 수 없습니다:", error)


# %% 25. 파일 로딩·검증·예외 처리 미니 예제
# 실제 평가에서 예외/오류 처리 비중이 크므로,
# 파일을 안전하게 읽고 형식을 검사하는 흐름을 미리 연습한다.

import ast
import json
from pathlib import Path

sample_path = Path("sample_practice1_data.json")

sample_path.write_text(
    json.dumps(sales, ensure_ascii=False, indent=2),
    encoding="utf-8",
)


def load_sales(
    file_path: str | Path,
) -> list[dict] | None:
    """판매 데이터를 읽고 기본 형식을 검사한다."""

    path = Path(file_path)

    try:
        text = path.read_text(encoding="utf-8")

        try:
            # 정상 JSON 배열
            data = json.loads(text)

        except json.JSONDecodeError:
            # sales = [...] 형식
            variable_name, separator, value_text = text.partition("=")

            if not separator or variable_name.strip() != "sales":
                raise ValueError("지원하지 않는 파일 형식입니다.")

            data = ast.literal_eval(value_text.strip())

        if not isinstance(data, list):
            raise TypeError("전체 데이터는 리스트여야 합니다.")

        required_fields = {"month", "region", "category", "amount"}

        for index, row in enumerate(data, start=1):
            if not isinstance(row, dict):
                raise TypeError(f"{index}번째 데이터가 딕셔너리가 아닙니다.")

            missing_fields = required_fields - row.keys()

            if missing_fields:
                raise ValueError(
                    f"{index}번째 데이터의 필수 필드 누락: {missing_fields}"
                )

            if not isinstance(row["amount"], (int, float)):
                raise TypeError(f"{index}번째 amount는 숫자여야 합니다.")

        print(f"파일 로딩 성공: {len(data)}건")

        return data

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None

    except (OSError, SyntaxError, TypeError, ValueError) as error:
        print("데이터 로딩 실패:", error)
        return None


# %% 26. 파일 로딩 체크포인트
# 정상 파일은 데이터를 반환하고, 없는 파일은 None을 반환한다.

loaded_sales = load_sales(sample_path)

assert loaded_sales is not None
assert len(loaded_sales) == len(sales)

missing_sales = load_sales("not_found_practice1.json")

assert missing_sales is None

print("파일 로딩·검증 예제 통과")
# %%

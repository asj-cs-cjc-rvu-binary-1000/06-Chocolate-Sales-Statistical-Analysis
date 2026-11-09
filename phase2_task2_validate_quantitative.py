import csv
import math
from collections import defaultdict

dataset_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

numeric_columns = [
    "quantity",
    "unit_price",
    "discount",
    "revenue",
    "cost",
    "profit",
    "cocoa_percent",
    "weight_g",
    "age"
]

with open(
    dataset_path,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    records = list(reader)

if headers is None:
    raise ValueError("Dataset headers are missing.")

missing_columns = [
    column for column in numeric_columns
    if column not in headers
]

if missing_columns:
    raise ValueError(
        f"Required numerical columns missing: {missing_columns}"
    )

values = defaultdict(list)
invalid_numeric = defaultdict(list)
missing_numeric = defaultdict(list)

for row_number, row in enumerate(records, start=2):
    for column in numeric_columns:
        raw_value = row[column]

        if raw_value is None or raw_value.strip() == "":
            missing_numeric[column].append(row_number)
            continue

        try:
            number = float(raw_value)
            if not math.isfinite(number):
                raise ValueError("Non-finite number")
            values[column].append(number)
        except (ValueError, TypeError):
            invalid_numeric[column].append(
                (row_number, raw_value)
            )

print("=" * 70)
print("PHASE 2 - TASK 2: QUANTITATIVE VARIABLE VALIDATION")
print("=" * 70)

print(f"\nDataset records: {len(records)}")
print(f"Quantitative variables checked: {len(numeric_columns)}")

print("\nNUMERICAL SUMMARY")
print("-" * 70)

for column in numeric_columns:
    column_values = values[column]

    if column_values:
        print(
            f"{column:15} "
            f"Min: {min(column_values):12.4f} "
            f"Max: {max(column_values):12.4f} "
            f"Valid: {len(column_values)}"
        )
    else:
        print(f"{column:15} No valid numerical values")

print("\nMISSING AND NON-NUMERIC VALUE CHECK")
print("-" * 70)

for column in numeric_columns:
    print(
        f"{column:15} "
        f"Missing: {len(missing_numeric[column]):3} | "
        f"Invalid: {len(invalid_numeric[column]):3}"
    )

checks = {}

# Every quantitative field must be numeric and non-missing.
for column in numeric_columns:
    checks[f"{column} contains no missing values"] = (
        len(missing_numeric[column]) == 0
    )
    checks[f"{column} contains only valid finite numbers"] = (
        len(invalid_numeric[column]) == 0
    )

# Specific logical checks.
checks["Quantity contains positive whole numbers"] = (
    bool(values["quantity"])
    and all(
        value > 0 and value.is_integer()
        for value in values["quantity"]
    )
)

checks["Unit price contains only positive values"] = (
    bool(values["unit_price"])
    and all(value > 0 for value in values["unit_price"])
)

checks["Revenue contains only positive values"] = (
    bool(values["revenue"])
    and all(value > 0 for value in values["revenue"])
)

# Discounts may be stored as fractions or percentages.
discount_values = values["discount"]
discount_scale = (
    "fraction (0 to 1)"
    if discount_values and max(discount_values) <= 1
    else "percentage (0 to 100)"
)

checks["Discount values are within 0 to 100"] = (
    bool(discount_values)
    and all(0 <= value <= 100 for value in discount_values)
)

checks["Age values are between 18 and 100"] = (
    bool(values["age"])
    and all(18 <= value <= 100 for value in values["age"])
)

checks["Cocoa percentage values are between 0 and 100"] = (
    bool(values["cocoa_percent"])
    and all(0 <= value <= 100 for value in values["cocoa_percent"])
)

checks["Weight values are positive"] = (
    bool(values["weight_g"])
    and all(value > 0 for value in values["weight_g"])
)

checks["Cost values are positive"] = (
    bool(values["cost"])
    and all(value > 0 for value in values["cost"])
)

print("\nLOGICAL VALIDATION CHECKS")
print("-" * 70)
print(f"Discount storage scale detected: {discount_scale}")

for description, passed in checks.items():
    print(
        f"{description}: "
        f"{'PASS' if passed else 'REVIEW'}"
    )

# Show examples if any logical checks fail.
if not all(checks.values()):
    print("\nVALIDATION DETAILS FOR REVIEW")

    for column in numeric_columns:
        if missing_numeric[column]:
            print(
                f"{column}: missing at CSV rows "
                f"{missing_numeric[column][:10]}"
            )

        if invalid_numeric[column]:
            print(
                f"{column}: invalid examples "
                f"{invalid_numeric[column][:10]}"
            )

    for column, condition in [
        ("quantity", lambda x: x <= 0 or not x.is_integer()),
        ("unit_price", lambda x: x <= 0),
        ("revenue", lambda x: x <= 0),
        ("discount", lambda x: x < 0 or x > 100),
        ("age", lambda x: x < 18 or x > 100),
        ("cocoa_percent", lambda x: x < 0 or x > 100),
        ("weight_g", lambda x: x <= 0),
        ("cost", lambda x: x <= 0)
    ]:
        invalid_values = [
            value for value in values[column]
            if condition(value)
        ]
        if invalid_values:
            print(
                f"{column}: invalid values "
                f"{invalid_values[:10]}"
            )

    print("\nTASK 2 VALIDATION: REVIEW REQUIRED")
    raise SystemExit(1)

print("\nTASK 2 VALIDATION: ALL CHECKS PASSED")
print("Original sampled dataset: NOT MODIFIED")
print("=" * 70)

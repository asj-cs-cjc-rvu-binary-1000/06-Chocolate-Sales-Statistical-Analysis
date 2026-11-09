import csv
import os
from collections import Counter

dataset_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

decision_path = "docs/cleaning_decisions.md"

# --------------------------------------------------
# 1. Read original sampled dataset
# --------------------------------------------------

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

required = [
    "order_id",
    "product_id",
    "category",
    "brand"
]

missing_columns = [
    column for column in required
    if column not in headers
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )

# --------------------------------------------------
# 2. Identify missing qualitative values
# --------------------------------------------------

def is_missing(value):
    return value is None or value.strip() == ""

missing_category = [
    row for row in records
    if is_missing(row["category"])
]

missing_brand = [
    row for row in records
    if is_missing(row["brand"])
]

affected_records = [
    row for row in records
    if (
        is_missing(row["category"])
        or is_missing(row["brand"])
    )
]

both_missing = [
    row for row in records
    if (
        is_missing(row["category"])
        and is_missing(row["brand"])
    )
]

# --------------------------------------------------
# 3. Print dataset and missing-value summary
# --------------------------------------------------

print("=" * 65)
print("PHASE 2 - TASK 1: MISSING VALUE INVESTIGATION")
print("=" * 65)

print(f"\nOriginal dataset records: {len(records)}")
print(f"Original dataset variables: {len(headers)}")

print("\nMISSING VALUE SUMMARY")
print(f"Missing category: {len(missing_category)}")
print(f"Missing brand: {len(missing_brand)}")
print(f"Both category and brand missing: {len(both_missing)}")
print(f"Unique affected transactions: {len(affected_records)}")

# --------------------------------------------------
# 4. Inspect affected product records
# --------------------------------------------------

print("\nAFFECTED TRANSACTIONS")
print("-" * 65)

for row in affected_records:
    print(
        f"Order ID: {row['order_id']} | "
        f"Product ID: {row['product_id']} | "
        f"Category: {row['category'] or '[MISSING]'} | "
        f"Brand: {row['brand'] or '[MISSING]'}"
    )

# --------------------------------------------------
# 5. Count affected product IDs
# --------------------------------------------------

product_counts = Counter(
    row["product_id"]
    for row in affected_records
)

print("\nAFFECTED PRODUCT ID FREQUENCIES")

for product_id, count in sorted(product_counts.items()):
    print(f"{product_id}: {count} transaction(s)")

# --------------------------------------------------
# 6. Verify consistency with expected findings
# --------------------------------------------------

print("\nINVESTIGATION CHECKS")

checks = {
    "Exactly 8 missing category values":
        len(missing_category) == 8,

    "Exactly 8 missing brand values":
        len(missing_brand) == 8,

    "Exactly 8 affected transactions":
        len(affected_records) == 8,

    "All 8 affected transactions have both fields missing":
        len(both_missing) == 8
}

for description, passed in checks.items():
    print(
        f"{description}: "
        f"{'PASS' if passed else 'REVIEW'}"
    )

# --------------------------------------------------
# 7. Record selected cleaning decision
# --------------------------------------------------

if not all(checks.values()):
    print("\nINVESTIGATION REQUIRES REVIEW.")
    print("No cleaning decision has been documented.")
    raise SystemExit(1)

os.makedirs("docs", exist_ok=True)

decision_document = """# Data Cleaning Decisions

## Phase 2 – Task 1: Missing Qualitative Values

### Problem Identified

The original sampled dataset contains 1,000 transactions.

Investigation identified:
- Missing values in category: 8
- Missing values in brand: 8
- Unique affected transactions: 8
- Transactions missing both fields: 8

### Investigation of Affected Records

The affected transactions and their product IDs were
printed during the Task 1 investigation.

These records have missing product descriptions because
their product IDs could not be matched to the product
reference dataset during Phase 0.

### Cleaning Decision: Option A – Remove Affected Rows

The eight affected transactions will be excluded from
the final cleaned analysis dataset.

Justification:

1. Both category and brand are unavailable for these
   transactions.
2. The missing product information cannot be reliably
   reconstructed from the available reference data.
3. Retaining these records with invented product labels
   could distort category and brand frequency tables.
4. Removing these eight records provides a dataset with
   valid product category and brand information.

### Data Integrity

The original sampled dataset will remain unchanged.

The eight rows will be excluded only when creating the
separate cleaned dataset in Phase 2, Task 4.

No raw CSV files will be modified.

### Expected Effect

Original sampled records: 1,000
Rows selected for exclusion: 8
Expected cleaned records: 992

This expected count will be verified when the cleaned
dataset is created.

### Other Cleaning Tasks

Quantitative validation and categorical label
standardisation will be documented after their
respective investigations.
"""

with open(
    decision_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(decision_document)

# --------------------------------------------------
# 8. Final output
# --------------------------------------------------

print("\nCLEANING DECISION")
print("Option A: Remove the 8 affected transactions.")
print("Original sampled dataset: NOT MODIFIED")
print("Rows deleted at this stage: 0")

print(f"\nDocumentation created: {decision_path}")
print(f"Documentation size: {os.path.getsize(decision_path):,} bytes")

print("\nTASK 1 INVESTIGATION: SUCCESS")
print("=" * 65)

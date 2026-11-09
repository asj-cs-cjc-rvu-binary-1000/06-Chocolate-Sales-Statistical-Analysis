import csv
import os

input_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

output_path = (
    "data/processed/"
    "chocolate_sales_clean.csv"
)

def is_missing(value):
    return value is None or value.strip() == ""

# Read original sampled dataset.
with open(
    input_path,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    records = list(reader)

if headers is None:
    raise ValueError("Input dataset has no headers.")

if len(records) != 1000:
    raise ValueError(
        f"Expected 1,000 records, found {len(records)}."
    )

# Identify records selected for exclusion in Task 1.
affected_records = [
    row for row in records
    if (
        is_missing(row["category"])
        or is_missing(row["brand"])
    )
]

# Confirm the affected records match Tasks 1 and 2.
if len(affected_records) != 8:
    raise ValueError(
        f"Expected 8 affected records, found {len(affected_records)}."
    )

for row in affected_records:
    if not (
        is_missing(row["category"])
        and is_missing(row["brand"])
        and is_missing(row["product_name"])
        and is_missing(row["cocoa_percent"])
        and is_missing(row["weight_g"])
    ):
        raise ValueError(
            "Affected record does not match the verified "
            "missing-product pattern: "
            f"{row['order_id']}"
        )

affected_product_ids = {
    row["product_id"] for row in affected_records
}

if affected_product_ids != {"P0000", "P0201"}:
    raise ValueError(
        "Unexpected affected product IDs: "
        f"{sorted(affected_product_ids)}"
    )

# Retain all records not selected for exclusion.
clean_records = [
    row for row in records
    if row not in affected_records
]

# Confirm expected cleaned row count.
if len(clean_records) != 992:
    raise ValueError(
        f"Expected 992 cleaned records, found {len(clean_records)}."
    )

# Verify that all retained fields are complete.
missing_values = []

for row in clean_records:
    for column in headers:
        if is_missing(row[column]):
            missing_values.append(
                (row["order_id"], column)
            )

if missing_values:
    print("Remaining missing values:")
    for item in missing_values[:20]:
        print(item)

    raise ValueError(
        f"Found {len(missing_values)} missing values "
        "in the proposed cleaned dataset."
    )

# Write the cleaned dataset as a plain CSV.
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(
    output_path,
    "w",
    encoding="utf-8",
    newline=""
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=headers
    )
    writer.writeheader()
    writer.writerows(clean_records)

# Reopen and independently verify the saved CSV.
with open(
    output_path,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)
    saved_headers = reader.fieldnames
    saved_records = list(reader)

assert saved_headers == headers
assert len(saved_records) == 992

remaining_missing = sum(
    1
    for row in saved_records
    for column in saved_headers
    if is_missing(row[column])
)

assert remaining_missing == 0

print("=" * 70)
print("PHASE 2 - TASK 4: CREATE CLEANED DATASET")
print("=" * 70)

print(f"Original sampled records: {len(records)}")
print(f"Records excluded: {len(affected_records)}")
print(f"Excluded product IDs: {sorted(affected_product_ids)}")
print(f"Cleaned dataset records: {len(saved_records)}")
print(f"Number of variables: {len(saved_headers)}")
print(f"Remaining missing/empty values: {remaining_missing}")
print(f"Output file: {output_path}")
print(
    f"Output file size: "
    f"{os.path.getsize(output_path):,} bytes"
)

print("\nVERIFICATION CHECKS")
print("Original row count is 1,000: PASS")
print("Exactly 8 records excluded: PASS")
print("Cleaned row count is 992: PASS")
print("All 24 columns preserved: PASS")
print("No missing or empty values: PASS")
print("Saved CSV independently verified: PASS")

print("\nOriginal sampled dataset: NOT MODIFIED")
print("TASK 4: SUCCESS")
print("=" * 70)

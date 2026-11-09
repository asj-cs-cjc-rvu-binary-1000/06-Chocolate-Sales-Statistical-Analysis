import csv
from collections import Counter, defaultdict

dataset_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

categorical_columns = [
    "product_name",
    "brand",
    "category",
    "gender",
    "loyalty_member",
    "store_name",
    "city",
    "country",
    "store_type"
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
    column for column in categorical_columns
    if column not in headers
]

if missing_columns:
    raise ValueError(
        f"Required categorical columns missing: {missing_columns}"
    )

print("=" * 75)
print("PHASE 2 - TASK 3: CATEGORICAL LABEL INSPECTION")
print("=" * 75)

print(f"\nDataset records: {len(records)}")

variant_groups = {}
issues_found = False

for column in categorical_columns:
    frequencies = Counter(
        row[column].strip()
        for row in records
        if row[column] is not None and row[column].strip() != ""
    )

    missing_count = sum(
        1 for row in records
        if row[column] is None or row[column].strip() == ""
    )

    normalized_groups = defaultdict(list)

    for label in frequencies:
        normalized_groups[label.casefold()].append(label)

    variants = {
        key: labels
        for key, labels in normalized_groups.items()
        if len(labels) > 1
    }

    whitespace_count = sum(
        1 for row in records
        if row[column] is not None
        and row[column] != row[column].strip()
    )

    variant_groups[column] = variants

    print("\n" + "=" * 75)
    print(f"COLUMN: {column}")
    print("=" * 75)

    print(f"Distinct non-empty labels: {len(frequencies)}")
    print(f"Missing/empty values: {missing_count}")
    print(f"Values with surrounding whitespace: {whitespace_count}")

    print("\nFREQUENCY TABLE")

    for label, count in sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0].casefold())
    ):
        print(f"{label}: {count}")

    print("\nPOSSIBLE CAPITALIZATION VARIANTS")

    if variants:
        issues_found = True

        for normalized, labels in sorted(variants.items()):
            print(
                f"Possible equivalent labels: "
                f"{[(label, frequencies[label]) for label in labels]}"
            )
    else:
        print("None detected.")

    if whitespace_count:
        issues_found = True
        print(
            "\nNOTICE: Some original values contain "
            "leading or trailing whitespace."
        )

print("\n" + "=" * 75)
print("FOCUSED CATEGORY CHECKS")
print("=" * 75)

for column in ["gender", "country", "store_type", "loyalty_member"]:
    labels = sorted({
        row[column].strip()
        for row in records
        if row[column] is not None and row[column].strip() != ""
    })

    print(f"\n{column}: {labels}")

print("\n" + "=" * 75)
print("INSPECTION SUMMARY")
print("=" * 75)

if issues_found:
    print("Potential label inconsistencies require review.")
else:
    print("No capitalization or whitespace inconsistencies detected.")

print(
    "\nOriginal sampled dataset: NOT MODIFIED"
)
print("No categorical values have been changed yet.")
print("=" * 75)

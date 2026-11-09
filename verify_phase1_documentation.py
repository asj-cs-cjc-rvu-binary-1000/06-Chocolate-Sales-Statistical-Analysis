import csv
import os
import sys

dataset_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

dictionary_path = "docs/data_dictionary.md"
analysis_path = "docs/analysis_plan.md"

# --------------------------------------------------
# 1. Read dataset headers
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

# --------------------------------------------------
# 2. Read documentation
# --------------------------------------------------

for path in [dictionary_path, analysis_path]:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

with open(dictionary_path, encoding="utf-8") as file:
    dictionary = file.read()

with open(analysis_path, encoding="utf-8") as file:
    plan = file.read()

# --------------------------------------------------
# 3. Verify dictionary variable coverage
# --------------------------------------------------

missing_variables = [
    name for name in headers
    if name not in dictionary
]

print("=" * 65)
print("PHASE 1 - TASK 6: DOCUMENTATION AUDIT")
print("=" * 65)

print(f"\nDataset records: {len(records)}")
print(f"Dataset variables: {len(headers)}")

print("\nDATA DICTIONARY CHECKS")

print(
    "All 24 variables documented:",
    "PASS" if not missing_variables else "FAIL"
)

if missing_variables:
    print("Missing variables:", missing_variables)

# --------------------------------------------------
# 4. Verify classifications and measurement scales
# --------------------------------------------------

classification_terms = [
    "Qualitative",
    "Quantitative"
]

scale_terms = [
    "Nominal",
    "Ordinal",
    "Interval",
    "Ratio"
]

classification_ok = all(
    term.lower() in dictionary.lower()
    for term in classification_terms
)

scale_ok = all(
    term.lower() in dictionary.lower()
    for term in scale_terms
)

primary_section_ok = (
    "Phase 1 – Primary Variable Selection" in dictionary
)

print(
    "Variable classifications documented:",
    "PASS" if classification_ok else "FAIL"
)

print(
    "Measurement scales documented:",
    "PASS" if scale_ok else "FAIL"
)

print(
    "Primary variable section present:",
    "PASS" if primary_section_ok else "FAIL"
)

# --------------------------------------------------
# 5. Verify analysis plan
# --------------------------------------------------

required_plan_terms = [
    "Research Question",
    "quantity",
    "revenue",
    "category",
    "Pearson",
    "scatterplot",
    "histogram",
    "bar chart",
    "Descriptive Statistical Analysis"
]

missing_plan_terms = [
    term for term in required_plan_terms
    if term.lower() not in plan.lower()
]

print("\nANALYSIS PLAN CHECKS")

print(
    "Research question documented:",
    "PASS" if "research question" in plan.lower() else "FAIL"
)

print(
    "Primary variables documented:",
    "PASS" if (
        "quantity" in plan.lower()
        and "revenue" in plan.lower()
    ) else "FAIL"
)

print(
    "Statistical methods documented:",
    "PASS" if "pearson" in plan.lower() else "FAIL"
)

print(
    "Planned visualisations documented:",
    "PASS" if (
        "scatterplot" in plan.lower()
        and "histogram" in plan.lower()
        and "bar chart" in plan.lower()
    ) else "FAIL"
)

if missing_plan_terms:
    print("Missing plan terms:", missing_plan_terms)

# --------------------------------------------------
# 6. Documentation file sizes
# --------------------------------------------------

print("\nDOCUMENTATION FILES")

for path in [dictionary_path, analysis_path]:
    size = os.path.getsize(path)

    print(f"{path}: {size:,} bytes")

    if size == 0:
        raise ValueError(f"Empty file: {path}")

# --------------------------------------------------
# 7. Final result
# --------------------------------------------------

checks = [
    not missing_variables,
    classification_ok,
    scale_ok,
    primary_section_ok,
    not missing_plan_terms
]

print("\n" + "=" * 65)

if all(checks):
    print("PHASE 1 DOCUMENTATION AUDIT: PASS")
    print("All documentation requirements verified.")
else:
    print("PHASE 1 DOCUMENTATION AUDIT: FAIL")
    print("Review the failed checks before proceeding.")
    sys.exit(1)

print("=" * 65)

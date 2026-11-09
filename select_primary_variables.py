import csv
import os
from collections import Counter

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

dataset_path = (
    "data/processed/"
    "chocolate_sales_analysis_dataset.csv"
)

dictionary_path = "docs/data_dictionary.md"
analysis_plan_path = "docs/analysis_plan.md"

# --------------------------------------------------
# 2. Define selected variables
# --------------------------------------------------

primary_variables = [
    "quantity",
    "revenue"
]

supporting_variables = [
    "category",
    "brand",
    "gender",
    "loyalty_member",
    "age",
    "unit_price",
    "discount",
    "profit",
    "order_date",
    "country"
]

selected_variables = (
    primary_variables + supporting_variables
)

# --------------------------------------------------
# 3. Read and verify dataset
# --------------------------------------------------

with open(
    dataset_path,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)
    headers = reader.fieldnames

    if headers is None:
        raise ValueError("Dataset has no header row.")

    records = list(reader)

row_count = len(records)
column_count = len(headers)

print("=" * 65)
print("PHASE 1 - TASK 5: PRIMARY VARIABLE SELECTION")
print("=" * 65)

print(f"\nDataset records: {row_count}")
print(f"Dataset variables: {column_count}")

if row_count != 1000:
    raise ValueError(
        f"Expected 1000 records, found {row_count}"
    )

if column_count != 24:
    raise ValueError(
        f"Expected 24 variables, found {column_count}"
    )

# --------------------------------------------------
# 4. Verify selected variables
# --------------------------------------------------

missing_columns = [
    variable
    for variable in selected_variables
    if variable not in headers
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("\nPRIMARY VARIABLES:")

for variable in primary_variables:
    print(f"  - {variable}")

print("\nSUPPORTING VARIABLES:")

for variable in supporting_variables:
    print(f"  - {variable}")

# --------------------------------------------------
# 5. Count missing values
# --------------------------------------------------

print("\nMISSING VALUE COUNTS:")

missing_counts = {}

for variable in selected_variables:

    count = sum(
        1 for record in records
        if record[variable] is None
        or record[variable].strip() == ""
    )

    missing_counts[variable] = count

    print(f"  {variable}: {count}")

# --------------------------------------------------
# 6. Update data dictionary
# --------------------------------------------------

dictionary_section = """
## Phase 1 – Primary Variable Selection

### Primary Correlation Variables

| Variable | Role | Measurement Scale | Statistical Type |
|---|---|---|---|
| quantity | Independent variable (X) | Ratio | Quantitative discrete |
| revenue | Dependent variable (Y) | Ratio | Quantitative continuous |

The primary statistical investigation examines whether
quantity sold is associated with total revenue.

The scatterplot will place quantity on the X-axis and
revenue on the Y-axis.

### Supporting Variables

| Variable | Purpose |
|---|---|
| category | Compare sales across product categories |
| brand | Examine brand distribution |
| gender | Examine customer distribution |
| loyalty_member | Examine loyalty membership groups |
| age | Describe customer age distribution |
| unit_price | Examine product pricing |
| discount | Examine transaction discounts |
| profit | Describe transaction profitability |
| order_date | Examine sales over time |
| country | Describe geographical distribution |

### Missing Value Summary

| Variable | Missing Values |
|---|---|
"""

for variable in selected_variables:
    dictionary_section += (
        f"| {variable} | {missing_counts[variable]} |\n"
    )

dictionary_section += """
All selected variables were verified against the
1,000-record analysis dataset.
"""

os.makedirs("docs", exist_ok=True)

if not os.path.exists(dictionary_path):
    raise FileNotFoundError(
        f"Existing data dictionary not found: {dictionary_path}"
    )

with open(
    dictionary_path,
    "r",
    encoding="utf-8"
) as file:
    dictionary_content = file.read()

marker = "## Phase 1 – Primary Variable Selection"

if marker in dictionary_content:
    dictionary_content = (
        dictionary_content.split(marker)[0].rstrip()
    )

dictionary_content += "\n\n" + dictionary_section.strip() + "\n"

with open(
    dictionary_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(dictionary_content)

# --------------------------------------------------
# 7. Create/update analysis plan
# --------------------------------------------------

analysis_plan = """
# Statistical Analysis Plan

## Project Title

Statistical Analysis of Chocolate Sales Data

## 1. Research Question

Is there an association between the quantity of
chocolate sold and total revenue?

## 2. Analysis Dataset

- Dataset: chocolate_sales_analysis_dataset.csv
- Sample size: 1,000 sales transactions
- Sampling method: Simple random sampling without replacement
- Random seed: 42

## 3. Primary Correlation Analysis

| Variable | Role | Measurement Scale | Type |
|---|---|---|---|
| quantity | Independent (X) | Ratio | Quantitative discrete |
| revenue | Dependent (Y) | Ratio | Quantitative continuous |

A scatterplot will be created with quantity on the
X-axis and revenue on the Y-axis.

Pearson's correlation coefficient will be calculated
to measure the strength and direction of the linear
association between these two quantitative variables.

## 4. Primary Qualitative Analysis

- Variable: category
- Purpose: Examine the distribution of transactions
  across chocolate product categories.
- Chart: Frequency table and bar chart.

## 5. Supporting Analyses

| Variable | Planned Analysis |
|---|---|
| brand | Frequency distribution |
| gender | Frequency distribution |
| loyalty_member | Group distribution |
| age | Descriptive statistics and histogram |
| unit_price | Descriptive statistics |
| discount | Descriptive statistics |
| profit | Descriptive statistics |
| order_date | Sales trends over time |
| country | Geographical frequency distribution |

## 6. Planned Statistical Visualisations

1. Product category bar chart.
2. Customer gender or segment pie chart.
3. Revenue histogram.
4. Revenue boxplot.
5. Quantity versus revenue scatterplot.

## 7. Descriptive Statistical Analysis

The analysis will include:

- Mean
- Median
- Mode
- Minimum
- Maximum
- Range
- Variance
- Standard deviation
- Quartiles

Appropriate statistics will be calculated for
quantitative variables.

## 8. Correlation Analysis

Pearson's correlation coefficient will be used to
investigate the linear association between quantity
and revenue.

The result will be interpreted in terms of direction
and strength. Statistical significance will also be
considered where appropriate.

## 9. Data Integrity Considerations

The analysis will retain the selected sample of
1,000 transactions.

Unmatched product records identified during dataset
inspection will not be automatically deleted.

Data cleaning decisions will be documented separately.

## 10. Expected Outcome

The analysis will establish whether quantity sold
and total revenue exhibit a positive, negative, or
negligible linear association.
"""

with open(
    analysis_plan_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(analysis_plan.strip() + "\n")

# --------------------------------------------------
# 8. Verify documentation files
# --------------------------------------------------

print("\nDOCUMENTATION FILES:")

for path in [dictionary_path, analysis_plan_path]:

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    size = os.path.getsize(path)

    print(f"  {path}: {size:,} bytes")

    if size == 0:
        raise ValueError(f"Empty documentation file: {path}")

# --------------------------------------------------
# 9. Final verification
# --------------------------------------------------

print("\n" + "=" * 65)
print("VERIFICATION RESULTS")
print("=" * 65)

print("Dataset records: PASS")
print("Dataset variables: PASS")
print("Primary variables: PASS")
print("Supporting variables: PASS")
print("Missing value counts: PASS")
print("Data dictionary updated: PASS")
print("Analysis plan created/updated: PASS")
print("Raw CSV files modified: NO")
print("Unmatched product records deleted: NO")

print("\nTASK 5 SCRIPT EXECUTION: SUCCESS")
print("=" * 65)

# Data Cleaning Decisions

## 1. Original Dataset

The original sampled analysis dataset was created during Phase 1 using simple random sampling without replacement.

- Original dataset: chocolate_sales_analysis_dataset.csv
- Original records: 1,000
- Original variables: 24
- Sampling method: Simple Random Sampling
- Random seed: 42

The original sampled dataset has been preserved.

## 2. Missing Qualitative Values

Investigation identified missing values in two qualitative variables.

| Variable | Missing values |
|---|---:|
| category | 8 |
| brand | 8 |

The eight affected transactions were associated with unmatched product IDs P0000 and P0201.

### Cleaning Decision

Option A was selected: exclude the eight affected transactions when creating the cleaned dataset.

### Justification

1. Product descriptions could not be reliably recovered.
2. Both category and brand were missing for the affected transactions.
3. Inventing product labels could distort category and brand frequency tables.
4. Excluding these records ensures valid product descriptions in the final analysis dataset.

The original sampled dataset was not modified.

## 3. Quantitative Variable Validation

Nine quantitative variables were examined for missing values and logically valid numerical ranges.

| Variable | Minimum | Maximum | Missing values |
|---|---:|---:|---:|
| quantity | 1 | 5 | 0 |
| unit_price | 3.04 | 14.98 | 0 |
| discount | 0.00 | 0.20 | 0 |
| revenue | 2.44 | 73.25 | 0 |
| cost | 1.29 | 49.52 | 0 |
| profit | 1.09 | 36.37 | 0 |
| cocoa_percent | 50 | 90 | 8 |
| weight_g | 50 | 200 | 8 |
| age | 18 | 70 | 0 |

The eight missing cocoa_percent and weight_g values occurred in the same transactions associated with unmatched product IDs P0000 and P0201.

No numerical values were imputed or changed.

The eight affected transactions were excluded during cleaned dataset creation.

## 4. Categorical Label Standardisation

Nine categorical variables were inspected:

- product_name
- brand
- category
- gender
- loyalty_member
- store_name
- city
- country
- store_type

The inspection found no capitalisation inconsistencies, leading or trailing whitespace, or duplicate labels caused by inconsistent capitalisation.

No categorical labels were changed.

## 5. Creation of the Cleaned Dataset

The cleaned dataset was created using the original sampled analysis dataset.

| Description | Records |
|---|---:|
| Original sampled records | 1,000 |
| Excluded records | 8 |
| Final cleaned records | 992 |

Output file:

`data/processed/chocolate_sales_clean.csv`

The cleaned dataset retains all 24 variables.

The original sampled dataset remains unchanged.

## 6. Summary of Cleaning Actions

| Cleaning activity | Action taken |
|---|---|
| Missing category values | Excluded 8 affected transactions |
| Missing brand values | Excluded 8 affected transactions |
| Quantitative validation | Inspected 9 variables |
| Numerical imputation | None |
| Numerical value modification | None |
| Categorical label standardisation | No changes required |
| Original sampled dataset | Preserved |
| Cleaned dataset | Created with 992 records |

The eight excluded transactions were associated with unmatched product IDs P0000 and P0201.

## 7. Final Dataset

The final cleaned dataset was independently verified.

| Property | Verified result |
|---|---:|
| File | chocolate_sales_clean.csv |
| Records | 992 |
| Variables | 24 |
| Missing or empty cells | 0 |
| Excluded transactions | 8 |
| Numerical values imputed | 0 |
| Categorical labels changed | 0 |
| Original sampled dataset preserved | Yes |

The cleaned dataset is ready for import into the Excel statistical analysis workbook.

All cleaning decisions were documented to maintain transparency, reproducibility, and data integrity.
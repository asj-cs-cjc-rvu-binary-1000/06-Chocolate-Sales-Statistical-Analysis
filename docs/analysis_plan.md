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

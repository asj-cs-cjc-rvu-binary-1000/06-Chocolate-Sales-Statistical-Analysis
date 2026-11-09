# Chocolate Sales Data Dictionary

## Overview

This document describes the variables contained in the
original chocolate sales datasets.

The variable definitions, data types, descriptions, and
measurement scales will be completed after inspecting
the actual CSV files.

## Data Dictionary

| File Name | Column Name | Data Type | Description |
|-----------|-------------|-----------|-------------|
|           |             |            |             |

## Phase 1 – Variable Identification

### Dataset Overview

| Attribute | Details |
|---|---|
| Dataset name | chocolate_sales_analysis_dataset.csv |
| Sample size | 1,000 sales transactions |
| Number of variables | 24 |
| Sampling method | Simple random sampling without replacement |
| Random seed | 42 |
| Data sources | Sales, Products, Customers and Stores |

### Complete Variable Inventory

| No. | Variable Name | Source Dataset | Description |
|---:|---|---|---|
| 1 | `order_id` | Sales | Unique identifier for each sales transaction. |
| 2 | `order_date` | Sales | Date on which the transaction occurred. |
| 3 | `product_id` | Sales / Products | Identifier of the product sold. |
| 4 | `store_id` | Sales / Stores | Identifier of the store where the sale occurred. |
| 5 | `customer_id` | Sales / Customers | Identifier of the customer associated with the transaction. |
| 6 | `quantity` | Sales | Number of chocolate units sold in the transaction. |
| 7 | `unit_price` | Sales | Price per unit of the product. |
| 8 | `discount` | Sales | Discount recorded for the transaction. |
| 9 | `revenue` | Sales | Total revenue recorded for the transaction. |
| 10 | `cost` | Sales | Total cost recorded for the transaction. |
| 11 | `profit` | Sales | Profit recorded for the transaction. |
| 12 | `product_name` | Products | Name of the chocolate product. |
| 13 | `brand` | Products | Brand associated with the product. |
| 14 | `category` | Products | Product category or classification. |
| 15 | `cocoa_percent` | Products | Cocoa percentage of the chocolate product. |
| 16 | `weight_g` | Products | Product weight measured in grams. |
| 17 | `age` | Customers | Age of the customer. |
| 18 | `gender` | Customers | Recorded gender category of the customer. |
| 19 | `loyalty_member` | Customers | Indicator of the customer's loyalty membership status. |
| 20 | `join_date` | Customers | Date on which the customer joined the programme or customer database. |
| 21 | `store_name` | Stores | Name of the store. |
| 22 | `city` | Stores | City in which the store is located. |
| 23 | `country` | Stores | Country in which the store is located. |
| 24 | `store_type` | Stores | Classification or type of store. |

### Notes

- The variable names above match the actual headers in the joined CSV dataset.
- The `product_id`, `customer_id` and `store_id` variables are shared join keys between sales and their respective dimension datasets.
- Some product details may be blank because eight sampled transactions have unmatched product IDs.
- Unmatched product records have been retained in the dataset.
- This inventory identifies variables only. Statistical classifications and measurement scales will be documented separately in the subsequent tasks.

## Phase 1 – Variable Classification

### Classification of Variables

Variables are classified as qualitative or quantitative based on their statistical meaning.

| No. | Variable Name | Classification | Subcategory | Reason |
|---:|---|---|---|---|
| 1 | `order_id` | Qualitative | Nominal | Transaction identifier used for identification. |
| 2 | `order_date` | Quantitative | Discrete (Temporal) | Calendar date used to identify when a transaction occurred. |
| 3 | `product_id` | Qualitative | Nominal | Product identifier used as a category or label. |
| 4 | `store_id` | Qualitative | Nominal | Store identifier used as a category or label. |
| 5 | `customer_id` | Qualitative | Nominal | Customer identifier used as a category or label. |
| 6 | `quantity` | Quantitative | Discrete | Count of chocolate units sold. |
| 7 | `unit_price` | Quantitative | Continuous | Numerical measurement of the price per unit. |
| 8 | `discount` | Quantitative | Continuous | Numerical measurement of the discount. |
| 9 | `revenue` | Quantitative | Continuous | Numerical measurement of total sales revenue. |
| 10 | `cost` | Quantitative | Continuous | Numerical measurement of transaction cost. |
| 11 | `profit` | Quantitative | Continuous | Numerical measurement of transaction profit. |
| 12 | `product_name` | Qualitative | Nominal | Name identifying the chocolate product. |
| 13 | `brand` | Qualitative | Nominal | Brand category associated with the product. |
| 14 | `category` | Qualitative | Nominal | Product category without an inherent ranking. |
| 15 | `cocoa_percent` | Quantitative | Continuous | Measured percentage of cocoa in the product. |
| 16 | `weight_g` | Quantitative | Continuous | Product weight measured in grams. |
| 17 | `age` | Quantitative | Discrete | Customer age recorded as a numerical count of years. |
| 18 | `gender` | Qualitative | Nominal | Categorical gender information. |
| 19 | `loyalty_member` | Qualitative | Nominal | Membership status representing Yes or No. |
| 20 | `join_date` | Quantitative | Discrete (Temporal) | Calendar date indicating when the customer joined. |
| 21 | `store_name` | Qualitative | Nominal | Name identifying the store. |
| 22 | `city` | Qualitative | Nominal | City location of the store. |
| 23 | `country` | Qualitative | Nominal | Country location of the store. |
| 24 | `store_type` | Qualitative | Nominal | Category identifying the type of store. |

### Classification Summary

- Total variables: 24
- Qualitative variables: 13
- Quantitative variables: 11

### Statistical Notes

- Identifier variables such as order_id, product_id, customer_id and store_id are qualitative nominal variables, even though they may contain numbers or letters.
- loyalty_member is qualitative nominal because it represents membership categories rather than a measurable quantity.
- quantity is quantitative discrete because it represents a count of units sold.
- Financial measurements, percentages and weight are classified as quantitative continuous variables.
- order_date and join_date are treated as quantitative temporal variables at calendar-day resolution.
- No ordinal variables are identified in this dataset.

## Phase 1 – Scales of Measurement

### Classification of Variables by Measurement Scale

Variables are assigned one of the four standard statistical measurement scales: nominal, ordinal, interval or ratio.

| No. | Variable Name | Measurement Scale | Reason |
|---:|---|---|---|
| 1 | `order_id` | Nominal | Transaction identifier. |
| 2 | `order_date` | Interval | Calendar dates have meaningful differences but no absolute zero. |
| 3 | `product_id` | Nominal | Product identifier. |
| 4 | `store_id` | Nominal | Store identifier. |
| 5 | `customer_id` | Nominal | Customer identifier. |
| 6 | `quantity` | Ratio | Zero means no units were sold. |
| 7 | `unit_price` | Ratio | Zero represents no monetary price. |
| 8 | `discount` | Ratio | Zero represents no discount. |
| 9 | `revenue` | Ratio | Zero represents no revenue. |
| 10 | `cost` | Ratio | Zero represents no cost. |
| 11 | `profit` | Ratio | Zero represents no profit; negative values can represent losses. |
| 12 | `product_name` | Nominal | Product name used for identification. |
| 13 | `brand` | Nominal | Brand category. |
| 14 | `category` | Nominal | Product category without inherent ranking. |
| 15 | `cocoa_percent` | Ratio | Zero represents no cocoa content. |
| 16 | `weight_g` | Ratio | Zero represents no weight. |
| 17 | `age` | Ratio | Age has a meaningful zero point. |
| 18 | `gender` | Nominal | Categorical gender information. |
| 19 | `loyalty_member` | Nominal | Membership category such as Yes or No. |
| 20 | `join_date` | Interval | Calendar dates have meaningful differences but no absolute zero. |
| 21 | `store_name` | Nominal | Store name. |
| 22 | `city` | Nominal | City location. |
| 23 | `country` | Nominal | Country location. |
| 24 | `store_type` | Nominal | Store category without inherent ranking. |

### Measurement Scale Summary

- Total variables: 24
- Nominal variables: 13
- Ordinal variables: 0
- Interval variables: 2
- Ratio variables: 9

### Statistical Notes

- Identifier variables are nominal, even when they contain numeric characters.
- Calendar dates are treated as interval variables.
- Quantity, financial measurements, age, cocoa percentage and weight are treated as ratio variables.
- No ordinal variables were identified.
- Profit can be negative while retaining its ratio measurement scale.

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
| quantity | 0 |
| revenue | 0 |
| category | 8 |
| brand | 8 |
| gender | 0 |
| loyalty_member | 0 |
| age | 0 |
| unit_price | 0 |
| discount | 0 |
| profit | 0 |
| order_date | 0 |
| country | 0 |

All selected variables were verified against the
1,000-record analysis dataset.

# Data Overview

## Dataset Shape

- Rows: 3,729
- Columns: 17

## Data Types

| column | data_type |
| --- | --- |
| product_name | object |
| category | object |
| sub_category | object |
| brand | object |
| quantity | object |
| price | float64 |
| mrp | float64 |
| discount_percent | int64 |
| savings_amount | float64 |
| rating | float64 |
| reviews | int64 |
| available_quantity | int64 |
| availability | object |
| value_score | float64 |
| rating_was_missing | bool |
| out_of_stock | bool |
| quantity_raw | int64 |

## Missing Values

| column | missing_values | missing_percent |
| --- | --- | --- |
| product_name | 0 | 0.0 |
| category | 0 | 0.0 |
| sub_category | 0 | 0.0 |
| brand | 0 | 0.0 |
| quantity | 0 | 0.0 |
| price | 0 | 0.0 |
| mrp | 0 | 0.0 |
| discount_percent | 0 | 0.0 |
| savings_amount | 0 | 0.0 |
| rating | 0 | 0.0 |
| reviews | 0 | 0.0 |
| available_quantity | 0 | 0.0 |
| availability | 0 | 0.0 |
| value_score | 0 | 0.0 |
| rating_was_missing | 0 | 0.0 |
| out_of_stock | 0 | 0.0 |
| quantity_raw | 0 | 0.0 |

## Unique Values

| column | unique_values |
| --- | --- |
| product_name | 1673 |
| category | 14 |
| sub_category | 1 |
| brand | 1 |
| quantity | 158 |
| price | 331 |
| mrp | 251 |
| discount_percent | 42 |
| savings_amount | 98 |
| rating | 1 |
| reviews | 1 |
| available_quantity | 7 |
| availability | 2 |
| value_score | 818 |
| rating_was_missing | 1 |
| out_of_stock | 2 |
| quantity_raw | 143 |

## Statistical Summary

| metric | count | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| price | 3729.0 | 138.78 | 120.72 | 10.0 | 55.0 | 104.0 | 184.0 | 630.0 |
| mrp | 3729.0 | 152.55 | 132.63 | 10.28 | 60.0 | 110.0 | 200.0 | 697.88 |
| discount_percent | 3729.0 | 7.62 | 9.21 | 0.0 | 0.0 | 6.0 | 10.0 | 51.0 |
| savings_amount | 3729.0 | 13.77 | 23.75 | 0.0 | 0.0 | 5.0 | 16.0 | 264.0 |
| rating | 3729.0 | 3.0 | 0.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 |
| reviews | 3729.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| available_quantity | 3729.0 | 4.01 | 2.2 | 0.0 | 2.0 | 5.0 | 6.0 | 6.0 |
| value_score | 3729.0 | 0.15 | 0.03 | 0.09 | 0.12 | 0.14 | 0.16 | 0.3 |
| quantity_raw | 3729.0 | 213.29 | 194.79 | 0.0 | 50.0 | 182.0 | 340.0 | 1500.0 |

## Categorical Summary

| column | count | unique | top | freq |
| --- | --- | --- | --- | --- |
| product_name | 3729 | 1673 | Amul Delicious Fat Spread - Cholesterol Free | 10 |
| category | 3729 | 14 | Cooking Essentials | 514 |
| sub_category | 3729 | 1 | Unknown | 3729 |
| brand | 3729 | 1 | Unbranded | 3729 |
| quantity | 3729 | 158 | 200 | 410 |
| availability | 3729 | 2 | In Stock | 3276 |

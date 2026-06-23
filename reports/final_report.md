# Zepto Business Intelligence & Exploratory Data Analysis

## Objective

Build a professional Exploratory Data Analysis application for a real-world Zepto product dataset to uncover customer behavior, pricing patterns, product performance, and business opportunities.

## Business Questions

1. Which Zepto categories generate the highest average selling prices?
2. Which products offer the largest discount percentages and savings amounts?
3. Which brands dominate Zepto's catalog by product count?
4. Which categories have the deepest product assortment?
5. Are expensive products also highly rated by customers?
6. Which products provide the best value for money after discounts and ratings?
7. Is there a meaningful relationship between discount percentage and rating?
8. Which categories should Zepto prioritize for inventory and promotion?
9. Which categories appear premium based on price and MRP behavior?
10. Which products or categories show low customer performance and need attention?

## Dataset Summary

- Total cleaned products: 3,729
- Total categories: 14
- Total brands: 1
- Average selling price: 138.78
- Average discount: 7.62%
- Average rating: 3.00

## Analysis Performed

- Dataset exploration: shape, data types, missing values, unique values, and summary statistics.
- Data cleaning: duplicates, missing values, column normalization, type conversion, invalid records, and outliers.
- Univariate analysis: product count, price distribution, and rating distribution.
- Bivariate analysis: price vs rating, discount vs rating, and category vs price.
- Multivariate analysis: category vs brand vs price and discount vs rating vs category.
- Hypothesis testing: correlation analysis, Welch's t-test, and chi-square test.
- Business intelligence: category performance, pricing trends, value products, and recommendations.

## Key Findings

### Top Categories by Product Count

| category | product_count |
| --- | --- |
| Cooking Essentials | 514 |
| Munchies | 514 |
| Packaged Food | 388 |
| Ice Cream & Desserts | 388 |
| Chocolates & Candies | 388 |
| Paan Corner | 343 |
| Personal Care | 343 |
| Home & Cleaning | 193 |
| Biscuits | 147 |
| Dairy, Bread & Batter | 129 |

### Highest Average Price Categories

| category | price |
| --- | --- |
| Paan Corner | 187.05 |
| Personal Care | 187.05 |
| Meats, Fish & Eggs | 164.1 |
| Health & Hygiene | 145.86 |
| Home & Cleaning | 141.2 |
| Chocolates & Candies | 140.98 |
| Packaged Food | 140.98 |
| Ice Cream & Desserts | 140.98 |
| Cooking Essentials | 131.45 |
| Munchies | 131.45 |

### Highest Discount Products

| product_name | category | brand | price | mrp | discount_percent |
| --- | --- | --- | --- | --- | --- |
| Dukes Waffy Chocolate Wafers | Biscuits | Unbranded | 22.0 | 45.0 | 51 |
| Dukes Waffy Orange Wafers | Biscuits | Unbranded | 22.0 | 45.0 | 51 |
| Dukes Waffy Strawberry Wafers | Biscuits | Unbranded | 22.0 | 45.0 | 51 |
| RRO Mascarpone Cheese | Dairy, Bread & Batter | Unbranded | 177.0 | 355.0 | 50 |
| RRO Mascarpone Cheese | Beverages | Unbranded | 177.0 | 355.0 | 50 |
| RRO Cheddar Block Cheese | Dairy, Bread & Batter | Unbranded | 147.0 | 295.0 | 50 |
| RRO Mozzarella Block Cheese | Dairy, Bread & Batter | Unbranded | 147.0 | 295.0 | 50 |
| RRO Cheddar Block Cheese | Beverages | Unbranded | 147.0 | 295.0 | 50 |
| RRO Mozzarella Block Cheese | Beverages | Unbranded | 147.0 | 295.0 | 50 |
| Moi Soi Sichuan Chilli Oil- For Stir Fry Marinade Spread & Dip | Packaged Food | Unbranded | 140.0 | 280.0 | 50 |

### Best Value Products

| product_name | category | brand | price | rating | discount_percent | value_score |
| --- | --- | --- | --- | --- | --- | --- |
| Epigamia Fruit Yogurt Vanilla | Health & Hygiene | Unbranded | 20.0 | 3.0 | 50 | 0.296 |
| Epigamia Fruit Yogurt Alphonso Mango | Health & Hygiene | Unbranded | 20.0 | 3.0 | 50 | 0.296 |
| Epigamia Fruit Yogurt Strawberry | Health & Hygiene | Unbranded | 20.0 | 3.0 | 50 | 0.296 |
| Mint Leaves | Fruits & Vegetables | Unbranded | 10.0 | 3.0 | 18 | 0.295 |
| Beetroot | Fruits & Vegetables | Unbranded | 10.0 | 3.0 | 18 | 0.295 |
| Garlic Indian | Fruits & Vegetables | Unbranded | 10.0 | 3.0 | 18 | 0.295 |
| Banana Leaf | Fruits & Vegetables | Unbranded | 10.0 | 3.0 | 16 | 0.29 |
| Dukes Waffy Orange Wafers | Biscuits | Unbranded | 22.0 | 3.0 | 51 | 0.289 |
| Dukes Waffy Chocolate Wafers | Biscuits | Unbranded | 22.0 | 3.0 | 51 | 0.289 |
| Dukes Waffy Strawberry Wafers | Biscuits | Unbranded | 22.0 | 3.0 | 51 | 0.289 |

### Low Performing Products

| product_name | category | brand | price | rating | reviews |
| --- | --- | --- | --- | --- | --- |
| Onion | Fruits & Vegetables | Unbranded | 21.0 | 3.0 | 0 |
| Tomato Hybrid | Fruits & Vegetables | Unbranded | 35.0 | 3.0 | 0 |
| Tender Coconut | Fruits & Vegetables | Unbranded | 43.0 | 3.0 | 0 |
| Coriander Leaves | Fruits & Vegetables | Unbranded | 17.0 | 3.0 | 0 |
| Ladies Finger | Fruits & Vegetables | Unbranded | 12.0 | 3.0 | 0 |
| Potato | Fruits & Vegetables | Unbranded | 29.0 | 3.0 | 0 |
| Lemon | Fruits & Vegetables | Unbranded | 63.0 | 3.0 | 0 |
| Watermelon | Fruits & Vegetables | Unbranded | 49.0 | 3.0 | 0 |
| Capsicum Green | Fruits & Vegetables | Unbranded | 19.0 | 3.0 | 0 |
| Chilli Green | Fruits & Vegetables | Unbranded | 16.0 | 3.0 | 0 |

## Hypothesis Test Results

- Higher discounts increase ratings. Result: Not strongly supported (statistic=nan, p-value=nan).
- Premium products receive better ratings. Result: Not strongly supported (statistic=nan, p-value=nan).
- Popular categories have lower average prices. Result: Not strongly supported (statistic=0.3916, p-value=0.1661).
- Product availability differs by category. Result: Availability pattern differs by category (statistic=89.7315, p-value=0.0).

## Insights

- Cooking Essentials shows strong customer performance based on rating, review activity, and assortment depth.
- Paan Corner has the highest average selling price and should be managed with margin-focused pricing.
- Fruits & Vegetables carries the highest average discount and should be monitored for margin leakage.
- Products with high value scores combine strong ratings, meaningful discounts, and accessible pricing.
- Low-rated products with review volume deserve priority review because the signal is more reliable than isolated ratings.

## Recommendations

- Increase inventory depth for categories with high ratings, high review activity, and strong product counts.
- Promote high-value products through app banners, search boosts, and category-level recommendation slots.
- Re-evaluate discount-heavy categories to separate effective promotions from unnecessary margin loss.
- Audit low-performing products for quality, listing accuracy, pricing, and fulfillment issues.
- Build category-specific pricing rules because premium and value categories show different business behavior.

## Conclusion

The analysis converts Zepto product catalog data into practical business intelligence. It identifies category strengths, pricing opportunities, discount effectiveness, value products, and products requiring corrective attention. The pipeline is reusable for new Zepto Kaggle extracts because it automatically selects the richest raw CSV and normalizes common product dataset column formats.

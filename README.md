# Zepto Business Intelligence & Exploratory Data Analysis

## Project Overview

This project is a complete internship-level Exploratory Data Analysis application for a real-world Zepto product dataset from Kaggle. It automatically selects the richest CSV file from `data/raw/`, cleans product catalog data, analyzes pricing and customer behavior, generates statistical tests, creates visualizations, and writes recruiter-friendly business reports.

## Business Problem

Quick-commerce platforms such as Zepto operate with large product catalogs, fast-changing discounts, and category-level inventory pressure. The goal of this project is to convert raw product data into business intelligence that helps identify high-performing categories, discount opportunities, pricing trends, low-performing products, and inventory priorities.

## Dataset Information

This project uses the Kaggle dataset:

- [Zepto Inventory Dataset by palvinder2006](https://www.kaggle.com/datasets/palvinder2006/zepto-inventory-dataset)

The downloaded source file is available in `data/raw/zepto_v1.xlsx`, and a CSV copy is available in `data/raw/zepto_v1.csv` for the Python pipeline.

Other compatible Kaggle Zepto datasets include:

- Zepto Product Dataset
- Zepto Grocery Product Dataset
- Zepto Inventory Dataset

Place one or more CSV files in `data/raw/`. If multiple CSV files exist, the application scores them by product-information richness and automatically chooses the best dataset. The pipeline supports common columns such as product name, category, sub category, brand, price, MRP, discount, quantity, rating, reviews, availability, `discountPercent`, `discountedSellingPrice`, and `availableQuantity`.

## Key Questions

1. Which categories generate the highest average prices?
2. Which products have the highest discounts?
3. Which brands dominate Zepto?
4. Which categories have the most products?
5. Are expensive products highly rated?
6. Which products offer the best value for money?
7. Is there a relationship between discounts and ratings?
8. Which categories should Zepto prioritize?

## Technologies Used

- Python
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- pathlib
- logging

## Folder Structure

```text
CodeAlpha_EDA_Zepto_Project/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── config/
│   └── settings.py
├── data/
│   ├── raw/
│   └── processed/
├── preprocessing/
│   └── clean_data.py
├── analysis/
│   ├── explore_data.py
│   ├── hypothesis_testing.py
│   └── insight_generator.py
├── visualization/
│   └── create_visualizations.py
├── visualizations/
├── reports/
└── logs/
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Add a Zepto Kaggle CSV file to `data/raw/`, then run:

```bash
python main.py
```

## Generated Outputs

- `data/processed/cleaned_data.csv`
- `reports/business_questions.md`
- `reports/data_overview.md`
- `reports/hypothesis_tests.md`
- `reports/final_report.md`
- `logs/project.log`
- Professional charts in `visualizations/`

## Visualizations

The project generates:

- Product count bar charts
- Price distribution histograms
- Rating distribution histograms
- Availability pie chart
- Price vs rating scatter plot
- Discount vs rating scatter plot
- Category price box plot
- Category average price bar chart
- Category vs brand price heatmap
- Discount vs rating vs category bubble chart
- Correlation matrix heatmap

## Insights

The analysis identifies:

- Top-performing categories
- Premium product categories
- High-discount categories
- Low-performing products
- Best value-for-money products
- Relationships among price, discount, rating, reviews, and availability

## Recommendations

- Increase inventory for categories with strong ratings, review activity, and product depth.
- Promote products with high value scores and customer-friendly pricing.
- Re-evaluate excessive discounts that do not improve ratings or demand signals.
- Audit low-rated products for quality, listing accuracy, fulfillment issues, and pricing mismatch.
- Use category-specific pricing strategies for premium and value-driven segments.

## Future Improvements

- Add time-series analysis if date or order-level data becomes available.
- Build an interactive dashboard with Streamlit or Power BI.
- Add automated Kaggle API ingestion when credentials are available.
- Compare Zepto pricing with Blinkit, Instamart, or BigBasket datasets.
- Add SKU-level demand forecasting and inventory optimization.

"""Project-wide constants for the Zepto EDA pipeline."""

from pathlib import Path


PROJECT_NAME = "Zepto Business Intelligence & Exploratory Data Analysis"

BASE_DIR = Path(".")
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"
VISUALIZATIONS_DIR = BASE_DIR / "visualizations"
LOGS_DIR = BASE_DIR / "logs"

CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "cleaned_data.csv"
PROJECT_LOG_PATH = LOGS_DIR / "project.log"

BUSINESS_QUESTIONS_REPORT = REPORTS_DIR / "business_questions.md"
DATA_OVERVIEW_REPORT = REPORTS_DIR / "data_overview.md"
HYPOTHESIS_REPORT = REPORTS_DIR / "hypothesis_tests.md"
FINAL_REPORT = REPORTS_DIR / "final_report.md"

RANDOM_STATE = 42
TOP_N = 10
OUTLIER_LOWER_QUANTILE = 0.01
OUTLIER_UPPER_QUANTILE = 0.99

PREFERRED_FIELDS = {
    "product_name",
    "category",
    "sub_category",
    "brand",
    "price",
    "mrp",
    "discount_percent",
    "quantity",
    "available_quantity",
    "rating",
    "reviews",
    "availability",
    "out_of_stock",
}

COLUMN_ALIASES = {
    "product_name": {
        "product_name",
        "product",
        "products",
        "name",
        "sku_name",
        "item_name",
        "title",
    },
    "category": {"category", "category_name", "cat"},
    "sub_category": {
        "sub_category",
        "subcategory",
        "subcat",
        "sub_category_name",
        "l2_category",
    },
    "brand": {"brand", "brand_name", "manufacturer"},
    "price": {
        "price",
        "selling_price",
        "discounted_price",
        "discountedsellingprice",
        "discounted_selling_price",
        "sale_price",
        "current_price",
    },
    "mrp": {"mrp", "maximum_retail_price", "original_price", "list_price"},
    "discount_percent": {
        "discount",
        "discount_percent",
        "discount_percentage",
        "discountpercent",
        "off",
        "offer_percent",
    },
    "quantity": {
        "quantity",
        "pack_size",
        "pack",
        "weight",
        "weightingms",
        "weight_in_gms",
        "weightingm",
        "net_weight",
    },
    "available_quantity": {
        "available_quantity",
        "availablequantity",
        "stock",
        "inventory",
        "stock_quantity",
    },
    "rating": {"rating", "ratings", "avg_rating", "average_rating", "stars"},
    "reviews": {
        "reviews",
        "review_count",
        "num_reviews",
        "number_of_reviews",
        "rating_count",
    },
    "availability": {
        "availability",
        "available",
        "in_stock",
        "stock_status",
    },
    "out_of_stock": {"out_of_stock", "outofstock"},
}

VISUALIZATION_STYLE = {
    "figure.figsize": (11, 7),
    "axes.titlesize": 16,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
}

"""Business insight and final report generation."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from analysis.explore_data import BUSINESS_QUESTIONS, _markdown_table
from config.settings import FINAL_REPORT, PROJECT_NAME, TOP_N


LOGGER = logging.getLogger(__name__)


def generate_insights(df: pd.DataFrame) -> dict[str, pd.DataFrame | list[str]]:
    """Generate actionable product, pricing, and category insights."""
    category_summary = (
        df.groupby("category", as_index=False)
        .agg(
            product_count=("product_name", "count"),
            average_price=("price", "mean"),
            average_mrp=("mrp", "mean"),
            average_discount=("discount_percent", "mean"),
            average_rating=("rating", "mean"),
            total_reviews=("reviews", "sum"),
            average_value_score=("value_score", "mean"),
        )
        .round(2)
    )

    best_categories = category_summary.sort_values(
        ["average_rating", "total_reviews", "product_count"],
        ascending=False,
    ).head(TOP_N)
    premium_categories = category_summary.sort_values("average_price", ascending=False).head(TOP_N)
    high_discount_categories = category_summary.sort_values("average_discount", ascending=False).head(TOP_N)
    high_value_products = (
        df.sort_values("value_score", ascending=False)
        .loc[:, ["product_name", "category", "brand", "price", "rating", "discount_percent", "value_score"]]
        .head(TOP_N)
        .round(3)
    )

    low_performing_products = (
        df.sort_values(["rating", "reviews"], ascending=[True, False])
        .loc[:, ["product_name", "category", "brand", "price", "rating", "reviews"]]
        .head(TOP_N)
        .round(2)
    )

    top_category = best_categories.iloc[0]["category"] if not best_categories.empty else "leading categories"
    premium_category = premium_categories.iloc[0]["category"] if not premium_categories.empty else "premium categories"
    discount_category = (
        high_discount_categories.iloc[0]["category"]
        if not high_discount_categories.empty
        else "discount-heavy categories"
    )

    narrative_insights = [
        f"{top_category} shows strong customer performance based on rating, review activity, and assortment depth.",
        f"{premium_category} has the highest average selling price and should be managed with margin-focused pricing.",
        f"{discount_category} carries the highest average discount and should be monitored for margin leakage.",
        "Products with high value scores combine strong ratings, meaningful discounts, and accessible pricing.",
        "Low-rated products with review volume deserve priority review because the signal is more reliable than isolated ratings.",
    ]

    recommendations = [
        "Increase inventory depth for categories with high ratings, high review activity, and strong product counts.",
        "Promote high-value products through app banners, search boosts, and category-level recommendation slots.",
        "Re-evaluate discount-heavy categories to separate effective promotions from unnecessary margin loss.",
        "Audit low-performing products for quality, listing accuracy, pricing, and fulfillment issues.",
        "Build category-specific pricing rules because premium and value categories show different business behavior.",
    ]

    LOGGER.info("Insights generated")
    return {
        "category_summary": category_summary,
        "best_categories": best_categories,
        "premium_categories": premium_categories,
        "high_discount_categories": high_discount_categories,
        "high_value_products": high_value_products,
        "low_performing_products": low_performing_products,
        "narrative_insights": narrative_insights,
        "recommendations": recommendations,
    }


def generate_final_report(
    df: pd.DataFrame,
    eda_results: dict[str, pd.DataFrame],
    hypothesis_results: dict[str, object],
    insight_results: dict[str, pd.DataFrame | list[str]],
    output_path: Path = FINAL_REPORT,
) -> None:
    """Create the final portfolio-ready EDA report."""
    sections = [
        f"# {PROJECT_NAME}",
        "",
        "## Objective",
        "",
        (
            "Build a professional Exploratory Data Analysis application for a real-world "
            "Zepto product dataset to uncover customer behavior, pricing patterns, product "
            "performance, and business opportunities."
        ),
        "",
        "## Business Questions",
        "",
    ]

    for index, question in enumerate(BUSINESS_QUESTIONS, start=1):
        sections.append(f"{index}. {question}")

    sections.extend(
        [
            "",
            "## Dataset Summary",
            "",
            f"- Total cleaned products: {len(df):,}",
            f"- Total categories: {df['category'].nunique():,}",
            f"- Total brands: {df['brand'].nunique():,}",
            f"- Average selling price: {df['price'].mean():.2f}",
            f"- Average discount: {df['discount_percent'].mean():.2f}%",
            f"- Average rating: {df['rating'].mean():.2f}",
            "",
            "## Analysis Performed",
            "",
            "- Dataset exploration: shape, data types, missing values, unique values, and summary statistics.",
            "- Data cleaning: duplicates, missing values, column normalization, type conversion, invalid records, and outliers.",
            "- Univariate analysis: product count, price distribution, and rating distribution.",
            "- Bivariate analysis: price vs rating, discount vs rating, and category vs price.",
            "- Multivariate analysis: category vs brand vs price and discount vs rating vs category.",
            "- Hypothesis testing: correlation analysis, Welch's t-test, and chi-square test.",
            "- Business intelligence: category performance, pricing trends, value products, and recommendations.",
            "",
            "## Key Findings",
            "",
            "### Top Categories by Product Count",
            "",
            _markdown_table(eda_results["category_product_count"]),
            "",
            "### Highest Average Price Categories",
            "",
            _markdown_table(eda_results["average_price_by_category"]),
            "",
            "### Highest Discount Products",
            "",
            _markdown_table(eda_results["highest_discount_products"]),
            "",
            "### Best Value Products",
            "",
            _markdown_table(insight_results["high_value_products"]),
            "",
            "### Low Performing Products",
            "",
            _markdown_table(insight_results["low_performing_products"]),
            "",
            "## Hypothesis Test Results",
            "",
        ]
    )

    for result in hypothesis_results.values():
        sections.extend(
            [
                f"- {result['hypothesis']} Result: {result['interpretation']} "
                f"(statistic={result['statistic']}, p-value={result['p_value']})."
            ]
        )

    sections.extend(["", "## Insights", ""])
    for insight in insight_results["narrative_insights"]:
        sections.append(f"- {insight}")

    sections.extend(["", "## Recommendations", ""])
    for recommendation in insight_results["recommendations"]:
        sections.append(f"- {recommendation}")

    sections.extend(
        [
            "",
            "## Conclusion",
            "",
            (
                "The analysis converts Zepto product catalog data into practical business intelligence. "
                "It identifies category strengths, pricing opportunities, discount effectiveness, value "
                "products, and products requiring corrective attention. The pipeline is reusable for new "
                "Zepto Kaggle extracts because it automatically selects the richest raw CSV and normalizes "
                "common product dataset column formats."
            ),
        ]
    )

    output_path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    LOGGER.info("Final report saved to %s", output_path)

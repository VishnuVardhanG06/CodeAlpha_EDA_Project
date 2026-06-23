"""Exploratory data analysis and report generation."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from config.settings import (
    BUSINESS_QUESTIONS_REPORT,
    DATA_OVERVIEW_REPORT,
    TOP_N,
)


LOGGER = logging.getLogger(__name__)


BUSINESS_QUESTIONS = [
    "Which Zepto categories generate the highest average selling prices?",
    "Which products offer the largest discount percentages and savings amounts?",
    "Which brands dominate Zepto's catalog by product count?",
    "Which categories have the deepest product assortment?",
    "Are expensive products also highly rated by customers?",
    "Which products provide the best value for money after discounts and ratings?",
    "Is there a meaningful relationship between discount percentage and rating?",
    "Which categories should Zepto prioritize for inventory and promotion?",
    "Which categories appear premium based on price and MRP behavior?",
    "Which products or categories show low customer performance and need attention?",
]


def _markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Render a dataframe as a compact Markdown table without optional dependencies."""
    if df.empty:
        return "_No data available._"

    table = df.head(max_rows).copy()
    table = table.fillna("")
    columns = [str(column) for column in table.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in table.iterrows():
        values = [str(value).replace("|", "/") for value in row.tolist()]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def generate_business_questions(output_path: Path = BUSINESS_QUESTIONS_REPORT) -> None:
    """Save business questions before running analysis."""
    content = [
        "# Business Questions",
        "",
        "These questions guide the Zepto EDA project and connect the analysis to business decisions.",
        "",
    ]
    for index, question in enumerate(BUSINESS_QUESTIONS, start=1):
        content.append(f"{index}. {question}")

    output_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    LOGGER.info("Business questions saved to %s", output_path)


def summarize_dataset(df: pd.DataFrame) -> dict[str, pd.DataFrame | tuple[int, int]]:
    """Calculate core dataset exploration outputs."""
    missing = (
        df.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_values"})
    )
    missing["missing_percent"] = (missing["missing_values"] / len(df) * 100).round(2)

    unique_values = (
        df.nunique(dropna=False)
        .reset_index()
        .rename(columns={"index": "column", 0: "unique_values"})
    )

    dtype_summary = (
        df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "column", 0: "data_type"})
    )

    numeric_summary = df.describe(include="number").round(2).T.reset_index()
    numeric_summary = numeric_summary.rename(columns={"index": "metric"})

    categorical_summary = df.describe(include="object").T.reset_index()
    categorical_summary = categorical_summary.rename(columns={"index": "column"})

    return {
        "shape": df.shape,
        "dtypes": dtype_summary,
        "missing": missing,
        "unique": unique_values,
        "numeric_summary": numeric_summary,
        "categorical_summary": categorical_summary,
    }


def generate_data_overview_report(
    df: pd.DataFrame,
    output_path: Path = DATA_OVERVIEW_REPORT,
) -> dict[str, pd.DataFrame | tuple[int, int]]:
    """Write the dataset overview report."""
    summary = summarize_dataset(df)
    rows, columns = summary["shape"]

    sections = [
        "# Data Overview",
        "",
        "## Dataset Shape",
        "",
        f"- Rows: {rows:,}",
        f"- Columns: {columns:,}",
        "",
        "## Data Types",
        "",
        _markdown_table(summary["dtypes"]),
        "",
        "## Missing Values",
        "",
        _markdown_table(summary["missing"]),
        "",
        "## Unique Values",
        "",
        _markdown_table(summary["unique"]),
        "",
        "## Statistical Summary",
        "",
        _markdown_table(summary["numeric_summary"]),
        "",
        "## Categorical Summary",
        "",
        _markdown_table(summary["categorical_summary"]),
    ]

    output_path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    LOGGER.info("Data overview saved to %s", output_path)
    return summary


def run_eda(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run univariate, bivariate, and multivariate EDA summaries."""
    eda_results: dict[str, pd.DataFrame] = {}

    eda_results["category_product_count"] = (
        df["category"].value_counts().head(TOP_N).reset_index()
    )
    eda_results["category_product_count"].columns = ["category", "product_count"]

    eda_results["brand_product_count"] = (
        df["brand"].value_counts().head(TOP_N).reset_index()
    )
    eda_results["brand_product_count"].columns = ["brand", "product_count"]

    eda_results["average_price_by_category"] = (
        df.groupby("category", as_index=False)["price"]
        .mean()
        .sort_values("price", ascending=False)
        .head(TOP_N)
        .round(2)
    )

    eda_results["average_rating_by_category"] = (
        df.groupby("category", as_index=False)["rating"]
        .mean()
        .sort_values("rating", ascending=False)
        .head(TOP_N)
        .round(2)
    )

    eda_results["highest_discount_products"] = (
        df.sort_values(["discount_percent", "savings_amount"], ascending=False)
        .loc[:, ["product_name", "category", "brand", "price", "mrp", "discount_percent"]]
        .head(TOP_N)
        .round(2)
    )

    eda_results["best_value_products"] = (
        df.sort_values("value_score", ascending=False)
        .loc[:, ["product_name", "category", "brand", "price", "rating", "discount_percent", "value_score"]]
        .head(TOP_N)
        .round(3)
    )

    eda_results["category_brand_price"] = (
        df.groupby(["category", "brand"], as_index=False)
        .agg(product_count=("product_name", "count"), average_price=("price", "mean"))
        .sort_values(["product_count", "average_price"], ascending=False)
        .head(TOP_N)
        .round(2)
    )

    LOGGER.info("EDA completed")
    return eda_results

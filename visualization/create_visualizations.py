"""Professional visualizations for the Zepto EDA project."""

from __future__ import annotations

import logging

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config.settings import TOP_N, VISUALIZATION_STYLE, VISUALIZATIONS_DIR


LOGGER = logging.getLogger(__name__)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams.update(VISUALIZATION_STYLE)


def _save_plot(filename: str) -> None:
    """Save the active matplotlib figure to the visualizations directory."""
    output_path = VISUALIZATIONS_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    LOGGER.info("Visualization saved to %s", output_path)


def _top_categories(df: pd.DataFrame) -> list[str]:
    """Return top categories by product count for readable charts."""
    return df["category"].value_counts().head(TOP_N).index.tolist()


def create_univariate_visualizations(df: pd.DataFrame) -> None:
    """Create product count, price, rating, and availability charts."""
    top_category_counts = df["category"].value_counts().head(TOP_N)
    plt.figure()
    sns.barplot(x=top_category_counts.values, y=top_category_counts.index, color="#2f80ed")
    plt.title("Top Categories by Product Count")
    plt.xlabel("Product Count")
    plt.ylabel("Category")
    _save_plot("category_product_count.png")

    plt.figure()
    sns.histplot(df["price"], bins=35, kde=True, color="#27ae60")
    plt.title("Selling Price Distribution")
    plt.xlabel("Selling Price")
    plt.ylabel("Number of Products")
    _save_plot("price_distribution.png")

    plt.figure()
    sns.histplot(df["rating"].dropna(), bins=20, kde=True, color="#f2994a")
    plt.title("Customer Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Products")
    _save_plot("rating_distribution.png")

    if df["availability"].nunique() > 1:
        plt.figure(figsize=(8, 8))
        availability_counts = df["availability"].value_counts()
        plt.pie(
            availability_counts.values,
            labels=availability_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("Set2", len(availability_counts)),
        )
        plt.title("Product Availability Share")
        _save_plot("availability_pie.png")


def create_bivariate_visualizations(df: pd.DataFrame) -> None:
    """Create bivariate charts for pricing, discounts, ratings, and categories."""
    plt.figure()
    sns.scatterplot(
        data=df,
        x="price",
        y="rating",
        hue="availability",
        alpha=0.7,
        edgecolor=None,
    )
    plt.title("Price vs Rating")
    plt.xlabel("Selling Price")
    plt.ylabel("Rating")
    _save_plot("price_vs_rating.png")

    plt.figure()
    sns.scatterplot(
        data=df,
        x="discount_percent",
        y="rating",
        hue="availability",
        alpha=0.7,
        edgecolor=None,
    )
    plt.title("Discount vs Rating")
    plt.xlabel("Discount (%)")
    plt.ylabel("Rating")
    _save_plot("discount_vs_rating.png")

    top_categories = _top_categories(df)
    category_df = df[df["category"].isin(top_categories)]
    plt.figure(figsize=(13, 8))
    sns.boxplot(data=category_df, x="price", y="category", color="#9b51e0")
    plt.title("Category vs Selling Price")
    plt.xlabel("Selling Price")
    plt.ylabel("Category")
    _save_plot("category_price_boxplot.png")

    category_price = (
        df.groupby("category", as_index=False)["price"]
        .mean()
        .sort_values("price", ascending=False)
        .head(TOP_N)
    )
    plt.figure()
    sns.barplot(data=category_price, x="price", y="category", color="#eb5757")
    plt.title("Highest Average Price Categories")
    plt.xlabel("Average Selling Price")
    plt.ylabel("Category")
    _save_plot("category_avg_price.png")


def create_multivariate_visualizations(df: pd.DataFrame) -> None:
    """Create multivariate charts for category, brand, price, discount, and rating."""
    top_categories = _top_categories(df)
    top_brands = df["brand"].value_counts().head(TOP_N).index.tolist()
    heatmap_data = (
        df[df["category"].isin(top_categories) & df["brand"].isin(top_brands)]
        .pivot_table(
            index="category",
            columns="brand",
            values="price",
            aggfunc="mean",
        )
    )

    if not heatmap_data.empty:
        plt.figure(figsize=(13, 8))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False, linewidths=0.5)
        plt.title("Average Price Heatmap: Category vs Brand")
        plt.xlabel("Brand")
        plt.ylabel("Category")
        _save_plot("category_brand_price_heatmap.png")

    category_df = df[df["category"].isin(top_categories)]
    plt.figure(figsize=(13, 8))
    sns.scatterplot(
        data=category_df,
        x="discount_percent",
        y="rating",
        size="price",
        hue="category",
        sizes=(30, 350),
        alpha=0.7,
        edgecolor=None,
    )
    plt.title("Discount vs Rating by Category and Price")
    plt.xlabel("Discount (%)")
    plt.ylabel("Rating")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    _save_plot("discount_rating_category.png")

    numeric_columns = [
        column
        for column in ["price", "mrp", "discount_percent", "savings_amount", "rating", "reviews", "value_score"]
        if column in df.columns
    ]
    correlation = df[numeric_columns].corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", center=0, fmt=".2f")
    plt.title("Correlation Matrix")
    _save_plot("correlation_matrix.png")


def create_all_visualizations(df: pd.DataFrame) -> None:
    """Create all project visualizations."""
    create_univariate_visualizations(df)
    create_bivariate_visualizations(df)
    create_multivariate_visualizations(df)
    LOGGER.info("Visualizations created")

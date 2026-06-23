"""Hypothesis tests for the Zepto EDA project."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from config.settings import HYPOTHESIS_REPORT


LOGGER = logging.getLogger(__name__)


def _safe_pearson(x: pd.Series, y: pd.Series) -> tuple[float, float]:
    """Return Pearson correlation and p-value when enough data exists."""
    valid = pd.concat([x, y], axis=1).dropna()
    if len(valid) < 3 or valid.iloc[:, 0].nunique() < 2 or valid.iloc[:, 1].nunique() < 2:
        return np.nan, np.nan
    correlation, p_value = stats.pearsonr(valid.iloc[:, 0], valid.iloc[:, 1])
    return round(float(correlation), 4), round(float(p_value), 4)


def _safe_ttest(group_a: pd.Series, group_b: pd.Series) -> tuple[float, float]:
    """Run Welch's t-test when both samples have enough observations."""
    group_a = group_a.dropna()
    group_b = group_b.dropna()
    if len(group_a) < 2 or len(group_b) < 2:
        return np.nan, np.nan
    statistic, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
    return round(float(statistic), 4), round(float(p_value), 4)


def _safe_chi_square(table: pd.DataFrame) -> tuple[float, float, int]:
    """Run a chi-square independence test when the contingency table is valid."""
    if table.empty or min(table.shape) < 2 or (table.sum(axis=1) == 0).any():
        return np.nan, np.nan, 0
    statistic, p_value, dof, _ = stats.chi2_contingency(table)
    return round(float(statistic), 4), round(float(p_value), 4), int(dof)


def run_hypothesis_tests(df: pd.DataFrame) -> dict[str, object]:
    """Evaluate project hypotheses using correlation, t-test, and chi-square tests."""
    results: dict[str, object] = {}

    discount_rating_corr, discount_rating_p = _safe_pearson(
        df["discount_percent"],
        df["rating"],
    )
    results["h1_discount_rating_correlation"] = {
        "hypothesis": "Higher discounts increase ratings.",
        "method": "Pearson correlation",
        "statistic": discount_rating_corr,
        "p_value": discount_rating_p,
        "interpretation": (
            "Supported directionally"
            if pd.notna(discount_rating_corr) and discount_rating_corr > 0 and discount_rating_p < 0.05
            else "Not strongly supported"
        ),
    }

    premium_threshold = df["price"].quantile(0.75)
    budget_threshold = df["price"].quantile(0.25)
    premium_ratings = df.loc[df["price"] >= premium_threshold, "rating"]
    budget_ratings = df.loc[df["price"] <= budget_threshold, "rating"]
    t_stat, t_p_value = _safe_ttest(premium_ratings, budget_ratings)
    results["h2_premium_rating_ttest"] = {
        "hypothesis": "Premium products receive better ratings.",
        "method": "Welch's t-test: top price quartile vs bottom price quartile",
        "premium_mean_rating": round(float(premium_ratings.mean()), 3),
        "budget_mean_rating": round(float(budget_ratings.mean()), 3),
        "statistic": t_stat,
        "p_value": t_p_value,
        "interpretation": (
            "Supported"
            if pd.notna(t_stat) and premium_ratings.mean() > budget_ratings.mean() and t_p_value < 0.05
            else "Not strongly supported"
        ),
    }

    category_summary = (
        df.groupby("category")
        .agg(product_count=("product_name", "count"), average_price=("price", "mean"))
        .reset_index()
    )
    popularity_price_corr, popularity_price_p = _safe_pearson(
        category_summary["product_count"],
        category_summary["average_price"],
    )
    results["h3_popular_categories_price_correlation"] = {
        "hypothesis": "Popular categories have lower average prices.",
        "method": "Pearson correlation between category product count and average price",
        "statistic": popularity_price_corr,
        "p_value": popularity_price_p,
        "interpretation": (
            "Supported directionally"
            if pd.notna(popularity_price_corr) and popularity_price_corr < 0 and popularity_price_p < 0.05
            else "Not strongly supported"
        ),
    }

    availability_table = pd.crosstab(df["category"], df["availability"])
    chi_stat, chi_p_value, chi_dof = _safe_chi_square(availability_table)
    results["category_availability_chi_square"] = {
        "hypothesis": "Product availability differs by category.",
        "method": "Chi-square test of independence",
        "statistic": chi_stat,
        "p_value": chi_p_value,
        "degrees_of_freedom": chi_dof,
        "interpretation": (
            "Availability pattern differs by category"
            if pd.notna(chi_p_value) and chi_p_value < 0.05
            else "No statistically strong category availability difference detected"
        ),
    }

    LOGGER.info("Hypothesis testing completed")
    return results


def save_hypothesis_report(
    results: dict[str, object],
    output_path: Path = HYPOTHESIS_REPORT,
) -> None:
    """Save hypothesis testing results as a Markdown report."""
    lines = [
        "# Hypothesis Testing",
        "",
        "Significance is interpreted at alpha = 0.05.",
        "",
    ]

    for key, result in results.items():
        lines.extend(
            [
                f"## {key.replace('_', ' ').title()}",
                "",
                f"- Hypothesis: {result['hypothesis']}",
                f"- Method: {result['method']}",
                f"- Statistic: {result['statistic']}",
                f"- P-value: {result['p_value']}",
                f"- Interpretation: {result['interpretation']}",
                "",
            ]
        )
        for optional_key in ["premium_mean_rating", "budget_mean_rating", "degrees_of_freedom"]:
            if optional_key in result:
                lines.insert(-1, f"- {optional_key.replace('_', ' ').title()}: {result[optional_key]}")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Hypothesis report saved to %s", output_path)

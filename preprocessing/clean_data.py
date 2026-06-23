"""Data loading, dataset selection, and cleaning utilities."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from config.settings import (
    CLEANED_DATA_PATH,
    COLUMN_ALIASES,
    OUTLIER_LOWER_QUANTILE,
    OUTLIER_UPPER_QUANTILE,
    PREFERRED_FIELDS,
    RAW_DATA_DIR,
)


LOGGER = logging.getLogger(__name__)


def standardize_column_name(column: str) -> str:
    """Convert a raw column name into a predictable snake_case name."""
    cleaned = str(column).strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return re.sub(r"_+", "_", cleaned).strip("_")


def _alias_lookup() -> dict[str, str]:
    """Return a mapping from known raw column aliases to canonical names."""
    lookup: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            lookup[standardize_column_name(alias)] = canonical
    return lookup


def _canonical_columns(columns: list[str]) -> set[str]:
    """Map raw column names to known business fields."""
    lookup = _alias_lookup()
    return {lookup.get(standardize_column_name(column), standardize_column_name(column)) for column in columns}


def choose_richest_dataset(raw_data_dir: Path = RAW_DATA_DIR) -> Path:
    """Select the CSV file with the richest Zepto product information."""
    csv_files = sorted(raw_data_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            "No CSV dataset found in data/raw. Download a Zepto product, grocery, "
            "or inventory dataset from Kaggle and place the CSV file in data/raw."
        )

    scored_files: list[tuple[int, int, int, Path]] = []
    for csv_file in csv_files:
        try:
            sample = pd.read_csv(csv_file, nrows=200)
        except Exception as exc:
            LOGGER.warning("Skipping unreadable dataset %s: %s", csv_file, exc)
            continue

        canonical = _canonical_columns(list(sample.columns))
        preferred_score = len(canonical.intersection(PREFERRED_FIELDS))
        row_score = len(sample)
        column_score = len(sample.columns)
        scored_files.append((preferred_score, column_score, row_score, csv_file))

    if not scored_files:
        raise ValueError("CSV files were found in data/raw, but none could be read by pandas.")

    selected = sorted(scored_files, reverse=True)[0][3]
    LOGGER.info("Selected richest dataset: %s", selected)
    return selected


def load_raw_dataset(dataset_path: Path | None = None) -> pd.DataFrame:
    """Load the selected raw Zepto dataset."""
    selected_path = dataset_path or choose_richest_dataset()
    df = pd.read_csv(selected_path)
    LOGGER.info("Dataset loaded from %s with shape %s", selected_path, df.shape)
    return df


def rename_known_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize raw column names and map known aliases to canonical names."""
    alias_lookup = _alias_lookup()
    standardized_columns = [standardize_column_name(column) for column in df.columns]

    rename_map: dict[str, str] = {}
    seen: set[str] = set()
    for original, standardized in zip(df.columns, standardized_columns):
        canonical = alias_lookup.get(standardized, standardized)
        if canonical in seen:
            canonical = f"{standardized}_raw"
        base_name = canonical
        suffix = 2
        while canonical in seen:
            canonical = f"{base_name}_{suffix}"
            suffix += 1
        seen.add(canonical)
        rename_map[original] = canonical

    return df.rename(columns=rename_map)


def _extract_numeric(series: pd.Series) -> pd.Series:
    """Extract numeric values from strings such as Rs. 99, 15%, or 1,200."""
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(-?\d+\.?\d*)", expand=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def _normalize_availability(df: pd.DataFrame) -> pd.Series:
    """Build a consistent In Stock / Out of Stock availability field."""
    if "out_of_stock" in df.columns:
        raw = df["out_of_stock"]
        if pd.api.types.is_bool_dtype(raw):
            return pd.Series(
                np.where(raw, "Out of Stock", "In Stock"),
                index=df.index,
            )

        text = raw.astype(str).str.strip().str.lower()
        out_tokens = {"true", "yes", "out of stock", "outofstock", "unavailable", "1"}
        in_tokens = {"false", "no", "in stock", "instock", "available", "0"}
        standardized = np.where(text.isin(out_tokens), "Out of Stock", np.nan)
        standardized = np.where(text.isin(in_tokens), "In Stock", standardized)
        return pd.Series(standardized, index=df.index).fillna("In Stock")

    if "availability" not in df.columns:
        return pd.Series("In Stock", index=df.index)

    raw = df["availability"]
    if pd.api.types.is_bool_dtype(raw):
        return np.where(raw, "In Stock", "Out of Stock")

    text = raw.astype(str).str.strip().str.lower()
    out_tokens = {"false", "no", "out of stock", "outofstock", "unavailable", "0"}
    in_tokens = {"true", "yes", "in stock", "instock", "available", "1"}

    standardized = np.where(text.isin(out_tokens), "Out of Stock", np.nan)
    standardized = np.where(text.isin(in_tokens), "In Stock", standardized)
    return pd.Series(standardized, index=df.index).fillna("In Stock")


def _normalize_price_scale(df: pd.DataFrame) -> pd.DataFrame:
    """Convert paise-like price columns into rupees when the scale is obvious."""
    for column in ["price", "mrp"]:
        if column in df.columns:
            median_value = df[column].dropna().median()
            if pd.notna(median_value) and median_value > 1000:
                df[column] = df[column] / 100
                LOGGER.info("Converted %s from paise-like scale to rupees", column)
    return df


def _cap_outliers(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Winsorize numeric columns at project-level quantile thresholds."""
    for column in columns:
        if column not in df.columns or df[column].dropna().empty:
            continue
        lower = df[column].quantile(OUTLIER_LOWER_QUANTILE)
        upper = df[column].quantile(OUTLIER_UPPER_QUANTILE)
        if pd.notna(lower) and pd.notna(upper) and lower < upper:
            df[column] = df[column].clip(lower=lower, upper=upper)
    return df


def _prepare_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert expected numeric fields to numeric dtype and derive missing metrics."""
    numeric_candidates = [
        "price",
        "mrp",
        "discount_percent",
        "rating",
        "reviews",
        "available_quantity",
    ]
    for column in numeric_candidates:
        if column in df.columns:
            df[column] = _extract_numeric(df[column])

    if "price" not in df.columns and "mrp" in df.columns:
        df["price"] = df["mrp"]

    if "mrp" not in df.columns and "price" in df.columns:
        df["mrp"] = df["price"]

    df = _normalize_price_scale(df)

    if "discount_percent" not in df.columns:
        df["discount_percent"] = np.nan

    if {"price", "mrp"}.issubset(df.columns):
        valid_price = df["price"].notna() & df["mrp"].notna() & (df["mrp"] > 0)
        derived_discount = ((df["mrp"] - df["price"]) / df["mrp"]) * 100
        df.loc[df["discount_percent"].isna() & valid_price, "discount_percent"] = derived_discount
        df.loc[df["mrp"] < df["price"], "mrp"] = df.loc[df["mrp"] < df["price"], "price"]

    df["discount_percent"] = df["discount_percent"].fillna(0).clip(lower=0, upper=100)

    if "rating" in df.columns:
        df["rating"] = df["rating"].clip(lower=0, upper=5)
    else:
        df["rating"] = np.nan

    if "reviews" not in df.columns:
        df["reviews"] = 0
    df["reviews"] = df["reviews"].fillna(0).clip(lower=0)

    if "available_quantity" not in df.columns:
        df["available_quantity"] = np.nan

    return df


def _prepare_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Fill and normalize expected categorical fields."""
    if "product_name" not in df.columns:
        raise ValueError("The selected dataset must contain a product name or name column.")

    df["product_name"] = df["product_name"].astype(str).str.strip()
    df = df[df["product_name"].ne("") & df["product_name"].str.lower().ne("nan")].copy()

    for column, default in {
        "category": "Unknown",
        "sub_category": "Unknown",
        "brand": "Unbranded",
        "quantity": "Unknown",
    }.items():
        if column not in df.columns:
            df[column] = default
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .replace({"": default, "nan": default, "None": default})
        )

    df["availability"] = _normalize_availability(df)
    return df


def clean_dataset(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean a raw Zepto dataset and return a modeling-ready dataframe."""
    df = rename_known_columns(raw_df).copy()
    original_rows = len(df)

    df = df.drop_duplicates()
    df = _prepare_categorical_columns(df)
    df = _prepare_numeric_columns(df)

    df = df[df["price"].notna() & (df["price"] > 0)].copy()
    df = df[df["mrp"].notna() & (df["mrp"] > 0)].copy()

    if df["rating"].notna().any():
        category_medians = df.groupby("category")["rating"].transform("median")
        global_median = df["rating"].median()
        df["rating_was_missing"] = df["rating"].isna()
        df["rating"] = df["rating"].fillna(category_medians).fillna(global_median)
    else:
        df["rating_was_missing"] = True
        df["rating"] = 3.0

    df = _cap_outliers(df, ["price", "mrp", "reviews", "available_quantity"])

    if "available_quantity" in df.columns:
        df["available_quantity"] = df["available_quantity"].fillna(0).clip(lower=0)

    df["savings_amount"] = (df["mrp"] - df["price"]).clip(lower=0)
    df["value_score"] = (
        (df["rating"].fillna(df["rating"].median() if df["rating"].notna().any() else 3) / 5)
        * (1 + df["discount_percent"] / 100)
        / np.log1p(df["price"])
    )

    desired_order = [
        "product_name",
        "category",
        "sub_category",
        "brand",
        "quantity",
        "price",
        "mrp",
        "discount_percent",
        "savings_amount",
        "rating",
        "reviews",
        "available_quantity",
        "availability",
        "value_score",
        "rating_was_missing",
    ]
    existing_columns = [column for column in desired_order if column in df.columns]
    remaining_columns = [column for column in df.columns if column not in existing_columns]
    df = df[existing_columns + remaining_columns].reset_index(drop=True)

    LOGGER.info(
        "Cleaning completed: %s raw rows -> %s clean rows",
        original_rows,
        len(df),
    )
    return df


def save_cleaned_data(df: pd.DataFrame, output_path: Path = CLEANED_DATA_PATH) -> None:
    """Save cleaned data to the processed data folder."""
    df.to_csv(output_path, index=False)
    LOGGER.info("Cleaned data saved to %s", output_path)


def run_cleaning_pipeline(dataset_path: Path | None = None) -> pd.DataFrame:
    """Load, clean, and save the selected Zepto dataset."""
    raw_df = load_raw_dataset(dataset_path)
    cleaned_df = clean_dataset(raw_df)
    save_cleaned_data(cleaned_df)
    return cleaned_df

"""Main entry point for the Zepto Business Intelligence EDA project."""

from __future__ import annotations

import logging
import sys

from analysis.explore_data import (
    generate_business_questions,
    generate_data_overview_report,
    run_eda,
)
from analysis.hypothesis_testing import run_hypothesis_tests, save_hypothesis_report
from analysis.insight_generator import generate_final_report, generate_insights
from config.settings import PROJECT_LOG_PATH, PROJECT_NAME
from preprocessing.clean_data import run_cleaning_pipeline
from visualization.create_visualizations import create_all_visualizations


def setup_logging() -> None:
    """Configure file and console logging for the project."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(PROJECT_LOG_PATH, mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> None:
    """Run the full Zepto EDA pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting %s", PROJECT_NAME)

        generate_business_questions()
        cleaned_df = run_cleaning_pipeline()
        generate_data_overview_report(cleaned_df)

        eda_results = run_eda(cleaned_df)
        hypothesis_results = run_hypothesis_tests(cleaned_df)
        save_hypothesis_report(hypothesis_results)

        create_all_visualizations(cleaned_df)

        insight_results = generate_insights(cleaned_df)
        generate_final_report(cleaned_df, eda_results, hypothesis_results, insight_results)

        logger.info("Reports generated")
        logger.info("Project completed successfully")

    except Exception as exc:
        logger.exception("Project failed: %s", exc)
        raise


if __name__ == "__main__":
    main()

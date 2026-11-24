# SWYNEX Task 2 — Exploratory Data Analysis

This task continues the UCI Adult / Census Income dataset prepared in Task 1.

## What it does
- Loads the cleaned Task 1 CSV from `Task-1-Data-Cleaning/data/processed/adult_cleaned.csv`
- Prints dataset dimensions, column types and descriptive statistics
- Analyses missing values, numeric distributions and categorical frequencies
- Produces a numeric correlation heatmap and income-group comparisons
- Writes at least five data-derived observations to `outputs/key_insights.txt`
- Saves charts and CSV summary tables under `outputs/`

## Run locally
```bash
python -m pip install -r Task-2-Exploratory-Data-Analysis/requirements.txt
python Task-1-Data-Cleaning/src/clean_data.py
python Task-2-Exploratory-Data-Analysis/eda.py
```

Task 1's data preparation uses the official UCI Adult dataset via `ucimlrepo`. Internet access is required for the first dataset download.

## Reproducibility
A GitHub Actions workflow runs the Task 1 cleaning pipeline followed by this EDA script whenever Task 2 files change. It publishes the generated report and charts as a workflow artifact and commits generated text/CSV reports to this repository.

## Dataset source
UCI Machine Learning Repository — Adult: https://archive.ics.uci.edu/dataset/2/adult

All findings are generated from the loaded dataset at run time; no results are fabricated or hard-coded.

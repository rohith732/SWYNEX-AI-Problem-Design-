# SWYNEX – Data Cleaning & Preparation

Task 1 for the Data Analyst Internship. This project uses the public UCI Adult (Census Income) dataset.

## Dataset
Official source: https://archive.ics.uci.edu/dataset/2/adult
DOI: https://doi.org/10.24432/C5XW20

## Run
```bash
pip install -r requirements.txt
python src/clean_data.py
streamlit run app.py
```

## Workflow
- Standardize column names and trim whitespace.
- Convert `?`, blank, NA and N/A markers to missing values.
- Normalize income labels.
- Remove exact duplicate rows.
- Fill missing categorical values with `Unknown`.
- Convert specified numeric columns and export a quality report.

Outputs are generated locally by running the script: `data/raw/adult_raw.csv`, `data/processed/adult_cleaned.csv`, and `reports/data_quality_report.json`.

The dataset is historical 1994 US Census data; it should not be interpreted as a current population estimate.

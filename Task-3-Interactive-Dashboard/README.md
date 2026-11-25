# SWYNEX Interactive Dashboard — Task 3

An interactive Streamlit dashboard built on the UCI Adult / Census Income dataset used in the earlier SWYNEX tasks.

## Features
- KPI cards: filtered record count, high-income share, average age, average weekly working hours.
- Interactive Plotly charts: income distribution, age distribution by income, education vs income, and top occupations.
- Sidebar filters for age, workclass, education, gender, occupation, marital status, and income category.
- Upload a cleaned CSV and download filtered records.
- Uses Task 1's cleaned CSV when present; otherwise fetches the official UCI dataset and applies the cleaning steps at load time.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

From the existing SWYNEX repository root:
```bash
python -m pip install -r Task-1-Data-Cleaning/requirements.txt
python Task-1-Data-Cleaning/src/clean_data.py
python -m pip install -r Task-3-Interactive-Dashboard/requirements.txt
streamlit run Task-3-Interactive-Dashboard/app.py
```

The app can also run independently and downloads UCI Adult on first launch. Internet access is needed for the initial download. Dataset: https://archive.ics.uci.edu/dataset/2/adult

All metrics and charts are calculated from the active dataset and filters at runtime. Results are not hard-coded. This is descriptive census analysis, not causal inference; avoid interpreting demographic associations as explanations of an individual's income.

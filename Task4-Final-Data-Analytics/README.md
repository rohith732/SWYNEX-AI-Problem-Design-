# SWYNEX Task 4 - Final Data Analytics Project

End-to-end descriptive analytics using the UCI Adult / Census Income dataset.

## Problem
Explore how education, occupation, age, and weekly working hours vary across the two historical income classes (<=50K and >50K). Findings are descriptive, not causal.

## Dataset
UCI Machine Learning Repository, Adult dataset: https://archive.ics.uci.edu/dataset/2/adult
48,842 instances and 14 input attributes plus the income target. Historical 1994 US Census data; not a current labor-market estimate.

## Files
- app.py: Streamlit interactive dashboard
- analysis.py: reproducible cleaning and summary script
- requirements.txt: dependencies
- LINKEDIN_POST.md: post draft

## Run
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py

For command-line cleaning and analysis:
python analysis.py

The app downloads the official adult.data and adult.test files from UCI, normalizes missing markers and test labels, removes exact duplicates, imputes categorical missing values as Unknown, and computes all charts dynamically. No synthetic dataset or hard-coded model accuracy is used.

## Cleaning and analysis
1. Load official train and test files with the documented 15 columns.
2. Convert ? markers to missing values and strip whitespace.
3. Normalize the test income label by removing its trailing period.
4. Remove exact duplicate records.
5. Fill missing categorical values with Unknown for dashboard analysis.
6. Compare income distribution, weekly hours, education, occupation, and age.

## Limitations and responsible use
The dataset reflects 1994 US Census records. Results must not be generalized to current populations or used for consequential hiring, credit, or eligibility decisions. Demographic comparisons are descriptive and do not establish causation.

## Citation
Becker, B. & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20. CC BY 4.0.

This is the Task 4 final case-study folder added to the existing SWYNEX internship repository.

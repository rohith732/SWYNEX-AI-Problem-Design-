import pandas as pd

COLS = ["age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","native-country","income"]
URLS = {
    "Train": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    "Test": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
}

def load_clean():
    frames = []
    for split, url in URLS.items():
        frame = pd.read_csv(url, names=COLS, sep=r"\s*,\s*", engine="python", na_values="?", skipinitialspace=True, skiprows=1 if split == "Test" else 0)
        frame["source_split"] = split
        frame["income"] = frame["income"].astype("string").str.replace(".", "", regex=False).str.strip()
        frames.append(frame)
    raw = pd.concat(frames, ignore_index=True)
    record_cols = [c for c in raw.columns if c != "source_split"]
    duplicate_count = int(raw.duplicated(subset=record_cols).sum())
    clean = raw.drop_duplicates(subset=record_cols).copy()
    missing = clean.isna().sum().sort_values(ascending=False)
    for col in clean.select_dtypes(include=["object", "string"]).columns:
        clean[col] = clean[col].fillna("Unknown").astype(str).str.strip()
    return raw, clean, duplicate_count, missing

if __name__ == "__main__":
    raw, clean, duplicates, missing = load_clean()
    print(f"Raw rows: {len(raw):,}")
    print(f"Clean rows: {len(clean):,}")
    print(f"Exact duplicates removed: {duplicates:,}")
    print("\nMissing values before categorical imputation:")
    print(missing[missing > 0].to_string() or "None")
    print("\nIncome distribution (%):")
    print(clean["income"].value_counts(normalize=True).mul(100).round(2).to_string())
    clean.to_csv("adult_income_cleaned.csv", index=False)
    print("\nSaved adult_income_cleaned.csv")

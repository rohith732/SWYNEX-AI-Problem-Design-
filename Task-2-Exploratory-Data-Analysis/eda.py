from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "Task-1-Data-Cleaning" / "data" / "processed" / "adult_cleaned.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
OUT.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError(
        f"Cleaned Task 1 dataset not found: {DATA}. Run Task-1-Data-Cleaning/src/clean_data.py first."
    )

df = pd.read_csv(DATA)
df.columns = [str(c).strip().lower().replace("-", "_").replace(" ", "_") for c in df.columns]

print("\n=== DATASET OVERVIEW ===")
print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
print("\nColumn types:\n", df.dtypes.to_string())
print("\nDescriptive statistics:\n", df.describe(include="all").T.to_string())

df.head(20).to_csv(OUT / "dataset_preview.csv", index=False)
df.describe(include="all").T.to_csv(OUT / "descriptive_statistics.csv")
missing = df.isna().sum().sort_values(ascending=False)
missing.rename("missing_count").to_csv(OUT / "missing_values.csv")

numeric = df.select_dtypes(include=np.number)
if not numeric.empty:
    for col in numeric.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        fig.tight_layout()
        fig.savefig(CHARTS / f"distribution_{col}.png", dpi=150)
        plt.close(fig)

    corr = numeric.corr(numeric_only=True)
    corr.to_csv(OUT / "numeric_correlations.csv")
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(corr, cmap="vlag", center=0, annot=True, fmt=".2f", ax=ax)
    ax.set_title("Numeric Feature Correlation Heatmap")
    fig.tight_layout()
    fig.savefig(CHARTS / "correlation_heatmap.png", dpi=150)
    plt.close(fig)

categorical = df.select_dtypes(include=["object", "category", "bool", "string"])
for col in categorical.columns:
    counts = df[col].fillna("Missing").astype(str).value_counts().head(12)
    counts.rename("count").to_csv(OUT / f"{col}_frequency.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=counts.values, y=counts.index, ax=ax)
    ax.set_title(f"Top Categories — {col}")
    ax.set_xlabel("Records")
    ax.set_ylabel(col)
    fig.tight_layout()
    fig.savefig(CHARTS / f"categories_{col}.png", dpi=150)
    plt.close(fig)

target = next((c for c in ("income", "salary", "class") if c in df.columns), None)
if target:
    for col in ("education", "occupation", "workclass", "marital_status", "sex"):
        if col in df.columns:
            tab = pd.crosstab(df[col], df[target], normalize="index") * 100
            tab.to_csv(OUT / f"{col}_by_{target}_percentage.csv")
            if len(tab) <= 25:
                ax = tab.plot(kind="bar", stacked=True, figsize=(11, 5))
                ax.set_title(f"{target.title()} Distribution by {col.replace('_', ' ').title()}")
                ax.set_ylabel("Percentage")
                plt.tight_layout()
                plt.savefig(CHARTS / f"{col}_vs_{target}.png", dpi=150)
                plt.close()

insights = [
    f"The cleaned dataset contains {len(df):,} records and {df.shape[1]} columns.",
    f"The dataset contains {int(df.isna().sum().sum()):,} missing cells."
]
if len(missing) and int(missing.max()) > 0:
    insights.append(f"The column with the most missing values is '{missing.index[0]}' ({int(missing.iloc[0]):,}).")
else:
    insights.append("No null values were found in the loaded cleaned dataset.")

if not numeric.empty:
    variances = numeric.var(numeric_only=True).sort_values(ascending=False)
    insights.append(f"'{variances.index[0]}' has the highest numeric variance ({variances.iloc[0]:,.2f}).")
    if numeric.shape[1] > 1:
        abs_corr = numeric.corr(numeric_only=True).abs()
        np.fill_diagonal(abs_corr.values, 0)
        pair = abs_corr.stack().idxmax()
        insights.append(f"The strongest absolute numeric correlation is between '{pair[0]}' and '{pair[1]}' ({abs_corr.loc[pair[0], pair[1]]:.3f}).")
    else:
        insights.append(f"'{numeric.columns[0]}' is the only numeric feature available for correlation analysis.")
else:
    insights.append("No numeric features were detected in the cleaned dataset.")

if target:
    shares = df[target].value_counts(normalize=True, dropna=False) * 100
    insights.append(f"The most common '{target}' category is '{shares.index[0]}' ({shares.iloc[0]:.1f}% of records).")
else:
    insights.append("No recognised income/target column was found for target distribution analysis.")

for col in categorical:
    if len(insights) >= 7:
        break
    vc = df[col].value_counts(dropna=False)
    if len(vc):
        insights.append(f"In '{col}', the most frequent category is '{vc.index[0]}' ({int(vc.iloc[0]):,} records).")

insights = insights[:7]
(OUT / "key_insights.txt").write_text("\n".join(f"{i}. {v}" for i, v in enumerate(insights, 1)) + "\n", encoding="utf-8")
(OUT / "run_summary.txt").write_text(
    f"Dataset: UCI Adult / Census Income\nRows: {len(df)}\nColumns: {df.shape[1]}\n"
    f"Numeric columns: {len(numeric.columns)}\nCategorical columns: {len(categorical.columns)}\n",
    encoding="utf-8"
)
print("\n=== FIVE OR MORE DATA-DERIVED INSIGHTS ===")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")
print(f"\nEDA completed. Outputs: {OUT}")

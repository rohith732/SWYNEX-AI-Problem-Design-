import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="SWYNEX Final Data Analytics", page_icon="📊", layout="wide")
COLS = ["age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","native-country","income"]
TRAIN = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
TEST = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test"

@st.cache_data(show_spinner="Loading official UCI data...")
def load_data():
    train = pd.read_csv(TRAIN, names=COLS, sep=r"\s*,\s*", engine="python", na_values="?", skipinitialspace=True)
    test = pd.read_csv(TEST, names=COLS, sep=r"\s*,\s*", engine="python", na_values="?", skipinitialspace=True, skiprows=1)
    train["source_split"] = "Train"
    test["source_split"] = "Test"
    raw = pd.concat([train, test], ignore_index=True)
    raw["income"] = raw["income"].astype("string").str.replace(".", "", regex=False).str.strip()
    duplicate_count = int(raw.duplicated().sum())
    clean = raw.drop_duplicates().copy()
    for col in clean.select_dtypes(include=["object", "string"]).columns:
        clean[col] = clean[col].fillna("Unknown").astype(str).str.strip()
    return clean, len(raw), duplicate_count

st.markdown("<div style='background:linear-gradient(110deg,#14294d,#274d83);padding:24px;border-radius:16px;color:white'><h1>SWYNEX | Final Data Analytics</h1><p>UCI Adult Census Income • Cleaning • EDA • Business insights</p></div>", unsafe_allow_html=True)
try:
    df, original_rows, duplicates = load_data()
except Exception as exc:
    st.error("Unable to download the official UCI dataset. Check internet access and retry.")
    st.exception(exc)
    st.stop()

st.sidebar.header("Filters")
def select_filter(col):
    return st.sidebar.multiselect(col.replace("-", " ").title(), sorted(df[col].unique()), default=[])
filters = {"workclass":select_filter("workclass"), "education":select_filter("education"), "sex":select_filter("sex"), "income":select_filter("income")}
view = df.copy()
for col, vals in filters.items():
    if vals:
        view = view[view[col].isin(vals)]

st.subheader("Dataset overview")
a,b,c,d = st.columns(4)
a.metric("Original records", f"{original_rows:,}")
b.metric("Clean records", f"{len(df):,}", delta=f"-{duplicates:,} duplicates")
c.metric("Filtered records", f"{len(view):,}")
d.metric("Input attributes", "14")
st.caption("Historical 1994 US Census data. All chart values are calculated from the downloaded UCI dataset.")
left,right = st.columns(2)
with left:
    st.subheader("Income distribution")
    counts = view["income"].value_counts().rename_axis("Income").reset_index(name="Records")
    st.plotly_chart(px.pie(counts, names="Income", values="Records", hole=.5, color_discrete_sequence=["#4169a1","#e6a04b"]), use_container_width=True)
with right:
    st.subheader("Average weekly hours by income")
    hours = view.groupby("income", as_index=False)["hours-per-week"].mean()
    st.plotly_chart(px.bar(hours, x="income", y="hours-per-week", color="income", color_discrete_sequence=["#4169a1","#e6a04b"]), use_container_width=True)
left,right = st.columns(2)
with left:
    st.subheader("Education vs income")
    edu = view.groupby(["education","income"]).size().reset_index(name="Records")
    st.plotly_chart(px.bar(edu, x="education", y="Records", color="income", barmode="group", color_discrete_sequence=["#4169a1","#e6a04b"]), use_container_width=True)
with right:
    st.subheader("Top occupations")
    occ = view["occupation"].value_counts().head(12).rename_axis("Occupation").reset_index(name="Records")
    st.plotly_chart(px.bar(occ, x="Records", y="Occupation", orientation="h", color_discrete_sequence=["#4169a1"]), use_container_width=True)
st.subheader("Age distribution")
st.plotly_chart(px.histogram(view, x="age", color="income", barmode="overlay", opacity=.65, nbins=30, color_discrete_sequence=["#4169a1","#e6a04b"]), use_container_width=True)
st.subheader("Business insights")
hi = view[view.income == ">50K"]
lo = view[view.income == "<=50K"]
if len(view):
    st.write(f"- {len(hi)/len(view)*100:.1f}% of filtered records belong to the >50K income class.")
    st.write(f"- Average weekly hours: >50K = {hi['hours-per-week'].mean():.1f}; <=50K = {lo['hours-per-week'].mean():.1f}.")
    st.write("- Education and occupation charts show descriptive group differences, not causal effects.")
st.subheader("Cleaned data preview")
st.dataframe(view.head(100), use_container_width=True)
st.download_button("Download filtered cleaned CSV", view.to_csv(index=False).encode("utf-8"), "adult_income_cleaned.csv", "text/csv")
st.info("Limitations: this is historical 1994 data, not a current wage benchmark. Do not use demographic patterns for consequential decisions about individuals.")

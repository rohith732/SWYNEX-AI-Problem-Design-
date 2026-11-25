from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from ucimlrepo import fetch_ucirepo

st.set_page_config(page_title="SWYNEX | Census Insights", page_icon="📊", layout="wide")
ROOT = Path(__file__).resolve().parent
LOCAL_DATA = ROOT.parent / "Task-1-Data-Cleaning" / "data" / "processed" / "adult_cleaned.csv"

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:#f5f7fb}.block-container{padding-top:1.5rem;max-width:1500px}
.hero{background:linear-gradient(115deg,#111b3b,#233d76 65%,#2e63a7);padding:28px 32px;border-radius:18px;color:white;margin-bottom:22px}
.hero h1{font-family:Manrope,sans-serif;font-size:30px;font-weight:800;margin:0;color:white}.hero p{margin:7px 0 0;color:#d7e3ff;font-size:14px}
.kpi{background:white;border:1px solid #e7ebf3;border-radius:14px;padding:17px 18px;min-height:105px;box-shadow:0 3px 12px #18274b09}
.kpi-label{font-size:12px;color:#69758c;font-weight:600;text-transform:uppercase;letter-spacing:.06em}.kpi-value{font-family:Manrope,sans-serif;font-size:27px;font-weight:800;color:#14213d;margin-top:7px}.kpi-note{font-size:11px;color:#8792a6;margin-top:2px}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e8edf5}footer{visibility:hidden}
</style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner="Loading the UCI Adult dataset…")
def load_uci_adult():
    ds=fetch_ucirepo(id=2)
    frame=pd.concat([ds.data.features,ds.data.targets],axis=1)
    frame.columns=frame.columns.astype(str).str.strip().str.lower().str.replace(r"[^a-z0-9]+","_",regex=True).str.strip("_")
    for col in frame.select_dtypes(include=["object","string","category"]).columns:
        frame[col]=frame[col].astype("string").str.strip().replace({"?":pd.NA,"":pd.NA,"NA":pd.NA,"N/A":pd.NA,"nan":pd.NA})
    if "income" in frame: frame["income"]=frame["income"].str.rstrip(".")
    frame=frame.drop_duplicates().copy()
    for col in frame.select_dtypes(include=["object","string","category"]).columns: frame[col]=frame[col].fillna("Unknown").astype("string")
    for col in ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"]:
        if col in frame: frame[col]=pd.to_numeric(frame[col],errors="coerce")
    return frame

st.markdown("<div class='hero'><h1>📊 Census Income Insights</h1><p>SWYNEX Technologies · Task 3 — Interactive Dashboard · UCI Adult / Census Income</p></div>",unsafe_allow_html=True)
with st.sidebar:
    st.markdown("### Dashboard controls"); st.caption("Choose a dataset and refine the view.")
    uploaded=st.file_uploader("Upload cleaned CSV (optional)",type=["csv"])
    if uploaded is not None:
        df=pd.read_csv(uploaded); data_source=f"Uploaded file · {uploaded.name}"
    elif LOCAL_DATA.exists():
        df=pd.read_csv(LOCAL_DATA); data_source="Task 1 cleaned dataset"
    else:
        try: df=load_uci_adult(); data_source="UCI Adult dataset · cleaned at load time"
        except Exception as exc:
            st.error("Dataset download failed. Install requirements and retry."); st.code("python -m pip install -r requirements.txt"); st.caption(str(exc)); st.stop()
    df.columns=df.columns.astype(str).str.strip().str.lower().str.replace(r"[^a-z0-9]+","_",regex=True).str.strip("_")
    if not {"income","age"}.issubset(df.columns): st.error("Dataset must contain age and income columns."); st.stop()
    df["age"]=pd.to_numeric(df["age"],errors="coerce")
    lo=int(df.age.min()) if df.age.notna().any() else 0; hi=int(df.age.max()) if df.age.notna().any() else 100
    age_range=st.slider("Age range",lo,max(lo,hi),(lo,max(lo,hi)))
    categorical_filters={}
    for col,label in [("workclass","Workclass"),("education","Education"),("sex","Gender"),("occupation","Occupation"),("marital_status","Marital status")]:
        if col in df:
            vals=sorted(df[col].dropna().astype(str).unique().tolist()); chosen=st.multiselect(label,vals)
            if chosen: categorical_filters[col]=chosen
    income_filter=st.multiselect("Income category",sorted(df.income.dropna().astype(str).unique().tolist()))
    st.caption(f"Source: {data_source}")

filtered=df[df.age.between(*age_range,inclusive="both")].copy()
for col,vals in categorical_filters.items(): filtered=filtered[filtered[col].astype(str).isin(vals)]
if income_filter: filtered=filtered[filtered.income.astype(str).isin(income_filter)]
if filtered.empty: st.warning("No records match the selected filters. Adjust the sidebar filters."); st.stop()
n=len(filtered); high_label=next((v for v in filtered.income.astype(str).unique() if "50" in v or "high" in v.lower()),None)
high_pct=(int((filtered.income.astype(str)==high_label).sum())/n*100) if high_label else 0
avg_age=filtered.age.mean(); avg_hours=pd.to_numeric(filtered["hours_per_week"],errors="coerce").mean() if "hours_per_week" in filtered else float("nan")
cols=st.columns(4)
metrics=[("FILTERED RECORDS",f"{n:,}","Records after current filters"),("HIGH-INCOME SHARE",f"{high_pct:.1f}%","Income category above $50K"),("AVERAGE AGE",f"{avg_age:.1f}","Years · filtered population"),("AVG. WEEKLY HOURS",f"{avg_hours:.1f}" if pd.notna(avg_hours) else "—","Hours per week")]
for col,(label,value,note) in zip(cols,metrics): col.markdown(f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div><div class='kpi-note'>{note}</div></div>",unsafe_allow_html=True)

st.markdown("### Explore the data")
left,right=st.columns(2)
with left:
    counts=filtered.income.astype(str).value_counts().rename_axis("Income group").reset_index(name="Records")
    fig=px.pie(counts,names="Income group",values="Records",hole=.58,title="Income distribution",color_discrete_sequence=["#3157a4","#8ca7dc","#dce5f5"])
    fig.update_layout(margin=dict(t=55,b=10,l=10,r=10),legend_title_text="",paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
with right:
    fig=px.histogram(filtered.dropna(subset=["age"]),x="age",color="income",nbins=28,barmode="overlay",opacity=.78,title="Age distribution by income",color_discrete_sequence=["#3157a4","#f0a34a","#8ca7dc"])
    fig.update_layout(margin=dict(t=55,b=10,l=10,r=10),legend_title_text="Income",paper_bgcolor="white",xaxis_title="Age",yaxis_title="Records"); st.plotly_chart(fig,use_container_width=True)
left,right=st.columns(2)
with left:
    if "education" in filtered:
        edu=filtered.groupby(["education","income"],observed=False).size().reset_index(name="Records")
        fig=px.bar(edu,x="education",y="Records",color="income",barmode="group",title="Education level vs income",color_discrete_sequence=["#3157a4","#f0a34a","#8ca7dc"])
        fig.update_layout(margin=dict(t=55,b=10,l=10,r=10),paper_bgcolor="white",xaxis_title="Education",yaxis_title="Records"); fig.update_xaxes(tickangle=-25); st.plotly_chart(fig,use_container_width=True)
with right:
    if "occupation" in filtered:
        occ=filtered.occupation.astype(str).value_counts().head(10).sort_values().reset_index(); occ.columns=["Occupation","Records"]
        fig=px.bar(occ,x="Records",y="Occupation",orientation="h",title="Top 10 occupations",color="Records",color_continuous_scale="Blues")
        fig.update_layout(margin=dict(t=55,b=10,l=10,r=10),paper_bgcolor="white",coloraxis_showscale=False); st.plotly_chart(fig,use_container_width=True)
st.markdown("### Filtered data preview"); st.caption(f"Showing up to 100 rows · {n:,} matching records · {data_source}")
st.dataframe(filtered.head(100),use_container_width=True,hide_index=True)
st.download_button("⬇ Download filtered CSV",filtered.to_csv(index=False).encode("utf-8"),"swynex_filtered_census_income.csv","text/csv")
st.markdown("<div style='text-align:center;color:#8792a6;font-size:12px;padding:20px 0'>SWYNEX Technologies · Interactive data exploration · UCI Adult dataset</div>",unsafe_allow_html=True)

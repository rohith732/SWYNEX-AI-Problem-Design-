from pathlib import Path
import json
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parent; CSV=ROOT/'data/processed/adult_cleaned.csv'; REPORT=ROOT/'reports/data_quality_report.json'
st.set_page_config(page_title='SWYNEX Data Cleaning',page_icon='🧹',layout='wide'); st.title('SWYNEX – Data Cleaning & Preparation'); st.caption('UCI Adult Census Income dataset')
if not CSV.exists() or not REPORT.exists():
 st.warning('Cleaned files not found. Run python src/clean_data.py first.'); st.code('pip install -r requirements.txt\npython src/clean_data.py\nstreamlit run app.py'); st.stop()
df=pd.read_csv(CSV); r=json.loads(REPORT.read_text()); a,b,c=st.columns(3); a.metric('Cleaned records',f'{len(df):,}'); b.metric('Columns',len(df.columns)); c.metric('Duplicates removed',r['duplicate_rows_removed'])
st.subheader('Cleaned data preview'); st.dataframe(df.head(30),use_container_width=True); st.subheader('Data types'); st.dataframe(pd.DataFrame({'column':df.dtypes.index,'dtype':df.dtypes.astype(str).values}),use_container_width=True)
st.download_button('Download cleaned CSV',CSV.read_bytes(),'adult_cleaned.csv','text/csv'); st.download_button('Download quality report',REPORT.read_bytes(),'data_quality_report.json','application/json')

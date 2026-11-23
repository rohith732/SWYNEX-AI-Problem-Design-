from pathlib import Path
import json
import pandas as pd
from ucimlrepo import fetch_ucirepo
ROOT=Path(__file__).resolve().parents[1]
NUMERIC=['age','fnlwgt','education_num','capital_gain','capital_loss','hours_per_week']
def main():
 for d in ['data/raw','data/processed','reports']:(ROOT/d).mkdir(parents=True,exist_ok=True)
 ds=fetch_ucirepo(id=2); raw=pd.concat([ds.data.features,ds.data.targets],axis=1)
 raw.columns=raw.columns.astype(str).str.strip().str.lower().str.replace(r'[^a-z0-9]+','_',regex=True).str.strip('_')
 raw.to_csv(ROOT/'data/raw/adult_raw.csv',index=False)
 before=len(raw); dup=int(raw.duplicated().sum()); missing=raw.isna().sum().astype(int).to_dict(); df=raw.copy()
 for c in df.select_dtypes(include=['object','string','category']).columns:df[c]=df[c].astype('string').str.strip().replace({'?':pd.NA,'':pd.NA,'NA':pd.NA,'N/A':pd.NA,'nan':pd.NA})
 if 'income' in df:df['income']=df['income'].str.rstrip('.')
 df=df.drop_duplicates().copy()
 for c in df.select_dtypes(include=['object','string','category']).columns:df[c]=df[c].fillna('Unknown').astype('string')
 for c in NUMERIC:
  if c in df:df[c]=pd.to_numeric(df[c],errors='coerce')
 df.to_csv(ROOT/'data/processed/adult_cleaned.csv',index=False)
 report={'dataset':'UCI Adult / Census Income','source':'https://archive.ics.uci.edu/dataset/2/adult','rows_before':int(before),'rows_after':int(len(df)),'columns':int(df.shape[1]),'duplicate_rows_found':dup,'duplicate_rows_removed':int(before-len(df)),'missing_values_before':missing,'missing_values_after':df.isna().sum().astype(int).to_dict(),'dtypes_after':{c:str(t) for c,t in df.dtypes.items()}}
 (ROOT/'reports/data_quality_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(f'Completed: {before:,} -> {len(df):,} rows; removed {before-len(df):,} duplicates.')
if __name__=='__main__':main()

"""Streamlit interface for the SWYNEX SMS spam classification prototype."""
from pathlib import Path
import csv, io, urllib.request, zipfile
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "SMSSpamCollection"
DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

@st.cache_resource(show_spinner="Loading UCI SMS dataset and training the classifier...")
def train_model():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        request = urllib.request.Request(DATA_URL, headers={"User-Agent": "SWYNEX-SMS-Demo/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            archive_bytes = response.read()
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            member = next(name for name in archive.namelist() if Path(name).name == "SMSSpamCollection")
            DATA_FILE.write_bytes(archive.read(member))
    import pandas as pd
    data = pd.read_csv(DATA_FILE, sep="\t", header=None, names=["label", "message"], quoting=csv.QUOTE_NONE, encoding="utf-8").dropna()
    model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("classifier", MultinomialNB()),
    ])
    model.fit(data["message"].astype(str), data["label"].astype(str))
    return model, len(data)

st.set_page_config(page_title="SWYNEX SMS Shield", page_icon="🛡️", layout="centered")
st.title("🛡️ SWYNEX SMS Shield")
st.caption("Task 2 · Model or API Integration")
st.write("Enter an SMS message and let the trained model classify it as likely Spam or Ham.")
model, rows = train_model()
sample1 = "Congratulations! You have won a free prize. Call now to claim your reward!"
sample2 = "Hi, are we still meeting for lunch today?"
choice = st.selectbox("Try an example", ["Choose…", "Promotional message", "Everyday message"])
defaults = {"Choose…": "", "Promotional message": sample1, "Everyday message": sample2}
message = st.text_area("SMS message", value=defaults[choice], height=130, max_chars=5000)
if st.button("Analyse message", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Enter a message first.")
    else:
        prediction = model.predict([message.strip()])[0]
        probabilities = model.predict_proba([message.strip()])[0]
        confidence = float(max(probabilities)) * 100
        if prediction.lower() == "spam":
            st.error("🚨 Likely SPAM")
        else:
            st.success("✓ Likely HAM · Not Spam")
        st.metric("Model confidence estimate", f"{confidence:.1f}%")
        st.progress(max(0, min(100, int(round(confidence)))))
        st.caption("Confidence is an estimated class probability, not proof that a message is safe.")
left, right = st.columns(2)
left.metric("Training messages", f"{rows:,}")
right.metric("Pipeline", "TF-IDF + Naive Bayes")
with st.expander("How it works"):
    st.write("TF-IDF converts message text into numeric features. Multinomial Naive Bayes predicts the label using examples from the UCI SMS Spam Collection.")
st.caption("Dataset: UCI SMS Spam Collection · Almeida & Hidalgo (2011) · CC BY 4.0")
st.caption("Limitations: historical English-language data; less reliable on Tamil, code-mixed text, or new scams. Educational prototype only. Do not enter private SMS messages or use this app to automatically block/delete messages.")

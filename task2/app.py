"""Streamlit interface for the SWYNEX SMS spam classification prototype."""
from pathlib import Path
import sys

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.train import load_dataset  # noqa: E402

st.set_page_config(page_title="SWYNEX SMS Shield", page_icon="🛡️", layout="centered")

@st.cache_resource(show_spinner="Training the SMS classifier on the UCI dataset...")
def get_model():
    data = load_dataset()
    model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("classifier", MultinomialNB()),
    ])
    model.fit(data["message"], data["label"])
    return model, len(data)

model, dataset_size = get_model()

st.title("🛡️ SWYNEX SMS Shield")
st.caption("AI-powered SMS Spam / Ham Detection — Task 2: Model or API Integration")
st.write(
    "Paste an SMS message below. The trained machine-learning model analyses its "
    "text and predicts whether it resembles **Spam** or a legitimate **Ham** message."
)

with st.expander("Try an example"):
    st.code("Congratulations! You have won a free prize. Call now!")
    st.code("Hi, are we still meeting for lunch today?")

message = st.text_area(
    "Enter an SMS message",
    placeholder="Type or paste your SMS here...",
    height=130,
    max_chars=5000,
)

if st.button("Analyse message", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Please enter a message before analysing.")
    else:
        prediction = model.predict([message.strip()])[0]
        probabilities = model.predict_proba([message.strip()])[0]
        confidence = float(max(probabilities)) * 100

        if prediction == "spam":
            st.error("🚨 Prediction: SPAM")
            st.write("This message contains text patterns associated with spam messages.")
        else:
            st.success("✅ Prediction: HAM (Not Spam)")
            st.write("This message looks more like a legitimate message in the training data.")

        st.metric("Model confidence", f"{confidence:.1f}%")
        st.progress(int(round(confidence)))
        st.caption(
            "Confidence is the model's estimated class probability, not a guarantee "
            "that the message is safe."
        )

st.divider()
left, right = st.columns(2)
left.metric("Training messages", f"{dataset_size:,}")
right.metric("Model", "TF-IDF + Naive Bayes")
st.info(
    "Privacy note: the app processes the text entered in this session and does not "
    "store it. Avoid entering private or sensitive SMS messages."
)
st.caption(
    "Prototype limitation: trained on historical English SMS data. It may perform "
    "less well on Tamil, code-mixed, or newly emerging scam messages. Do not use it "
    "to automatically block or delete messages."
)

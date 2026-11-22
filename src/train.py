"""Train and test a simple SMS spam classifier using the UCI dataset."""

from pathlib import Path
import csv
import io
import urllib.request
import zipfile

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "SMSSpamCollection"
MODEL_FILE = ROOT / "spam_classifier.joblib"
DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"


def ensure_dataset() -> None:
    """Download the public dataset from UCI only when it is not already present."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        return

    print("Dataset not found. Downloading the UCI SMS Spam Collection...")
    try:
        with urllib.request.urlopen(DATA_URL, timeout=30) as response:
            archive_bytes = response.read()
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            member = next(
                name for name in archive.namelist()
                if Path(name).name == "SMSSpamCollection"
            )
            DATA_FILE.write_bytes(archive.read(member))
    except (OSError, StopIteration, zipfile.BadZipFile) as exc:
        raise RuntimeError(
            "Could not download or extract the UCI dataset. Check your internet "
            "connection, then download it manually from "
            "https://archive.ics.uci.edu/dataset/228/sms and place the extracted "
            "SMSSpamCollection file inside the project's data folder."
        ) from exc


def main() -> None:
    ensure_dataset()
    data = pd.read_csv(
        DATA_FILE,
        sep="\t",
        header=None,
        names=["label", "message"],
        quoting=csv.QUOTE_NONE,
        encoding="utf-8",
    ).dropna()

    data["label"] = data["label"].astype(str).str.strip().str.lower()
    data["message"] = data["message"].astype(str).str.strip()
    data = data[data["label"].isin(["ham", "spam"]) & data["message"].ne("")]

    if data["label"].nunique() != 2 or len(data) < 10:
        raise ValueError("The dataset must contain enough labelled ham and spam messages.")

    X_train, X_test, y_train, y_test = train_test_split(
        data["message"],
        data["label"],
        test_size=0.20,
        random_state=42,
        stratify=data["label"],
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("classifier", MultinomialNB()),
    ])
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\n=== SMS SPAM CLASSIFICATION RESULTS ===")
    print(f"Total records: {len(data)}")
    print(f"Training records: {len(X_train)}")
    print(f"Test records: {len(X_test)}")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, labels=["ham", "spam"], zero_division=0))
    print("Confusion matrix (rows = actual, columns = predicted; order: ham, spam):")
    print(confusion_matrix(y_test, predictions, labels=["ham", "spam"]))

    joblib.dump(model, MODEL_FILE)
    print(f"\nTrained model saved to: {MODEL_FILE}")

    print("\nEnter an SMS message to test the model (or press Enter to finish):")
    message = input("> ").strip()
    if message:
        prediction = model.predict([message])[0]
        print(f"Prediction: {prediction.upper()}")
        print("Reminder: this is a learning prototype, not a guarantee that a message is safe.")


if __name__ == "__main__":
    main()

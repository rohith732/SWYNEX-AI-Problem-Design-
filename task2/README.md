# SWYNEX Model or API Integration — SMS Spam Detection

## Prototype
A working Streamlit web app that integrates the machine-learning model from Task 1. A user enters an SMS message and receives a **Spam** or **Ham (Not Spam)** prediction with the model's estimated class probability.

## Model and dataset
- Dataset: UCI SMS Spam Collection (5,574 labelled SMS messages; CC BY 4.0).
- Text representation: TF-IDF.
- Classifier: Multinomial Naive Bayes.
- Training: uses the labelled UCI dataset and the same preprocessing family as Task 1.
- Dataset source: https://archive.ics.uci.edu/dataset/228/sms
- Citation: Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection. https://doi.org/10.24432/C5CC84

## Run locally
From the repository root:

```bash
python -m pip install -r requirements.txt
streamlit run task2/app.py
```

On first launch, the app downloads the public UCI dataset using the existing Task 1 dataset loader. An internet connection is required for this first download. The model is trained and cached for the current Streamlit session.

## Example inputs
1. `Congratulations! You have won a free prize. Call now!`
2. `Hi, are we still meeting for lunch today?`

The app displays the actual model prediction when run. Predictions are data-dependent; the examples are not hard-coded outputs.

## Features
- Text input for a message.
- One-click classification.
- Spam / Ham result display.
- Estimated class probability.
- Example messages and privacy/limitations notice.

## Scope and limitations
This is a demonstration prototype, not a production security filter. It does not connect to a phone inbox, scan URLs, verify senders, or automatically block/delete messages. The source dataset is historical and English-language, so results may be weaker on Tamil, code-mixed, and newer scam messages. A high confidence score does not prove a message is safe.

## Task 2 deliverable
This folder demonstrates integration of a trained ML pipeline into a small interactive application, with example inputs and model-generated outputs.

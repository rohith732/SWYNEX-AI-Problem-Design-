# SWYNEX Task 2 — SMS Shield

A small Streamlit prototype integrating a TF-IDF + Multinomial Naive Bayes classifier trained on the UCI SMS Spam Collection.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run task2/app.py
```

The first run downloads the official dataset into task2/data and needs internet access.

## Demonstration
- Enter or select an SMS example.
- Predict likely Spam or Ham.
- Display the model's estimated class probability.
- Show dataset size and model pipeline.

## Dataset and limitations
Almeida, T. & Hidalgo, J. (2011), UCI SMS Spam Collection, https://doi.org/10.24432/C5CC84 (CC BY 4.0). Historical English SMS examples only. This is an educational prototype, not a production spam filter. It may perform less well on Tamil, code-mixed text, and emerging scams. Do not enter private messages or automatically block/delete messages based on this output.

# SWYNEX-AI-Problem-Design
## SMS Spam Message Classification Using Machine Learning

A beginner-friendly AI problem-design project that classifies an SMS message as **Spam** or **Ham (Not Spam)**.

### 1. Problem
Mobile users receive unwanted or misleading SMS messages. Manually checking every message takes time. This project explores a text-classification model that flags likely spam messages.

### 2. Intended user
A mobile phone user who wants an initial warning when an SMS resembles known spam messages. This is a prototype for learning and demonstration, not a production security filter.

### 3. Dataset
- **Name:** UCI SMS Spam Collection
- **Source:** https://archive.ics.uci.edu/dataset/228/sms
- **Size:** 5,574 labelled SMS messages
- **Labels:** `ham` (legitimate) and `spam`
- **License:** CC BY 4.0; retain attribution to the dataset creators.
- **Citation:** Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84

The training script downloads the dataset automatically when it is not found. It saves the extracted `SMSSpamCollection` file inside `data/`.

### 4. Proposed AI approach
1. Read the labelled SMS messages.
2. Split the data into training and test sets using a stratified 80:20 split.
3. Convert text into numerical features with TF-IDF.
4. Train a Multinomial Naive Bayes classifier.
5. Predict `spam` or `ham` for unseen messages.

### 5. Success criteria and evaluation
Evaluate only on the held-out test set. Report accuracy, precision, recall and F1-score for each class, plus a confusion matrix. Pay particular attention to spam recall and precision because false positives and false negatives have different consequences. Record the actual measured values after running the code; do not claim results before testing.

### 6. Constraints and risks
- The dataset contains English SMS messages; performance may be weaker on Tamil, code-mixed or other-language messages.
- The dataset is historical and may not represent current scam patterns.
- Message wording can change; new spam styles may be missed.
- False positives may hide legitimate messages; false negatives may allow spam through.
- Do not use this prototype to automatically delete or block messages.
- Do not upload private SMS messages or personal data.
- This is a demonstration model, not a guarantee that a message is safe.

### 7. How to run
Install Python 3.9+ and run:

```bash
python -m pip install -r requirements.txt
python src/train.py
```

The first run needs an internet connection to download the public UCI dataset. The script prints the test metrics and then lets you try one SMS message.

### 8. Measured baseline result

The 80:20 stratified test run achieved **97.31% accuracy** across 1,115 held-out messages. For the spam class, precision was **100.00%**, recall was **79.87%**, and F1-score was **88.81%**. The confusion matrix shows that 30 spam messages were missed. See [the full evaluation report](reports/evaluation.md).

### 9. Project scope
This task focuses only on binary SMS text classification. It does not include live phone integration, URL scanning, sender verification, deep learning or automatic message blocking.

### 10. Future improvements
- Add Tamil and code-mixed SMS examples.
- Evaluate on a newer, separately collected dataset.
- Compare Naive Bayes with Logistic Regression.
- Build a simple Streamlit demo after evaluating the baseline.

See [problem_design.md](problem_design.md) for the full AI problem design, [reports/evaluation.md](reports/evaluation.md) for the measured test results, [BEGINNER_SETUP_GUIDE.md](BEGINNER_SETUP_GUIDE.md) for Windows setup instructions and [LINKEDIN_VIDEO_SCRIPT.md](LINKEDIN_VIDEO_SCRIPT.md) for a short presentation script. A GitHub Actions workflow reruns training and evaluation when the project code or workflow changes.

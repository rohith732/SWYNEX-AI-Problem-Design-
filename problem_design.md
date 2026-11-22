# AI Problem Design Document
## SMS Spam Message Classification Using Machine Learning

### Problem statement
How can a text-classification model help a mobile phone user identify whether an incoming SMS is likely to be spam or legitimate?

### User
The intended user is an everyday mobile phone user who wants an initial warning about suspicious SMS messages.

### Input and output
- **Input:** The text content of one SMS message.
- **Output:** One of two labels: `spam` or `ham` (legitimate).

### Data source
The project uses the UCI SMS Spam Collection, a public labelled dataset containing 5,574 SMS messages. Dataset page: https://archive.ics.uci.edu/dataset/228/sms. The dataset is licensed under CC BY 4.0. Citation: Almeida, T. & Hidalgo, J. (2011), https://doi.org/10.24432/C5CC84.

### Proposed method
Use a TF-IDF text representation and a Multinomial Naive Bayes classifier. A stratified 80:20 train/test split will preserve the approximate class proportions. The test set will be held out from model training.

### Evaluation approach
Report accuracy, per-class precision, recall, F1-score and a confusion matrix on the held-out test set. Give particular attention to spam recall and precision because the two error types have different consequences. No performance result is assumed in advance; measured results must be added after execution.

### Constraints
1. Dataset messages are in English.
2. Dataset examples are historical and may not represent modern spam.
3. The dataset is imbalanced, so accuracy alone can be misleading.
4. The model may incorrectly flag legitimate messages or miss spam.
5. The model is a learning prototype and must not automatically delete or block messages.
6. Personal or private SMS messages should not be uploaded to the project.

### Success criteria
The experiment is successful if it:
- Runs reproducibly using the documented steps.
- Produces both `spam` and `ham` predictions.
- Reports all specified evaluation metrics on unseen test data.
- Discusses limitations and false-positive/false-negative risks honestly.

### Observed baseline results
The implemented baseline was evaluated on the stratified test split. It achieved 97.31% accuracy. For the spam class, precision was 1.0000, recall was 0.7987 and F1-score was 0.8881. The confusion matrix recorded 119 correctly identified spam messages and 30 spam messages predicted as ham. Full metrics are documented in [reports/evaluation.md](reports/evaluation.md).

### Scope boundary
This project designs and evaluates a binary SMS text classifier. It does not implement a mobile application, sender authentication, malicious-link analysis or real-time carrier integration.

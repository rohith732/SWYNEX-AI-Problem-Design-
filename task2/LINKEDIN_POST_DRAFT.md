I’ve been working on a small machine-learning prototype for SMS spam detection as part of Task 2 with SWYNEX Technologies.

The idea is simple: enter a text message and let a trained model classify it as likely **Spam** or **Ham (not spam)**.

For the prototype, I connected a TF-IDF text-processing pipeline with a Multinomial Naive Bayes classifier and built a lightweight interface using Python and Streamlit. I also included example messages and a confidence estimate so the prediction is easier to understand.

One important takeaway: a model prediction is not a guarantee. The dataset is historical and English-focused, so this demo should be treated as a learning prototype—not a replacement for a phone’s spam protection, especially for Tamil or code-mixed messages.

Project and source code: https://github.com/rohith732/SWYNEX-AI-Problem-Design-

Thanks to SWYNEX Technologies for the opportunity to practise connecting an ML model to a user-facing application.

@SWYNEX Technologies

#SWYNEX #Internship #MachineLearning #Python #Streamlit #NLP #SpamDetection

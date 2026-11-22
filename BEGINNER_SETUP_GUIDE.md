# Task 1 — Beginner Setup Guide (Windows)

## Before you begin
You need an internet connection for the first dataset download. The model code downloads the public UCI dataset automatically when it is not found in `data/`.

## Step 1 — Extract the project
1. Open your **Downloads** folder.
2. Right-click the project ZIP file.
3. Choose **Extract All**.
4. Open the extracted project folder.

## Step 2 — Install Python
1. Download Python 3.9 or newer from https://www.python.org/downloads/.
2. Run the installer.
3. On the first installer screen, tick **Add Python to PATH**.
4. Complete the installation.

To check installation, open Command Prompt and run:

```bat
python --version
```

If that command does not work, try:

```bat
py --version
```

## Step 3 — Open the project terminal
1. Open the project folder in File Explorer.
2. Click the address bar, type `cmd`, and press Enter.
3. A Command Prompt opens in the project folder.

## Step 4 — Install the required libraries
Run:

```bat
python -m pip install -r requirements.txt
```

If `python` is not recognized but `py --version` works, use:

```bat
py -m pip install -r requirements.txt
```

## Step 5 — Run the model
Run:

```bat
python src/train.py
```

Or use `py src/train.py` when your computer uses the `py` launcher.

The first run downloads the UCI SMS Spam Collection. Wait for the evaluation report. Then enter a sample SMS when prompted, or press Enter to finish.

## Step 6 — Save a screenshot
Take a screenshot of the terminal showing:
- total, training and test record counts;
- accuracy and the classification report;
- confusion matrix;
- one sample prediction, if available.

Do not edit or invent metric values. If dataset download fails, download it from https://archive.ics.uci.edu/dataset/228/sms and put the extracted file named `SMSSpamCollection` in the project's `data` folder.

## Important
Do not upload private SMS messages, passwords, phone numbers or personal information. This is a learning prototype; it must not automatically block or delete messages.

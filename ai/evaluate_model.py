import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# Load dataset
data = pd.read_csv("dataset.csv")

# Features
X = data[["heart_rate", "temperature"]]

# Target
y = data["status"]


# Same split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Load trained model
model = joblib.load("model.pkl")


# Predict
predictions = model.predict(X_test)


# Calculate metrics
accuracy = accuracy_score(y_test, predictions)

precision = precision_score(
    y_test,
    predictions,
    pos_label="abnormal"
)

recall = recall_score(
    y_test,
    predictions,
    pos_label="abnormal"
)

f1 = f1_score(
    y_test,
    predictions,
    pos_label="abnormal"
)


print("\n========== AI MODEL EVALUATION ==========")

print("Accuracy  :", round(accuracy * 100, 2), "%")
print("Precision :", round(precision * 100, 2), "%")
print("Recall    :", round(recall * 100, 2), "%")
print("F1-Score  :", round(f1 * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("==========================================")
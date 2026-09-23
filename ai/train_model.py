import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


# Load dataset
data = pd.read_csv("dataset.csv")

# Input features
X = data[["heart_rate", "temperature"]]

# Target
y = data["status"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Test
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("========== AI MODEL ==========")
print("Model: Random Forest")
print("Training samples:", len(X_train))
print("Testing samples :", len(X_test))
print("Accuracy        :", round(accuracy * 100, 2), "%")


# Save model
joblib.dump(model, "model.pkl")

print("Model saved as: model.pkl")
print("==============================")
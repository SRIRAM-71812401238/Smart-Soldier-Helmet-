import joblib


# Load trained AI model
model = joblib.load("model.pkl")


def predict_health(heart_rate, temperature):

    prediction = model.predict([
        [heart_rate, temperature]
    ])

    status = prediction[0]

    print("\n========== AI HEALTH PREDICTION ==========")
    print("Heart Rate  :", heart_rate, "BPM")
    print("Temperature :", temperature, "°C")
    print("AI Prediction:", status.upper())

    if status == "abnormal":
        print("🚨 HEALTH WARNING")
    else:
        print("✓ HEALTH STATUS NORMAL")

    print("==========================================")

    return status


# Simulated live sensor reading
heart_rate = 145
temperature = 38.7

predict_health(heart_rate, temperature)
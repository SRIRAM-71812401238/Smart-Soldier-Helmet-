from datetime import datetime
import math
import os
import joblib


# ============================================================
# SMART SOLDIER HELMET - INTEGRATED SOFTWARE PROTOTYPE
# ============================================================


# -------------------- RFID AUTHENTICATION --------------------

AUTHORIZED_RFID = {
    "A1B2C3D4": "Soldier_001",
    "B2C3D4E5": "Soldier_002",
    "C3D4E5F6": "Soldier_003"
}


def authenticate_rfid(rfid_id):

    if rfid_id in AUTHORIZED_RFID:

        soldier = AUTHORIZED_RFID[rfid_id]

        print("\n✓ AUTHENTICATION SUCCESSFUL")
        print("✓ Soldier:", soldier)
        print("✓ Helmet Activated")

        return True, soldier

    else:

        print("\n✗ AUTHENTICATION FAILED")
        print("✗ Unauthorized RFID")
        print("✗ Helmet Locked")

        return False, None


# -------------------- AI MODEL --------------------

# Find model.pkl inside the ai folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ai", "model.pkl")

model = joblib.load(MODEL_PATH)


def predict_health(heart_rate, temperature):

    prediction = model.predict([
        [heart_rate, temperature]
    ])

    return prediction[0]


# -------------------- GEO-FENCING --------------------

ZONE_LATITUDE = 11.0168
ZONE_LONGITUDE = 76.9558

ZONE_RADIUS = 500


def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371000

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def check_geofence(latitude, longitude):

    distance = calculate_distance(
        ZONE_LATITUDE,
        ZONE_LONGITUDE,
        latitude,
        longitude
    )

    if distance <= ZONE_RADIUS:
        return "INSIDE", distance

    else:
        return "OUTSIDE", distance


# -------------------- EMERGENCY ENGINE --------------------

def evaluate_emergency(
    authentication_status,
    health_status,
    geofence_status
):

    if authentication_status != "AUTHORIZED":

        return "UNAUTHORIZED"

    if health_status == "abnormal" and geofence_status == "OUTSIDE":

        return "CRITICAL"

    elif health_status == "abnormal":

        return "HEALTH_ALERT"

    elif geofence_status == "OUTSIDE":

        return "GEOFENCE_ALERT"

    else:

        return "NORMAL"


# ============================================================
# MAIN PROGRAM
# ============================================================

print("\n")
print("================================================")
print("        AI-ENABLED SMART SOLDIER HELMET")
print("================================================")


# -------------------- RFID --------------------

rfid_id = input("\nScan RFID card: ")

authenticated, soldier_id = authenticate_rfid(rfid_id)


# Stop if unauthorized
if not authenticated:

    print("\nSystem stopped.")
    print("Unauthorized access detected.")

else:

    # -------------------- SIMULATED SENSOR DATA --------------------

    heart_rate = 78
    temperature = 36.7

    latitude = 11.0168
    longitude = 76.9558


    # -------------------- DISPLAY SENSOR DATA --------------------

    print("\n========== SENSOR DATA ==========")

    print("Soldier ID   :", soldier_id)
    print("Heart Rate   :", heart_rate, "BPM")
    print("Temperature  :", temperature, "°C")
    print("Latitude     :", latitude)
    print("Longitude    :", longitude)

    print(
        "Time         :",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print("=================================")


    # -------------------- AI HEALTH PREDICTION --------------------

    health_prediction = predict_health(
        heart_rate,
        temperature
    )

    print("\n========== AI ANALYSIS ==========")
    print("AI Prediction:", health_prediction.upper())

    if health_prediction == "abnormal":

        print("🚨 HEALTH WARNING")

    else:

        print("✓ HEALTH STATUS NORMAL")

    print("=================================")


    # -------------------- GEO-FENCE --------------------

    geofence_status, distance = check_geofence(
        latitude,
        longitude
    )

    print("\n========== GEO-FENCE ==========")

    print(
        "Distance from safe zone:",
        round(distance, 2),
        "meters"
    )

    print("Geo-Fence Status:", geofence_status)

    if geofence_status == "OUTSIDE":

        print("🚨 GEO-FENCE ALERT")

    else:

        print("✓ Soldier is inside safe zone")

    print("================================")


    # -------------------- EMERGENCY ENGINE --------------------

    final_status = evaluate_emergency(
        "AUTHORIZED",
        health_prediction,
        geofence_status
    )


    print("\n========== FINAL STATUS ==========")

    if final_status == "NORMAL":

        print("✓ SYSTEM STATUS: NORMAL")
        print("✓ Soldier is safe according to current simulation.")

    elif final_status == "HEALTH_ALERT":

        print("⚠ HEALTH ALERT")
        print("⚠ Abnormal health condition detected.")

    elif final_status == "GEOFENCE_ALERT":

        print("⚠ GEO-FENCE ALERT")
        print("⚠ Soldier has moved outside the assigned zone.")

    elif final_status == "CRITICAL":

        print("🚨 CRITICAL EMERGENCY")
        print("🚨 Abnormal health + outside safe zone.")
        print("🚨 Emergency alert required.")

    print("=================================")
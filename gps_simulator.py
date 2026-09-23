import requests
import time
import math

FIREBASE_URL = "https://smart-soldier-helmet-default-rtdb.firebaseio.com"

SOLDIER_ID = "Soldier_001"

# Safe-zone center
CENTER_LAT = 11.0168
CENTER_LON = 76.9558


def generate_location(step):

    # Simulated movement
    radius = 0.0005

    latitude = CENTER_LAT + radius * math.sin(step / 5)

    longitude = CENTER_LON + radius * math.cos(step / 5)

    return latitude, longitude


step = 0

print("\n======================================")
print("   SMART SOLDIER GPS SIMULATOR")
print("======================================")
print("Press CTRL + C to stop\n")


while True:

    latitude, longitude = generate_location(step)

    data = {
        "heart_rate": 70,
        "temperature": 36.7,
        "latitude": latitude,
        "longitude": longitude,
        "status": "NORMAL"
    }

    url = FIREBASE_URL + "/" + SOLDIER_ID + ".json"

    try:

        response = requests.put(
            url,
            json=data,
            timeout=5
        )

        if response.status_code == 200:

            print(
                f"GPS → "
                f"Lat: {latitude:.6f} | "
                f"Lon: {longitude:.6f}"
            )

        else:

            print(
                "Firebase error:",
                response.status_code
            )

    except requests.RequestException as error:

        print(
            "Connection error:",
            error
        )

    step += 1

    time.sleep(2)
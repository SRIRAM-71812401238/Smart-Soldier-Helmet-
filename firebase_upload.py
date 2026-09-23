import requests
from firebase_config import FIREBASE_URL

data = {
    "heart_rate": 70,
    "temperature": 36.7,
    "latitude": 11.0168,
    "longitude": 76.9558,
    "status": "NORMAL"
}

url = FIREBASE_URL + "/Soldier_001.json"

response = requests.put(url, json=data)

print("Firebase Response:", response.status_code)

if response.status_code == 200:
    print("✓ Data uploaded successfully!")
else:
    print("✗ Upload failed")
    print(response.text)
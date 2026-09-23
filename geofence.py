# Geo-Fencing Module

import math


# Assigned safe-zone center
ZONE_LATITUDE = 11.0168
ZONE_LONGITUDE = 76.9558

# Safe-zone radius in meters
ZONE_RADIUS = 500


def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371000  # meters

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

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c

    return distance


def check_geofence(latitude, longitude):

    distance = calculate_distance(
        ZONE_LATITUDE,
        ZONE_LONGITUDE,
        latitude,
        longitude
    )

    print("\n========== GEO-FENCE ==========")
    print("Soldier Latitude :", latitude)
    print("Soldier Longitude:", longitude)
    print("Distance from zone:", round(distance, 2), "meters")

    if distance <= ZONE_RADIUS:

        print("Status: INSIDE SAFE ZONE")
        print("Geo-Fence: NORMAL")

        return "INSIDE"

    else:

        print("Status: OUTSIDE SAFE ZONE")
        print("Geo-Fence: ALERT")

        return "OUTSIDE"


# Test location
latitude = 11.0168
longitude = 76.9558

check_geofence(latitude, longitude)
# GPS Module


def get_gps_location():
    """
    Simulated GPS data.
    Later this will be replaced by the real GPS module.
    """

    latitude = 11.0168
    longitude = 76.9558

    return latitude, longitude


# Test GPS
latitude, longitude = get_gps_location()

print("\n========== GPS LOCATION ==========")
print("Latitude :", latitude)
print("Longitude:", longitude)
print("==================================")
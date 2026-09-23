# Emergency Decision Engine


def evaluate_emergency(
    authentication_status,
    health_status,
    geofence_status
):

    print("\n========== EMERGENCY ENGINE ==========")

    print("Authentication :", authentication_status)
    print("Health Status  :", health_status)
    print("Geo-Fence     :", geofence_status)

    # Authentication check
    if authentication_status != "AUTHORIZED":

        print("\n🚨 ALERT: UNAUTHORIZED USER")
        print("Helmet Status: LOCKED")

        return "UNAUTHORIZED"

    # Emergency conditions
    if health_status == "WARNING" and geofence_status == "OUTSIDE":

        print("\n🚨 CRITICAL EMERGENCY")
        print("Reason: Health abnormal + Outside safe zone")
        print("Action: Emergency Alert")

        return "CRITICAL"

    elif health_status == "WARNING":

        print("\n⚠ HEALTH EMERGENCY")
        print("Action: Health Alert")

        return "HEALTH_ALERT"

    elif geofence_status == "OUTSIDE":

        print("\n⚠ GEO-FENCE ALERT")
        print("Action: Location Alert")

        return "GEOFENCE_ALERT"

    else:

        print("\n✓ SYSTEM STATUS: NORMAL")

        return "NORMAL"


# Test case

authentication_status = "AUTHORIZED"
health_status = "NORMAL"
geofence_status = "INSIDE"

evaluate_emergency(
    authentication_status,
    health_status,
    geofence_status
)
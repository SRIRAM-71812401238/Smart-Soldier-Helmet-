# Health Monitoring Module


def check_health(heart_rate, temperature):

    print("\n========== HEALTH MONITORING ==========")
    print("Heart Rate  :", heart_rate, "BPM")
    print("Temperature :", temperature, "°C")

    # Basic safety checks for our simulation
    if heart_rate < 50 or heart_rate > 120:
        heart_status = "ABNORMAL"
    else:
        heart_status = "NORMAL"

    if temperature < 35.0 or temperature > 38.0:
        temperature_status = "ABNORMAL"
    else:
        temperature_status = "NORMAL"

    print("Heart Rate Status :", heart_status)
    print("Temperature Status:", temperature_status)

    if heart_status == "ABNORMAL" or temperature_status == "ABNORMAL":
        overall_status = "WARNING"
    else:
        overall_status = "NORMAL"

    print("Overall Health    :", overall_status)
    print("========================================")

    return overall_status


# Simulated sensor readings
heart_rate = 78
temperature = 36.7

check_health(heart_rate, temperature)
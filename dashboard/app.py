import streamlit as st
import requests
import math
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Smart Soldier Helmet",
    page_icon="🪖",
    layout="wide"
)


# ============================================================
# FIREBASE CONFIGURATION
# ============================================================

FIREBASE_URL = (
    "https://smart-soldier-helmet-default-rtdb.firebaseio.com"
)

SOLDIER_ID = "Soldier_001"


# ============================================================
# SREC CAMPUS GEO-FENCE CONFIGURATION
# ============================================================

# Official SREC campus reference coordinate
SREC_LATITUDE = 11.101802
SREC_LONGITUDE = 76.966400

# Prototype campus geo-fence radius.
# This is an operational approximation, not an exact legal campus boundary.
SREC_GEOFENCE_RADIUS = 300

ZONE_LATITUDE = SREC_LATITUDE
ZONE_LONGITUDE = SREC_LONGITUDE
ZONE_RADIUS = SREC_GEOFENCE_RADIUS


# ============================================================
# FIREBASE DATA
# ============================================================

firebase_data = None

try:

    response = requests.get(
        FIREBASE_URL + f"/{SOLDIER_ID}.json",
        timeout=5
    )

    if response.status_code == 200:
        firebase_data = response.json()

except requests.RequestException:

    firebase_data = None


# ============================================================
# READ SENSOR DATA
# ============================================================

soldier_id = SOLDIER_ID

if firebase_data:

    heart_rate = firebase_data.get(
        "heart_rate",
        0
    )

    temperature = firebase_data.get(
        "temperature",
        0
    )

    firebase_status = firebase_data.get(
        "status",
        "UNKNOWN"
    )

else:

    heart_rate = 0
    temperature = 0
    firebase_status = "NO DATA"


# ============================================================
# DISTANCE FUNCTION
# ============================================================

def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    earth_radius = 6371000

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(
        lat2 - lat1
    )

    delta_lon = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {

    background:
    radial-gradient(
        circle at top right,
        #1b2418,
        #0b0f0c 45%,
        #050705
    );

}

.block-container {

    max-width: 1500px;

    padding-top: 25px;

    padding-bottom: 40px;

}


/* HEADER */

.command-header {

    background:
    linear-gradient(
        135deg,
        #111811,
        #1a2117
    );

    border: 1px solid #3e4d32;

    border-left: 6px solid #aebd72;

    border-radius: 12px;

    padding: 25px 30px;

    margin-bottom: 25px;

    box-shadow:
    0 0 25px
    rgba(120,140,70,0.12);

}


.command-title {

    font-family: monospace;

    font-size: 34px;

    font-weight: 900;

    color: #c7d36f;

    letter-spacing: 3px;

}


.command-subtitle {

    font-family: monospace;

    font-size: 13px;

    color: #9aa88d;

    letter-spacing: 2px;

    margin-top: 8px;

}


.command-status {

    font-family: monospace;

    font-size: 12px;

    color: #8faf69;

    letter-spacing: 1px;

    margin-top: 15px;

}


/* SECTION */

.section-title {

    font-family: monospace;

    font-size: 17px;

    font-weight: 800;

    color: #b9c87b;

    letter-spacing: 2px;

    border-left: 4px solid #8e9f58;

    padding-left: 10px;

    margin-top: 12px;

    margin-bottom: 16px;

}


/* METRICS */

[data-testid="stMetric"] {

    background:
    linear-gradient(
        145deg,
        #151c15,
        #101610
    );

    border: 1px solid #37442f;

    border-radius: 12px;

    padding: 18px;

    min-height: 110px;

    box-shadow:
    0 5px 18px
    rgba(0,0,0,0.25);

}


[data-testid="stMetricLabel"] {

    color: #8f9d85 !important;

    font-family: monospace;

    font-size: 11px;

    letter-spacing: 1px;

}


[data-testid="stMetricValue"] {

    color: #dce6d7 !important;

    font-family: monospace;

    font-weight: 800;

}


/* NORMAL */

.normal-box {

    background: #102016;

    border: 1px solid #3c7048;

    border-radius: 12px;

    padding: 22px;

    color: #a7dca5;

    font-family: monospace;

}


/* WARNING */

.warning-box {

    background: #211e0e;

    border: 1px solid #8b7a35;

    border-radius: 12px;

    padding: 22px;

    color: #e0cf75;

    font-family: monospace;

}


/* CRITICAL */

.critical-box {

    background: #250f0f;

    border: 1px solid #8b3c3c;

    border-radius: 12px;

    padding: 22px;

    color: #ff9999;

    font-family: monospace;

}


/* INFORMATION */

.info-box {

    background: #111917;

    border: 1px solid #35463d;

    border-radius: 12px;

    padding: 20px;

    color: #aebbb0;

    font-family: monospace;

    min-height: 150px;

}


/* TACTICAL CARD */

.tactical-card {

    background:
    linear-gradient(
        145deg,
        #131a13,
        #0e130e
    );

    border: 1px solid #34402e;

    border-radius: 12px;

    padding: 22px;

    min-height: 130px;

}


.card-title {

    font-family: monospace;

    color: #89977e;

    font-size: 11px;

    letter-spacing: 2px;

}


.card-value {

    font-family: monospace;

    color: #c7d36f;

    font-size: 25px;

    font-weight: 900;

    margin-top: 12px;

}


/* FOOTER */

.footer {

    text-align: center;

    color: #596451;

    font-family: monospace;

    font-size: 11px;

    margin-top: 35px;

    padding: 18px;

    border-top: 1px solid #293328;

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="command-header">'
    '<div class="command-title">'
    '🪖 SMART SOLDIER HELMET'
    '</div>'
    '<div class="command-subtitle">'
    'AI-ENABLED TACTICAL MONITORING & COMMAND CENTER'
    '</div>'
    '<div class="command-status">'
    '● SYSTEM ONLINE &nbsp; | &nbsp; '
    'SECURE MONITORING &nbsp; | &nbsp; '
    'LIVE DATA LINK'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    'SYSTEM OVERVIEW'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "SOLDIER ID",
        soldier_id
    )


with col2:

    st.metric(
        "HEART RATE",
        f"{heart_rate} BPM"
    )


with col3:

    st.metric(
        "BODY TEMPERATURE",
        f"{temperature} °C"
    )


with col4:

    if firebase_status == "NORMAL":

        overview_status = "OPERATIONAL"

    elif firebase_status == "HEALTH ALERT":

        overview_status = "HEALTH ALERT"

    elif firebase_status == "CRITICAL":

        overview_status = "CRITICAL"

    else:

        overview_status = firebase_status

    st.metric(
        "HEALTH STATUS",
        overview_status
    )


st.divider()


# ============================================================
# COMPUTER PHYSICAL LOCATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📍 LIVE COMPUTER LOCATION'
    '</div>',
    unsafe_allow_html=True
)


location = streamlit_geolocation()


# Default values

display_latitude = 0

display_longitude = 0

location_accuracy = None

distance = 0

location_detected = False


if (
    location
    and
    location.get("latitude") is not None
    and
    location.get("longitude") is not None
):

    location_detected = True

    display_latitude = location["latitude"]

    display_longitude = location["longitude"]

    location_accuracy = location.get(
        "accuracy"
    )

    distance = calculate_distance(
        ZONE_LATITUDE,
        ZONE_LONGITUDE,
        display_latitude,
        display_longitude
    )


    map_data = {

        "latitude": [
            display_latitude
        ],

        "longitude": [
            display_longitude
        ]

    }


    map_col, location_col = st.columns(
        [2, 1]
    )


    with map_col:

        st.map(map_data)


    with location_col:

        st.metric(
            "LATITUDE",
            f"{display_latitude:.6f}"
        )

        st.metric(
            "LONGITUDE",
            f"{display_longitude:.6f}"
        )

        if location_accuracy is not None:

            st.metric(
                "ACCURACY",
                f"{location_accuracy:.0f} m"
            )

        else:

            st.metric(
                "ACCURACY",
                "N/A"
            )

        st.metric(
            "DISTANCE FROM SREC CAMPUS",
            f"{distance:.2f} m"
        )

        st.metric(
            "SREC GEO-FENCE RADIUS",
            f"{ZONE_RADIUS} m"
        )


    # ========================================================
    # GEO-FENCE
    # ========================================================

    if distance <= ZONE_RADIUS:

        geofence_status = "INSIDE"

        st.markdown(
            '<div class="normal-box">'
            '<h3>🟢 SOLDIER INSIDE SREC CAMPUS</h3>'
            '<p>'
            'Computer is currently inside the '
            'assigned operational area.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        geofence_status = "OUTSIDE"

        st.markdown(
            '<div class="critical-box">'
            '<h3>🚨 GEO-FENCE ALERT</h3>'
            '<p>'
            'Computer is currently outside the '
            'assigned operational area.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )


    st.caption(
        "● PHYSICAL LOCATION ACTIVE "
        "| Browser location permission granted"
    )


else:

    geofence_status = "UNKNOWN"

    st.warning(
        "📍 Click the location button above "
        "and allow browser location permission."
    )


st.divider()


# ============================================================
# TACTICAL STATUS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'TACTICAL STATUS'
    '</div>',
    unsafe_allow_html=True
)


# Determine health condition

if firebase_status in [
    "HEALTH ALERT",
    "CRITICAL"
]:

    health_abnormal = True

else:

    health_abnormal = False


# Determine final mission status

if not location_detected:

    status = firebase_status

elif (
    health_abnormal
    and
    geofence_status == "OUTSIDE"
):

    status = "CRITICAL"

elif health_abnormal:

    status = "HEALTH ALERT"

elif geofence_status == "OUTSIDE":

    status = "GEO-FENCE ALERT"

else:

    status = "NORMAL"


# Display tactical status

if status == "NORMAL":

    st.markdown(
        '<div class="normal-box">'
        '<h2>🟢 SYSTEM OPERATIONAL</h2>'
        '<p>'
        'All monitored parameters are within '
        'the configured limits.'
        '</p>'
        f'<small>'
        f'SOLDIER: {soldier_id}'
        ' &nbsp; | &nbsp; '
        'SYSTEM LINK: ACTIVE'
        ' &nbsp; | &nbsp; '
        'MONITORING: ENABLED'
        '</small>'
        '</div>',
        unsafe_allow_html=True
    )


elif status == "HEALTH ALERT":

    st.markdown(
        '<div class="warning-box">'
        '<h2>🟡 HEALTH ALERT</h2>'
        '<p>'
        'Abnormal health condition detected. '
        'Continuous monitoring required.'
        '</p>'
        f'<small>'
        f'SOLDIER: {soldier_id}'
        ' &nbsp; | &nbsp; '
        'SYSTEM LINK: ACTIVE'
        ' &nbsp; | &nbsp; '
        'MONITORING: ENABLED'
        '</small>'
        '</div>',
        unsafe_allow_html=True
    )


elif status == "GEO-FENCE ALERT":

    st.markdown(
        '<div class="warning-box">'
        '<h2>🟠 GEO-FENCE ALERT</h2>'
        '<p>'
        'Computer has moved outside the '
        'assigned operational zone.'
        '</p>'
        f'<small>'
        f'SOLDIER: {soldier_id}'
        ' &nbsp; | &nbsp; '
        'SYSTEM LINK: ACTIVE'
        ' &nbsp; | &nbsp; '
        'MONITORING: ENABLED'
        '</small>'
        '</div>',
        unsafe_allow_html=True
    )


elif status == "CRITICAL":

    st.markdown(
        '<div class="critical-box">'
        '<h2>🔴 CRITICAL EMERGENCY</h2>'
        '<p>'
        'Abnormal health condition combined '
        'with geo-fence violation.'
        '</p>'
        f'<small>'
        f'SOLDIER: {soldier_id}'
        ' &nbsp; | &nbsp; '
        'SYSTEM LINK: ACTIVE'
        ' &nbsp; | &nbsp; '
        'MONITORING: ENABLED'
        '</small>'
        '</div>',
        unsafe_allow_html=True
    )


else:

    st.markdown(
        '<div class="info-box">'
        '<h2>⚪ NO DATA</h2>'
        '<p>'
        'Unable to retrieve current soldier data.'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# HEALTH MONITORING
# ============================================================

st.markdown(
    '<div class="section-title">'
    '❤️ HEALTH MONITORING'
    '</div>',
    unsafe_allow_html=True
)


if health_abnormal:

    heart_status = "ABNORMAL"

    temperature_status = "ABNORMAL"

else:

    heart_status = "NORMAL"

    temperature_status = "NORMAL"


health_col1, health_col2 = st.columns(2)


# HEART RATE

with health_col1:

    if heart_status == "ABNORMAL":

        heart_color = "#ff8888"

        heart_message = (
            "🚨 HEART RATE ABNORMAL"
        )

    else:

        heart_color = "#8fd18f"

        heart_message = (
            "✓ HEART RATE NORMAL"
        )


    st.markdown(
        '<div class="tactical-card">'
        '<div class="card-title">'
        '❤️ HEART RATE'
        '</div>'
        f'<div class="card-value">'
        f'{heart_rate} BPM'
        '</div>'
        f'<div style="margin-top:15px;'
        f'color:{heart_color};'
        f'font-family:monospace;">'
        f'{heart_message}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# TEMPERATURE

with health_col2:

    if temperature_status == "ABNORMAL":

        temp_color = "#ff8888"

        temp_message = (
            "🚨 TEMPERATURE ABNORMAL"
        )

    else:

        temp_color = "#8fd18f"

        temp_message = (
            "✓ TEMPERATURE NORMAL"
        )


    st.markdown(
        '<div class="tactical-card">'
        '<div class="card-title">'
        '🌡 BODY TEMPERATURE'
        '</div>'
        f'<div class="card-value">'
        f'{temperature} °C'
        '</div>'
        f'<div style="margin-top:15px;'
        f'color:{temp_color};'
        f'font-family:monospace;">'
        f'{temp_message}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# AI HEALTH ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🤖 AI HEALTH ANALYSIS'
    '</div>',
    unsafe_allow_html=True
)


if status == "NORMAL":

    ai_prediction = "NORMAL"

    risk_level = "LOW RISK"


elif status == "HEALTH ALERT":

    ai_prediction = "ABNORMAL"

    risk_level = "ELEVATED RISK"


elif status == "CRITICAL":

    ai_prediction = "CRITICAL"

    risk_level = "CRITICAL RISK"


elif status == "GEO-FENCE ALERT":

    ai_prediction = "NORMAL"

    risk_level = "LOCATION RISK"


else:

    ai_prediction = "MONITOR"

    risk_level = "UNKNOWN"


ai_col1, ai_col2 = st.columns(2)


with ai_col1:

    st.markdown(
        '<div class="tactical-card">'
        '<div class="card-title">'
        'AI PREDICTION'
        '</div>'
        f'<div class="card-value">'
        f'{ai_prediction}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


with ai_col2:

    st.markdown(
        '<div class="tactical-card">'
        '<div class="card-title">'
        'HEALTH RISK LEVEL'
        '</div>'
        f'<div class="card-value">'
        f'{risk_level}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# SECURITY & COMMUNICATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔐 SECURITY & COMMUNICATION'
    '</div>',
    unsafe_allow_html=True
)


sec1, sec2, sec3 = st.columns(3)


# RFID

with sec1:

    st.markdown(
        '<div class="info-box">'
        '<h4>🔐 RFID AUTHENTICATION</h4>'
        f'Soldier: <b>{soldier_id}</b>'
        '<br><br>'
        'Authentication: '
        '<b>AUTHORIZED</b>'
        '<br><br>'
        'Helmet Status: '
        '<b>ACTIVE</b>'
        '</div>',
        unsafe_allow_html=True
    )


# GPS

with sec2:

    if location_detected:

        gps_latitude = (
            f"{display_latitude:.6f}"
        )

        gps_longitude = (
            f"{display_longitude:.6f}"
        )

        gps_status = "PHYSICAL LOCATION"

    else:

        gps_latitude = "NOT DETECTED"

        gps_longitude = "NOT DETECTED"

        gps_status = "WAITING"


    st.markdown(
        '<div class="info-box">'
        '<h4>📡 GPS / LOCATION TRACKING</h4>'
        f'Tracking: <b>{gps_status}</b>'
        '<br><br>'
        f'Latitude: <b>{gps_latitude}</b>'
        '<br><br>'
        f'Longitude: <b>{gps_longitude}</b>'
        '</div>',
        unsafe_allow_html=True
    )


# COMMUNICATION

with sec3:

    if firebase_data:

        firebase_state = "CONNECTED"

    else:

        firebase_state = "OFFLINE"


    st.markdown(
        '<div class="info-box">'
        '<h4>📶 COMMUNICATION LINK</h4>'
        f'Firebase: <b>{firebase_state}</b>'
        '<br><br>'
        'Data Link: <b>ACTIVE</b>'
        '<br><br>'
        'Monitoring: <b>ONLINE</b>'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# LOCATION INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🛰 LOCATION INFORMATION'
    '</div>',
    unsafe_allow_html=True
)


loc1, loc2, loc3 = st.columns(3)


with loc1:

    st.metric(
        "SAFE ZONE LATITUDE",
        f"{ZONE_LATITUDE:.6f}"
    )


with loc2:

    st.metric(
        "SAFE ZONE LONGITUDE",
        f"{ZONE_LONGITUDE:.6f}"
    )


with loc3:

    st.metric(
        "SAFE ZONE RADIUS",
        f"{ZONE_RADIUS} m"
    )


if location_detected:

    st.info(
        "The displayed coordinates are obtained "
        "from the computer/browser physical-location "
        "service. They are not simulated GPS coordinates."
    )

else:

    st.warning(
        "Physical location has not been detected yet."
    )


st.divider()


# ============================================================
# EVENT LOG
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📋 SYSTEM EVENT LOG'
    '</div>',
    unsafe_allow_html=True
)


current_time = datetime.now().strftime(
    "%H:%M:%S"
)


if status == "NORMAL":

    event_message = (
        "Soldier monitoring active. "
        "Health and location parameters normal."
    )


elif status == "HEALTH ALERT":

    event_message = (
        "Health alert detected. "
        "Command center monitoring required."
    )


elif status == "GEO-FENCE ALERT":

    event_message = (
        "Geo-fence boundary violation detected."
    )


elif status == "CRITICAL":

    event_message = (
        "CRITICAL condition detected. "
        "Health + location anomaly."
    )


else:

    event_message = (
        "Waiting for complete monitoring data."
    )


st.markdown(
    '<div class="info-box">'
    f'[{current_time}] &nbsp;&nbsp; '
    'SYSTEM &nbsp;&nbsp;→&nbsp;&nbsp; '
    f'{event_message}'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '🪖 AI-ENABLED SMART SOLDIER HELMET'
    ' &nbsp;|&nbsp; '
    'TACTICAL MONITORING SYSTEM'
    ' &nbsp;|&nbsp; '
    'SOFTWARE PROTOTYPE'
    '</div>',
    unsafe_allow_html=True
)
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
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=Share+Tech+Mono&display=swap');
:root{--army:#a6b85b;--bright:#c7d879;--line:#465637;--text:#e5eadc}
.stApp{background:radial-gradient(ellipse at 12% 0%,rgba(111,132,61,.18),transparent 34%),radial-gradient(ellipse at 90% 18%,rgba(67,86,42,.16),transparent 30%),linear-gradient(145deg,#090d08 0%,#11170f 48%,#080b07 100%);color:var(--text)}
.block-container{max-width:1600px;padding-top:1.7rem;padding-bottom:3rem}
[data-testid="stHeader"]{background:transparent}
p,label,.stMarkdown{color:var(--text)}
.command-header{position:relative;overflow:hidden;background:linear-gradient(110deg,rgba(35,47,27,.98),rgba(14,20,13,.98));border:1px solid #596d3b;border-left:7px solid var(--army);border-radius:5px;padding:27px 32px;margin-bottom:26px;box-shadow:0 12px 35px rgba(0,0,0,.38),inset 0 0 35px rgba(142,164,75,.05)}
.command-header:after{content:"FIELD OPERATIONS  /  SECURE NETWORK";position:absolute;right:24px;bottom:17px;color:rgba(199,216,121,.42);font:11px 'Share Tech Mono',monospace;letter-spacing:2px}
.command-title{font-family:'Barlow Condensed',sans-serif;font-size:clamp(30px,4vw,46px);font-weight:900;color:var(--bright);letter-spacing:3px;text-transform:uppercase;text-shadow:0 0 18px rgba(166,184,91,.2)}
.command-subtitle{font-family:'Share Tech Mono',monospace;font-size:12px;color:#c0c9ad;letter-spacing:2px;margin-top:5px}
.command-status{font-family:'Share Tech Mono',monospace;font-size:11px;color:#a9c777;letter-spacing:1.5px;margin-top:16px}
.section-title{font-family:'Barlow Condensed',sans-serif;font-size:21px;font-weight:800;color:var(--bright);letter-spacing:2px;text-transform:uppercase;border-left:4px solid var(--army);padding:3px 0 3px 12px;margin:14px 0 17px}
[data-testid="stMetric"]{background:linear-gradient(145deg,#20291b,#141b12);border:1px solid var(--line);border-top:2px solid #71864a;border-radius:5px;padding:17px 18px;min-height:112px;box-shadow:0 7px 20px rgba(0,0,0,.24)}
[data-testid="stMetricLabel"]{color:#aab69a!important;font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase}
[data-testid="stMetricValue"]{color:#e4edcf!important;font-family:'Barlow Condensed',sans-serif;font-weight:800;letter-spacing:.5px}
.normal-box,.warning-box,.critical-box,.info-box{border-radius:5px;padding:20px 22px;font-family:'Share Tech Mono',monospace;box-shadow:0 8px 22px rgba(0,0,0,.22)}
.normal-box{background:linear-gradient(100deg,#14251a,#101a13);border:1px solid #4c8051;border-left:5px solid #79b66d;color:#b9e2ad}
.warning-box{background:linear-gradient(100deg,#2b2713,#1b1a10);border:1px solid #927b3c;border-left:5px solid #d4b64f;color:#eadb91}
.critical-box{background:linear-gradient(100deg,#301616,#1d1010);border:1px solid #9b4545;border-left:5px solid #e15e52;color:#ffb1a9}
.info-box{background:linear-gradient(145deg,#20291f,#141b15);border:1px solid #465844;border-left:4px solid #71864a;color:#c0cbb9;min-height:150px}
.tactical-card{background:linear-gradient(145deg,rgba(34,44,29,.98),rgba(17,23,15,.98));border:1px solid #4b5c39;border-top:2px solid #71864a;border-radius:5px;padding:22px;min-height:138px;box-shadow:0 8px 22px rgba(0,0,0,.25)}
.card-title{font-family:'Share Tech Mono',monospace;color:#aab798;font-size:11px;letter-spacing:2px}
.card-value{font-family:'Barlow Condensed',sans-serif;color:var(--bright);font-size:31px;font-weight:800;letter-spacing:1px;margin-top:11px}
.footer{text-align:center;color:#82906e;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:1.5px;margin-top:36px;padding:20px;border-top:1px solid #35432c}
hr{border-color:#34422b!important}
[data-testid="stMap"]{border:1px solid #566a3c;border-radius:5px;overflow:hidden}
.stButton>button{background:#45572e;color:#f0f4e4;border:1px solid #829653;border-radius:3px;font-family:'Share Tech Mono',monospace;letter-spacing:1px}
.stButton>button:hover{background:#62783d;color:white;border-color:#c0d17a}
.stAlert{border-radius:4px;border:1px solid #687b48}
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
    'AI-ENABLED SOLDIER SAFETY  |  TACTICAL COMMAND DASHBOARD'
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
    ' AI-ENABLED SMART SOLDIER HELMET'
    ' &nbsp;|&nbsp; '
    'TACTICAL MONITORING SYSTEM'
    ' &nbsp;|&nbsp; '
    'SOFTWARE PROTOTYPE'
    '</div>',
    unsafe_allow_html=True
)
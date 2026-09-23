import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.title("Computer Live Location")

location = streamlit_geolocation()

st.write(location)

if location and location.get("latitude") is not None:

    st.success("Location detected!")

    st.write(
        "Latitude:",
        location["latitude"]
    )

    st.write(
        "Longitude:",
        location["longitude"]
    )

    st.write(
        "Accuracy:",
        location.get("accuracy"),
        "meters"
    )

else:

    st.warning(
        "Click the location button and allow browser location permission."
    )
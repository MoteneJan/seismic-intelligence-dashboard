import streamlit as st
from data_fetch import fetch_earthquake_data
from analysis import classify_event
import folium
from streamlit.components.v1 import html

st.set_page_config(page_title="Seismic Intelligence Dashboard", layout="wide")

# ---------------------------
# HEADER
# ---------------------------
st.title("🌍 Seismic Intelligence Dashboard")
st.markdown("Monitor and analyze seismic events for risk assessment")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("🔎 Filters")

min_magnitude = st.sidebar.slider("Minimum Magnitude", 1.0, 5.0, 2.0)
radius_km = st.sidebar.slider("Search Radius (km)", 10, 200, 50)

# ---------------------------
# FETCH DATA
# ---------------------------
data = fetch_earthquake_data()

if not data:
    st.error("❌ Failed to retrieve seismic data.")
    st.stop()

features = data.get("features", [])

if not features:
    st.warning("No events found.")
    st.stop()

# ---------------------------
# MAP
# ---------------------------
st.subheader("📍 Event Map")

m = folium.Map(location=[34.669, 28.909], zoom_start=6)

events_displayed = 0

for event in features:
    mag = event["properties"]["mag"]
    
    if mag < min_magnitude:
        continue

    coords = event["geometry"]["coordinates"]
    lon, lat, depth = coords

    classification, score = classify_event(mag, depth)

    color = "green" if classification == "Natural" else "red"

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        popup=f"Magnitude: {mag}<br>Depth: {depth} km<br>{classification}",
        color=color,
        fill=True
    ).add_to(m)

    events_displayed += 1

html(m._repr_html_(), height=500)

st.write(f"Showing {events_displayed} events")

# ---------------------------
# EVENT ANALYSIS PANEL
# ---------------------------
st.subheader("📊 Event Analysis")

event = features[0]
coords = event["geometry"]["coordinates"]
lon, lat, depth = coords
mag = event["properties"]["mag"]

classification, score = classify_event(mag, depth)

col1, col2, col3 = st.columns(3)

col1.metric("Magnitude", mag)
col2.metric("Depth (km)", depth)
col3.metric("Confidence Score", score)

st.markdown(f"### Classification: **{classification}**")

# ---------------------------
# RAW DATA (TRANSPARENCY)
# ---------------------------
with st.expander("🔍 View Raw Data"):
    st.json(event)

# ---------------------------
# ANALYST NOTES (🔥 UNIQUE FEATURE)
# ---------------------------
st.subheader("🧠 Analyst Notes")

notes = st.text_area("Write your assessment notes here...")

if st.button("Save Notes"):
    with open("notes.txt", "w") as f:
        f.write(notes)
    st.success("Notes saved!")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("Data sourced from USGS | Built for Intelligence Analysis Assessment")
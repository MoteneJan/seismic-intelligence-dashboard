import folium

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=6)
    
    folium.Marker(
        [lat, lon],
        popup="Seismic Event",
        tooltip="M2.5 Event"
    ).add_to(m)

    return m
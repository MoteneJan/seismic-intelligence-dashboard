import requests

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    params = {
        "format": "geojson",
        "starttime": "2026-03-06",
        "endtime": "2026-03-07",
        "latitude": 34.669,
        "longitude": 28.909,
        "maxradiuskm": 50,
        "minmagnitude": 2
    }

    response = requests.get(url, params=params)
    return response.json()
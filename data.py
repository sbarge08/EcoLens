import requests
import streamlit as st


# ============================================================
# LOCATION DATABASE
# ============================================================

LOCATIONS = {
    "Newark, NJ": {
        "latitude": 40.7357,
        "longitude": -74.1724,
    },

    "New York, NY": {
        "latitude": 40.7128,
        "longitude": -74.0060,
    },

    "Chicago, IL": {
        "latitude": 41.8781,
        "longitude": -87.6298,
    },

    "Los Angeles, CA": {
        "latitude": 34.0522,
        "longitude": -118.2437,
    },

    "Phoenix, AZ": {
        "latitude": 33.4484,
        "longitude": -112.0740,
    },

    "Miami, FL": {
        "latitude": 25.7617,
        "longitude": -80.1918,
    },

    "Denver, CO": {
        "latitude": 39.7392,
        "longitude": -104.9903,
    },
}


# ============================================================
# WEATHER DATA
# ============================================================

@st.cache_data(ttl=1800)
def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum"
        ),

        "forecast_days": 7,
        "timezone": "auto",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# AIR QUALITY DATA
# ============================================================

@st.cache_data(ttl=1800)
def get_air_quality(latitude, longitude):

    url = (
        "https://air-quality-api.open-meteo.com/"
        "v1/air-quality"
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "us_aqi,"
            "pm2_5,"
            "pm10"
        ),

        "timezone": "auto",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# ENVIRONMENTAL PROFILE
# ============================================================

@st.cache_data(ttl=1800)
def get_environmental_profile(location_name):

    # --------------------------------------------------------
    # Validate location
    # --------------------------------------------------------

    if location_name not in LOCATIONS:

        raise ValueError(
            f"Unsupported location: {location_name}"
        )

    coordinates = LOCATIONS[
        location_name
    ]

    latitude = coordinates[
        "latitude"
    ]

    longitude = coordinates[
        "longitude"
    ]

    # --------------------------------------------------------
    # Retrieve live data
    # --------------------------------------------------------

    try:

        weather = get_weather(
            latitude,
            longitude,
        )

        air_quality = get_air_quality(
            latitude,
            longitude,
        )

        return {
            "location": location_name,

            "latitude": latitude,

            "longitude": longitude,

            "weather": weather,

            "air_quality": air_quality,

            "data_status": "live",
        }

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    except Exception:

        return {
            "location": location_name,

            "latitude": latitude,

            "longitude": longitude,

            "weather": {
                "current": {
                    "temperature_2m": 28.0,
                    "relative_humidity_2m": 55.0,
                    "precipitation": 0.0,
                },

                "daily": {
                    "time": [
                        "Day 1",
                        "Day 2",
                        "Day 3",
                        "Day 4",
                        "Day 5",
                        "Day 6",
                        "Day 7",
                    ],

                    "temperature_2m_max": [
                        28,
                        29,
                        30,
                        30,
                        29,
                        28,
                        29,
                    ],

                    "temperature_2m_min": [
                        20,
                        21,
                        21,
                        22,
                        21,
                        20,
                        20,
                    ],

                    "precipitation_sum": [
                        0,
                        1,
                        0,
                        2,
                        1,
                        0,
                        1,
                    ],
                },
            },

            "air_quality": {
                "current": {
                    "us_aqi": 60,
                    "pm2_5": 15.0,
                    "pm10": 25.0,
                }
            },

            "data_status": "fallback",
        }
import requests
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

from config.settings import API_TOKEN, BASE_URL, STATIONS

def get_stations() -> dict:
    """Returns the hardcoded list of US city weather stations from the NOAA API.
    """
    return {s["name"]: s["id"] for s in STATIONS}


def get_weather_data(station_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """Fetches daily summary weather data (TMAX, TMIN) for a station."""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        bare_station_id = station_id.split(':')[-1] if ':' in station_id else station_id
        params = {
            "dataset": "daily-summaries",
            "stations": bare_station_id,
            "startDate": start_date,
            "endDate": end_date,
            "dataTypes": "TMAX,TMIN",
            "units": "metric",
            "format": "json",
            "includeAttributes": "false",
            "token": API_TOKEN
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict) and 'results' in data:
            return pd.DataFrame(data['results'])
        else:
            return pd.DataFrame() # Return empty DataFrame for unexpected format or empty data

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error fetching weather data: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error fetching weather data: {e}")
        return pd.DataFrame()
    except ValueError as e: # JSONDecodeError
        st.error(f"JSON Decode Error fetching weather data: {e}")
        return pd.DataFrame()
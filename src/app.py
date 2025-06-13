from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from api.weather_api import get_stations, get_weather_data
from utils.data_processing import process_weather_data
from visualization.plots import display_weather_plot


def main():
    """Main application function."""
    st.title("US Weather Forecaster")
    st.write("## *Weather data provided by NOAA* 🌤️")
    st.write("##")
    st.write("### Select a weather station and your preferences:")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start date", value=datetime(2025, 5, 1).date())
    with col2:
        end_date = st.date_input("End date", value=date.today())

    aggregation_options = ['monthly', 'yearly']
    if start_date and end_date and (end_date - start_date <= timedelta(days=31)):
        aggregation_options.insert(0, 'daily')

    current_selection = st.session_state.get('aggregation_period', 'monthly')
    default_aggregation_index = 0
    if current_selection in aggregation_options:
        default_aggregation_index = aggregation_options.index(current_selection)
    elif 'monthly' in aggregation_options:
        default_aggregation_index = aggregation_options.index('monthly')

    with col3:
        aggregation_period = st.selectbox(
            "Aggregation:",
            options=aggregation_options,
            index=default_aggregation_index,
            key='aggregation_period'
        )

    graph_type = st.selectbox("Select Graph Type:", ('Bar Graph', 'Line Graph'))

    stations = get_stations()
    if not stations:
        st.error("Unable to fetch weather stations. Please check your API token.")
        return

    station_names = list(stations.keys())
    selected_station_name = st.selectbox("Select Weather Station:", station_names)
    selected_station_id = stations[selected_station_name]

    if st.button('Get Weather'):
        try:
            raw_data = get_weather_data(
                selected_station_id,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )

            if raw_data is not None and not raw_data.empty:
                avg_temps = process_weather_data(
                    raw_data,
                    start_date_obj=pd.to_datetime(start_date),
                    end_date_obj=pd.to_datetime(end_date),
                    aggregation=aggregation_period
                )
                if avg_temps is not None and not avg_temps.empty:
                    display_weather_plot(
                        avg_temps,
                        graph_type,
                        aggregation_period,
                        user_start_date=pd.to_datetime(start_date),
                        user_end_date=pd.to_datetime(end_date),
                        station_name=selected_station_name
                    )
                elif avg_temps is None:
                    st.warning("Failed to process weather data.")
                else:
                    st.info("No data available to display for the selected criteria after processing.")
            elif raw_data is None:
                st.error("Failed to fetch weather data. The API might have returned no data or an error.")
            else:
                st.info("No raw weather data found for the selected station and date range.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("If this error persists, please try selecting a different weather station.")


if __name__ == '__main__':
    main()

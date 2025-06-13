import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def display_weather_plot(data: pd.Series, plot_type: str = 'Bar Graph', aggregation_period: str = 'monthly',
                         user_start_date: pd.Timestamp = None, user_end_date: pd.Timestamp = None, 
                         station_name: str = None):
    """Displays weather data plot, showing gaps for missing daily data."""

    if not isinstance(data, pd.Series) or data.empty:
        return

    plt.figure(figsize=(10, 5))

    plot_data_series = data.copy()

    if aggregation_period == 'daily' and user_start_date and user_end_date:
        all_dates_pd = pd.date_range(start=user_start_date, end=user_end_date, freq='D')
        if not isinstance(plot_data_series.index, pd.DatetimeIndex):
            try:
                plot_data_series.index = pd.to_datetime(plot_data_series.index)
            except Exception as e:
                st.error(f"Error converting plot index to datetime: {e}")
                return
        plot_data_series = plot_data_series.reindex(all_dates_pd)

    if plot_type == 'Bar Graph':
        x_plot_index = plot_data_series.index
        if isinstance(plot_data_series.index, pd.PeriodIndex):
            x_plot_index = plot_data_series.index.astype(str)
        plt.bar(x_plot_index, plot_data_series.values, color='skyblue', width=0.9)
    else:  # Line Graph        
        current_index_for_plot = plot_data_series.index
        if isinstance(current_index_for_plot, pd.PeriodIndex):
            current_index_for_plot = current_index_for_plot.to_timestamp()
        plt.plot(current_index_for_plot, plot_data_series.values, marker='o', linestyle='-', color='skyblue', linewidth=2)

    title_prefix = aggregation_period.capitalize()
    station_info = f" - {station_name}" if station_name else ""
    plt.title(f'{title_prefix} Average Temperatures{station_info}')
    plt.ylabel('Temperature (°C)')

    if aggregation_period == 'daily' and user_start_date and user_end_date:
        adjusted_start_limit = user_start_date - pd.Timedelta(days=0.5)
        adjusted_end_limit = user_end_date + pd.Timedelta(days=0.5)
        adjusted_start_limit = user_start_date - pd.Timedelta(days=0.5)
        adjusted_end_limit = user_end_date + pd.Timedelta(days=0.5)
        plt.xlim(left=adjusted_start_limit, right=adjusted_end_limit)
 

        plt.xticks(ticks=all_dates_pd, rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')

    plt.margins(x=0.05)
    plt.grid(False, linestyle='--', alpha=0.2)
    plt.tight_layout()

    if plot_data_series.name:
        plt.legend()

    st.pyplot(plt.gcf())
    plt.close(plt.gcf())
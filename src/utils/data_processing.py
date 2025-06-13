import pandas as pd
import streamlit as st

def process_weather_data(raw_data: pd.DataFrame, start_date_obj: pd.Timestamp, end_date_obj: pd.Timestamp, aggregation: str = 'monthly') -> pd.Series:
    """Processes raw weather DataFrame into aggregated average temperatures."""

    if raw_data.empty:
        st.warning("No raw data to process.")
        return pd.Series(dtype=float)

    if 'DATE' not in raw_data.columns:
        st.error("'DATE' column missing in raw data.")
        return pd.Series(dtype=float)

    df = raw_data.copy()
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df.dropna(subset=['DATE'], inplace=True)

    df = df[(df['DATE'] >= start_date_obj) & (df['DATE'] <= end_date_obj)]

    if df.empty:
        st.warning("No data available for the selected date range after filtering.")
        return pd.Series(dtype=float)

    df["TMAX"] = pd.to_numeric(df["TMAX"], errors='coerce')
    df["TMIN"] = pd.to_numeric(df["TMIN"], errors='coerce')
    df["TAVG"] = (df["TMAX"] + df["TMIN"]) / 2

    df.dropna(subset=['TAVG'], inplace=True)

    if df.empty:
        st.warning("No valid temperature data available for aggregation.")
        return pd.Series(dtype=float)

    if aggregation == 'daily':
        avg_temp = df.set_index('DATE').resample('D')['TAVG'].mean().round(1)
        all_days = pd.date_range(start=start_date_obj, end=end_date_obj, freq='D')
        avg_temp = avg_temp.reindex(all_days, fill_value=pd.NA)
    elif aggregation == 'monthly':
        avg_temp = df.set_index('DATE').resample('M')['TAVG'].mean().round(1)
        avg_temp.index = avg_temp.index.to_period('M')
    elif aggregation == 'yearly':
        avg_temp = df.set_index('DATE').resample('Y')['TAVG'].mean().round(1)
        avg_temp.index = avg_temp.index.to_period('Y')
    else:
        st.error(f"Invalid aggregation period: {aggregation}")
        return pd.Series(dtype=float)
    return avg_temp
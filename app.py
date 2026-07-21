import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# Auto Refresh (60 Seconds)
# ==========================
st_autorefresh(interval=60000, key="refresh")

# ==========================
# Dashboard Title
# ==========================
st.title("🌦 Real-Time Weather Dashboard")

# ==========================
# Sidebar
# ==========================
st.sidebar.header("Dashboard Settings")

city = st.sidebar.selectbox(
    "Select City",
    ["Ahmedabad", "Delhi", "Mumbai", "Bengaluru"]
)

alert_temp = st.sidebar.slider(
    "Temperature Alert (°C)",
    min_value=20,
    max_value=50,
    value=35
)

# ==========================
# City Coordinates
# ==========================
cities = {
    "Ahmedabad": (23.03, 72.58),
    "Delhi": (28.61, 77.20),
    "Mumbai": (19.07, 72.87),
    "Bengaluru": (12.97, 77.59)
}

latitude, longitude = cities[city]

# ==========================
# API Request
# ==========================
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    "&hourly=temperature_2m"
)

response = requests.get(url)

if response.status_code == 200:

    data = response.json()
    current = data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    time = current["time"]

    # ==========================
    # Current Weather Table
    # ==========================
    current_df = pd.DataFrame({
        "City": [city],
        "Time": [time],
        "Temperature (°C)": [temperature],
        "Humidity (%)": [humidity],
        "Wind Speed (km/h)": [wind]
    })

    st.subheader("Current Weather")
    st.dataframe(current_df)

    # ==========================
    # Metrics
    # ==========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌡 Temperature", f"{temperature} °C")

    with col2:
        st.metric("💧 Humidity", f"{humidity}%")

    with col3:
        st.metric("💨 Wind Speed", f"{wind} km/h")

    # ==========================
    # Alert
    # ==========================
    if temperature > alert_temp:
        st.error(f"⚠ Temperature crossed {alert_temp}°C")
    else:
        st.success("✅ Temperature is Normal")

    # ==========================
    # 24-Hour Forecast
    # ==========================
    hours = data["hourly"]["time"][:24]
    temperatures = data["hourly"]["temperature_2m"][:24]

    forecast_df = pd.DataFrame({
        "Time": hours,
        "Temperature (°C)": temperatures
    })

    st.subheader("📈 24-Hour Temperature Forecast")
    st.line_chart(forecast_df.set_index("Time"))

    # ==========================
    # Last Updated
    # ==========================
    st.write(
        "🕒 Last Updated:",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    # ==========================
    # Download Button
    # ==========================
    st.download_button(
        label="📥 Download Current Weather",
        data=current_df.to_csv(index=False),
        file_name="current_weather.csv",
        mime="text/csv"
    )

else:
    st.error("Unable to fetch weather data. Please try again later.")
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =====================================
# Page Configuration
# =====================================
st.set_page_config(page_title="Real-Time Weather Dashboard", layout="wide")

# Auto Refresh every 60 seconds
st_autorefresh(interval=60000, key="refresh")

st.title("🌦 Real-Time Weather Dashboard")

# =====================================
# Sidebar
# =====================================
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

# =====================================
# City Coordinates
# =====================================
cities = {
    "Ahmedabad": (23.03, 72.58),
    "Delhi": (28.61, 77.20),
    "Mumbai": (19.07, 72.87),
    "Bengaluru": (12.97, 77.59)
}

latitude, longitude = cities[city]

# =====================================
# API URL
# =====================================
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    "&hourly=temperature_2m"
)

# =====================================
# Fetch Live Data
# =====================================
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    weather_time = current["time"]

    # =====================================
    # Current Weather Table
    # =====================================
    current_df = pd.DataFrame({
        "City": [city],
        "Time": [weather_time],
        "Temperature (°C)": [temperature],
        "Humidity (%)": [humidity],
        "Wind Speed (km/h)": [wind]
    })

    st.subheader("Current Weather")
    st.dataframe(current_df, use_container_width=True)

    # =====================================
    # KPI Metrics
    # =====================================
    col1, col2, col3 = st.columns(3)

    col1.metric("🌡 Temperature", f"{temperature} °C")
    col2.metric("💧 Humidity", f"{humidity}%")
    col3.metric("💨 Wind Speed", f"{wind} km/h")

    # =====================================
    # Temperature Alert
    # =====================================
    if temperature >= alert_temp:
        st.error(f"⚠ Temperature crossed {alert_temp}°C")
    else:
        st.success("✅ Temperature is Normal")

    # =====================================
    # Forecast Chart
    # =====================================
    forecast_df = pd.DataFrame({
        "Time": data["hourly"]["time"][:24],
        "Temperature (°C)": data["hourly"]["temperature_2m"][:24]
    })

    st.subheader("📈 24-Hour Temperature Forecast")
    st.line_chart(
        forecast_df.set_index("Time"),
        use_container_width=True
    )

    # =====================================
    # Last Updated
    # =====================================
    st.write(
        "🕒 Last Updated:",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    # =====================================
    # Download CSV
    # =====================================
    st.download_button(
        "📥 Download Current Weather",
        current_df.to_csv(index=False),
        file_name="current_weather.csv",
        mime="text/csv"
    )

except requests.exceptions.RequestException as e:
    st.error("Unable to fetch weather data.")
    st.exception(e)

except Exception as e:
    st.error("An unexpected error occurred.")
    st.exception(e)

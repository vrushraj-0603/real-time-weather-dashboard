import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌦",
    layout="wide"
)

# Auto Refresh Every 5 Minutes
st_autorefresh(interval=300000, key="refresh")

st.title("🌦 Real-Time Weather Dashboard")
st.write("Live Weather Data using Open-Meteo API (No API Key Required)")

# =====================================
# City Coordinates
# =====================================
cities = {
    "Ahmedabad": (23.0225, 72.5714),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946)
}

# =====================================
# Sidebar
# =====================================
st.sidebar.header("Dashboard Settings")

city = st.sidebar.selectbox("Select City", list(cities.keys()))

alert_temp = st.sidebar.slider(
    "Temperature Alert (°C)",
    20,
    50,
    35
)

latitude, longitude = cities[city]

# =====================================
# Fetch Weather Data
# =====================================
@st.cache_data(ttl=300)
def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()

# =====================================
# Main Dashboard
# =====================================
try:
    data = get_weather(latitude, longitude)

    current = data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]

    weather_df = pd.DataFrame({
        "City": [city],
        "Temperature (°C)": [temperature],
        "Humidity (%)": [humidity],
        "Wind Speed (km/h)": [wind],
        "Last Updated": [datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    })

    st.subheader("📋 Current Weather")
    st.dataframe(weather_df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡 Temperature", f"{temperature} °C")
    col2.metric("💧 Humidity", f"{humidity}%")
    col3.metric("💨 Wind Speed", f"{wind} km/h")

    if temperature >= alert_temp:
        st.error(f"⚠ High Temperature Alert! ({temperature}°C)")
    else:
        st.success("✅ Temperature is Normal")

    st.subheader("📊 Weather Overview")

    chart_df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "Wind Speed"],
        "Value": [temperature, humidity, wind]
    })

    st.bar_chart(chart_df.set_index("Metric"))

    st.write(
        "🕒 Last Updated:",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    csv = weather_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Weather Report",
        data=csv,
        file_name="weather_report.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Error: {e}")

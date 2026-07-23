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
    layout="wide"
)

# Auto Refresh every 5 minutes
st_autorefresh(interval=300000, key="refresh")

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
# Cache API Data (5 Minutes)
# =====================================
@st.cache_data(ttl=300)
def get_weather_data(api_url):
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()

# =====================================
# Fetch Data
# =====================================
try:
    data = get_weather_data(url)

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
    # Download Button
    # =====================================
    st.download_button(
        label="📥 Download Current Weather",
        data=current_df.to_csv(index=False),
        file_name="current_weather.csv",
        mime="text/csv"
    )

except requests.exceptions.HTTPError as e:
    if e.response is not None and e.response.status_code == 429:
        st.warning("⚠ API request limit reached. Please wait a few minutes and try again.")
    else:
        st.error(f"HTTP Error: {e}")

except requests.exceptions.RequestException as e:
    st.error(f"Network Error: {e}")

except Exception as e:
    st.error(f"Unexpected Error: {e}")

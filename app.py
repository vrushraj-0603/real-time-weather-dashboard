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
st_autorefresh(interval=300000, key="weather_refresh")

st.title("🌦 Real-Time Weather Dashboard")
st.write("Live Weather Data using OpenWeatherMap API")

# =====================================
# API Key
# =====================================
API_KEY = "82040fe90c09f4f6a13abe09cedd5f32"   # Replace with your active API key

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
# Fetch Weather Data
# =====================================
@st.cache_data(ttl=300)
def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid=82040fe90c09f4f6a13abe09cedd5f32&units=metric"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()

# =====================================
# Main Dashboard
# =====================================
try:
    data = get_weather(city)

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    pressure = data["main"]["pressure"]
    condition = data["weather"][0]["description"].title()

    current_df = pd.DataFrame({
        "City": [city],
        "Temperature (°C)": [temperature],
        "Humidity (%)": [humidity],
        "Wind Speed (m/s)": [wind],
        "Pressure (hPa)": [pressure],
        "Condition": [condition],
        "Timestamp": [datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    })

    st.subheader("📋 Current Weather")
    st.dataframe(current_df, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡 Temperature", f"{temperature:.1f} °C")
    col2.metric("💧 Humidity", f"{humidity}%")
    col3.metric("💨 Wind Speed", f"{wind} m/s")
    col4.metric("🌤 Condition", condition)

    if temperature >= alert_temp:
        st.error(f"⚠ High Temperature Alert! ({temperature:.1f} °C)")
    else:
        st.success("✅ Temperature is Normal")

    st.subheader("📊 Weather Overview")

    chart_df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "Wind Speed", "Pressure"],
        "Value": [temperature, humidity, wind, pressure]
    })

    st.bar_chart(chart_df.set_index("Metric"))

    st.write(
        "🕒 Last Updated:",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    csv = current_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Weather Report",
        data=csv,
        file_name="weather_report.csv",
        mime="text/csv"
    )

except requests.exceptions.HTTPError as e:
    st.error(f"HTTP Error: {e}")

except requests.exceptions.RequestException as e:
    st.error(f"Network Error: {e}")

except Exception as e:
    st.error(f"Unexpected Error: {e}")

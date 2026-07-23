# Real-Time Weather Dashboard

## Overview

The **Real-Time Weather Dashboard** is a web application developed using **Python**, **Streamlit**, and the **Open-Meteo API**. It provides live weather information for multiple cities, including **Temperature**, **Humidity**, and **Wind Speed**. The dashboard features automatic data refresh, weather visualization, temperature alerts, and CSV report downloads.

---

## Objectives

- Fetch real-time weather data using the Open-Meteo API.
- Display live weather metrics for multiple cities.
- Visualize weather information using interactive charts.
- Provide temperature alerts based on user-defined thresholds.
- Allow users to download weather reports as CSV files.
- Build and deploy an interactive Streamlit dashboard.

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Requests
- Open-Meteo API

---

## Dataset

This project uses **live weather data** fetched directly from the **Open-Meteo API**.

Weather information includes:

- City
- Temperature (°C)
- Humidity (%)
- Wind Speed (km/h)
- Last Updated Time

---

## Project Workflow

1. Import the required Python libraries.
2. Select a city from the sidebar.
3. Fetch live weather data using the Open-Meteo API.
4. Process the JSON response.
5. Display current weather metrics.
6. Generate temperature alerts.
7. Visualize weather data using a bar chart.
8. Allow users to download the weather report as a CSV file.
9. Automatically refresh data every 5 minutes.

---

## Live Demo

**Streamlit Application**

https://real-time-weather-dashboard-4zeertj3mneqfqw3lapaqj.streamlit.app/

---

## Project Files

```text
README.md
app.py
requirements.txt
Dashboard_Screenshot.png
```

---

## Dashboard Features

- Multiple City Selection
- Live Temperature
- Live Humidity
- Live Wind Speed
- Weather Metrics Cards
- Temperature Alert System
- Weather Overview Bar Chart
- CSV Report Download
- Automatic Refresh (Every 5 Minutes)
- Last Updated Timestamp

---

## Dashboard Insights

- Displays real-time weather conditions.
- Allows comparison of weather across different cities.
- Generates alerts when the temperature exceeds the selected threshold.
- Provides downloadable weather reports for further analysis.
- Automatically refreshes to ensure up-to-date information.

---

## Requirements

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## Project Outcome

This project demonstrates how real-time data can be collected, processed, and visualized using Python and Streamlit. It showcases API integration, dashboard development, and interactive data visualization for monitoring live weather conditions.

---

## Author

**Vrushraj**

**Data Analytics Internship Project**

# WeatherProject
# 🌤️ Ibadan, Nigeria Weather Forecast Dashboard

![Weather Dashboard](https://learndataengineering.hashnode.dev/)

## 📖 Project Overview

This project provides a **Weather Forecast Dashboard** for **Ibadan, Nigeria**, showing real-time weather conditions and a 5-day forecast using interactive visualizations. The dashboard is built with **Streamlit** for easy web deployment and **Plotly** for interactive charts, allowing users to explore weather trends like temperature, humidity, wind speed, and more.

## 🛠 Features

- **Live Weather Updates**: Displays the current weather, including temperature, humidity, wind speed, and more.
- **5-Day Forecast**: Shows predicted weather patterns over the next five days.
- **Interactive Charts**: Visualizations using Plotly to showcase trends in temperature, precipitation, wind speed, and other metrics.
- **Geospatial Data**: Map showing the location of Ibadan, Nigeria, with latitude and longitude information.
- **Responsive Dashboard**: Optimized for both desktop and mobile viewing.
- **Icons and Visual Enhancements**: Weather-related icons and colour themes for better user experience.

## 🚀 Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Charts**: [Plotly](https://plotly.com/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [PySpark](https://spark.apache.org/)
- **API Integration**: [OpenWeatherMap API](https://openweathermap.org/)
- **API Integration**: [MapBOX API](https://mapbox.com/)

## ⚙️ Setup Instructions

### Prerequisites
- **Python 3.7+**
- **Virtual Environment**: (Recommended) [virtualenv](https://virtualenv.pypa.io/en/stable/)
- **Streamlit**: Install Streamlit for the web interface
- **Plotly**: Install Plotly for charting

📊 Visualizations Included

	•	Temperature Trends: Line chart showing temperature changes over time.
	•	Humidity vs. Temperature: Scatter plot to show the correlation between humidity and temperature.
	•	Precipitation Probability: Bar chart showing the chance of precipitation for the next five days.
	•	Wind Speed and Pressure: Bar and line chart to visualize wind speed and atmospheric pressure.
	•	Temperature Range: Area chart showing the range of daily minimum and maximum temperatures.
	•	Weather Heatmap: Heatmap visualizing correlations between weather metrics like temperature, humidity, and wind speed.

## 📁 Project Structure

```

├── data
│   └── transformed_weather_data.csv
├── weather_app.py                # Main Streamlit app file
├── requirements.txt              # Python dependencies
├── .env                          # API key configuration (not included in the repo)
└── README.md
```

🙌 Acknowledgments

	•	OpenWeatherMap and MapBOX for providing weather data and Map.
	•	Streamlit and Plotly for easy data visualization and interactivity.

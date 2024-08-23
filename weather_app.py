# weather_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import plotly.figure_factory as ff
import numpy as np
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Load the processed weather data
df_daily = pd.read_csv('transformed_weather_data.csv', parse_dates=['forecast_time'])

# Set the latitude and longitude of Ibadan, Nigeria
ibadan_lat = 7.3775
ibadan_lon = 3.9470

# Filter the data to get the current day's forecast
today = datetime.today().date()  # Get the current date
df_today = df_daily[df_daily['forecast_time'].dt.date == today]

# Format today's date as "22 AUG 2024" (sample look)
formatted_today = today.strftime("%d %b %Y").upper()

# Set page title and description
st.set_page_config(page_title="Ibadan Weather Dashboard", layout="wide")

# Create a centered title with a sunny yellow color
st.markdown(
    """
    <h1 style="text-align: center; color: #FFD700;">Ibadan, Nigeria Weather Forecast Dashboard</h1>
    """,
    unsafe_allow_html=True
)

# If there's no data for today, display a message
if df_today.empty:
    st.error("No weather data available for today.")
else:
    st.markdown(
    f"""
    <h3 style="color: #2ca02c;">Weather Overview for {formatted_today}</h3>
    """, 
    unsafe_allow_html=True
)
    #st.write(f"### Weather Overview for {formatted_today}")
    
    # Set up a four-column layout for today's key weather metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        max_temp = df_today['temperature'].max()
        st.metric(label="🌡️ Max Temperature", value=f"{max_temp:.2f}°C")
    
    with col2:
        min_temp = df_today['temperature'].min()
        st.metric(label="🌡️ Min Temperature", value=f"{min_temp:.2f}°C")
    
    with col3:
        total_precip = df_today['precipitation_probability'].sum()
        st.metric(label="🌧️ Total Precipitation", value=f"{total_precip:.2f} mm")
    
    with col4:
        max_wind = df_today['wind_speed'].max()
        st.metric(label="🌬️ Max Wind Speed", value=f"{max_wind:.2f} m/s")
    
    with col5:
        # Convert 'sunrise' to datetime and format it to 12-hour time (AM/PM)
        sunrise_time = pd.to_datetime(df_today['sunrise'].values[0]).strftime('%I:%M %p')
        st.metric(label="🌅 Sunrise", value=sunrise_time)
    
    with col6:
        # Convert 'sunset' to datetime and format it to 12-hour time (AM/PM)
        sunset_time = pd.to_datetime(df_today['sunset'].values[0]).strftime('%I:%M %p')
        st.metric(label="🌇 Sunset", value=sunset_time)

    with col7:
        # Display Lat/Long 
        st.write("🌍 Coordinates")
        st.write(f"**Latitude:** {ibadan_lat}")
        st.write(f"**Longitude:** {ibadan_lon}")
        

    # Create a two-column layout for the 
    col1, col2 = st.columns(2)

# 1. Temperature Trends over Time
    with col1:
        # Ensure the 'forecast_time' column is in datetime format
        df_daily['forecast_time'] = pd.to_datetime(df_daily['forecast_time'])

        # Format the date to '23 Aug'
        df_daily['date'] = df_daily['forecast_time'].dt.strftime('%d %b')

        # Create an interactive Plotly line chart for temperature trends
        fig = px.line(df_daily, x='forecast_time', y='temperature', 
                    title='Temperature Forecasts',
                    labels={'forecast_time': 'Time', 'temperature': 'Temperature (°C)'}, 
                    template='plotly_white')

        # Customize the layout for weather theme
        fig.update_traces(line_color='#ff7f0e', line_width=3, mode='lines+markers',
                        marker=dict(size=6, color='#ff7f0e', symbol='circle'))

        # Customize title and axis properties
        fig.update_layout(
            title=dict(
                text="Temperature Forecasts",  
                x=0.5,  # Center the title
                xanchor='center',  # Align it in the center
                yanchor='top',  # Optional: Align vertically at the top
                font=dict(size=20, color='#1f77b4', family="Arial Black")
            ),
            xaxis_title_font=dict(size=14, color='#4c4c4c'),
            yaxis_title_font=dict(size=14, color='#4c4c4c'),
            xaxis=dict(showgrid=True, gridcolor='lightgrey'),
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)'  # Overall transparent background
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
# 2. Plotly Map of Ibadan with Lat/Long
    with col2:
        st.markdown(
    """
    <h4 style="text-align: center; color: #1f77b4;">Ibadan Map & Coordinates</h4>
    """,
    unsafe_allow_html=True
)
        # Get the Mapbox token from the environment
        api_key = os.getenv("MAPBOXAPI_KEY") or st.secrets["MAPBOXAPI_KEY"]

        if api_key is None:
            st.error("Mapbox API key is not available")
        else:
            st.success("Mapbox API key is available")

        # Create a scatter mapbox for Ibadan
        fig = go.Figure(go.Scattermapbox(
            lat=[ibadan_lat],
            lon=[ibadan_lon],
            mode='markers',
            marker=go.scattermapbox.Marker(size=14, color='blue'),
            text=["Ibadan"],
        ))

        # Set the mapbox style and initial zoom
        fig.update_layout(
            mapbox=dict(
                style="streets",  # Change this to Mapbox-specific style like 'streets', 'satellite'
                center=dict(lat=ibadan_lat, lon=ibadan_lon),
                zoom=10,
                accesstoken=api_key  # Use the Mapbox token here
            ),
            height=400,
            margin={"r":0,"t":0,"l":0,"b":0}
        )

        # Show the map in Streamlit
        st.plotly_chart(fig)

        # Create a two-column layout for the map and coordinates (if needed)
        col1, col2 = st.columns(2)

# 3. Humidity vs Temperature
    with col1:
        # Ensure the 'forecast_time' column in df_daily is in datetime format
        df_daily['forecast_time'] = pd.to_datetime(df_daily['forecast_time'])

        # Create an interactive Plotly scatter plot for Humidity vs. Temperature
        fig = px.scatter(df_daily, x='temperature', y='humidity', 
                        title='Humidity vs. Temperature Forecasts',
                        labels={'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'},
                        template='plotly_white')

        # Customize scatter points and transparency
        fig.update_traces(marker=dict(size=12, color='#1f77b4', opacity=0.9))

        # Customize title and axis properties
        fig.update_layout(
            title=dict(
                text="Humidity vs. Temperature Forecasts",  # Your plot title
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Align the title based on the center
                yanchor='top',  # Keep the title at the top vertically
                font=dict(size=20, color='#2ca02c', family="Arial Black")  # Fresh green title
            ),
            xaxis_title_font=dict(size=14, color='#ff7f0e'),  # Warm orange for x-axis label
            yaxis_title_font=dict(size=14, color='#ff7f0e'),  # Warm orange for y-axis label
            xaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.5),
            yaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.5),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
        )

        # Display the plot in col1
        st.plotly_chart(fig, use_container_width=True)
        
# 4. Precipitation Probability
    with col2:
        # Step 1: Create a bar chart using Plotly
        x = df_daily['date']

        # Initialize the figure
        fig2 = go.Figure()

        # Add Temperature bars (warm orange color)
        fig2.add_trace(go.Bar(
            x=x, 
            y=df_daily['temperature'], 
            name='Temperature', 
            marker_color='#ff7f0e',
            hoverinfo='y'
        ))

        # Add Feels Like bars (harsher red color)
        fig2.add_trace(go.Bar(
            x=x, 
            y=df_daily['feels_like_temperature'], 
            name='Feels Like', 
            marker_color='#e63946',
            hoverinfo='y'
        ))

        # Update layout for interactivity, theming, and readability
        fig2.update_layout(
            barmode='group',  # Group the bars side by side
            title=dict(
                text='Temperature and Feels Like Forecasts',  # Title text
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Align the title based on the center
                yanchor='top',  # Keep the title at the top
                font=dict(size=20, color='#2ca02c', family="Arial Black")  # Green for title
            ),
            xaxis=dict(
                title='Date', 
                title_font=dict(size=14, color='#ff7f0e'),  # Orange for x-axis label
                tickformat='%d %b'  # Date format
            ),
            yaxis=dict(
                title='Temperature (°C)', 
                title_font=dict(size=14, color='#ff7f0e'),  # Orange for y-axis label
                showgrid=True, 
                gridcolor='lightgrey', 
                gridwidth=0.5  # Light grey grid
            ),
            legend=dict(x=0.9, y=1.15, orientation="h"),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
        )

        # Add tooltips and hover features
        fig2.update_traces(hovertemplate='%{y:.2f}°C')

        # Display the plot in Streamlit
        st.plotly_chart(fig2, use_container_width=True)

# 5. Precipitation Probability Over Time (Col 1)
    col1, col2 = st.columns(2)

    with col1:
        fig_precipitation = go.Figure()

        # Plot Precipitation Probability
        fig_precipitation.add_trace(go.Bar(
            x=df_daily['date'],
            y=df_daily['precipitation_probability'] * 100,
            name='Precipitation Probability Forcasts',
            marker_color='#1f77b4'  # Deep blue
        ))

        # Update layout for the Precipitation Probability plot
        fig_precipitation.update_layout(
            title=dict(
                text='Precipitation Probability Forecasts',
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Align the title at the center
                yanchor='top',  # Keep the title at the top
                font=dict(size=20, color='#1f77b4', family="Arial Black")  # Blue for title
            ),
            xaxis=dict(
                title='Date', 
                title_font=dict(size=14, color='#2ca02c'),  # Green for x-axis label
                tickformat='%d %b'  # Format for the date
            ),
            yaxis=dict(
                title='Precipitation Probability (%)',
                title_font=dict(size=14, color='#2ca02c'),  # Green for y-axis label
                gridcolor='lightgrey', 
                gridwidth=0.5  # Light grey grid
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            showlegend=False  # Hides the legend
        )

        # Display the precipitation plot
        st.plotly_chart(fig_precipitation, use_container_width=True)

# 6. Wind Speed and Pressure Over Time (Col 2)
    with col2:
        fig_wind_pressure = go.Figure()

        # Add Wind Speed bars
        fig_wind_pressure.add_trace(go.Bar(
            x=df_daily['date'],
            y=df_daily['wind_speed'],
            name='Wind Speed',
            marker_color='#bcbd22'  # Earthy brown
        ))

        # Add Pressure line
        fig_wind_pressure.add_trace(go.Scatter(
            x=df_daily['date'],
            y=df_daily['pressure'],
            mode='lines',
            name='Pressure',
            line=dict(color='#1f77b4', width=2)  
        ))

        # Update layout for the Wind Speed and Pressure plot
        fig_wind_pressure.update_layout(
            title=dict(
                text='Wind Speed and Pressure Forecasts',
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Align the title at the center
                yanchor='top',  # Keep the title at the top
                font=dict(size=20, color='#1f77b4', family="Arial Black")  # Blue for title
            ),
            xaxis=dict(
                title='Date', 
                title_font=dict(size=14, color='#2ca02c'),  # Green for x-axis label
                tickformat='%d %b'
            ),
            yaxis=dict(
                title='Wind Speed (m/s)',
                title_font=dict(size=14, color='#2ca02c'),  # Green for y-axis label
                gridcolor='lightgrey', 
                gridwidth=0.4
            ),
            yaxis2=dict(
                title='Pressure (hPa)', 
                overlaying='y', 
                side='right', 
                showgrid=False, 
                tickfont=dict(color='#7f7f7f')  # Grey for the secondary axis
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            showlegend=True  # Display the legend
        )

        # Display the Wind Speed and Pressure plot
        st.plotly_chart(fig_wind_pressure, use_container_width=True)

    # Create two columns
    col1, col2 = st.columns(2)

# 7. Temperature Range Plot as an Area Chart
    with col1:
        # Create an area chart for temperature range
        fig_temp_range = go.Figure()

        # Max temperature (area fill)
        fig_temp_range.add_trace(go.Scatter(
            x=df_daily['date'],
            y=df_daily['max_temperature'],
            name='Max Temp',
            fill='tonexty',
            mode='none',  # No line, just filled area
            fillcolor='rgba(255, 69, 0, 0.6)',  # Red-orange fill
        ))

        # Min temperature (area fill)
        fig_temp_range.add_trace(go.Scatter(
            x=df_daily['date'],
            y=df_daily['min_temperature'],
            name='Min Temp',
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(30, 144, 255, 0.6)',  # Cool blue fill
        ))

        # Update layout for temperature plot
        fig_temp_range.update_layout(
            title=dict(
                text='Today & 5-Day Temperature Forecast',
                x=0.5,  # Center the title
                xanchor='center',  # Align title center
                yanchor='top',  # Keep the title at the top
                font=dict(size=20, color='#2ca02c', family="Arial Black")  # Green title
            ),
            xaxis=dict(
                title='Date',
                title_font=dict(size=14, color='#ff7f0e'),  # Warm orange for x-axis
                tickformat='%d %b'  # Format date as "23 Aug"
            ),
            yaxis=dict(
                title='Temperature (°C)',
                title_font=dict(size=14, color='#ff7f0e')  # Warm orange for y-axis
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            showlegend=True,  # Show legend
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            )  # Horizontal legend at the top
        )

        # Display the area plot in col1
        st.plotly_chart(fig_temp_range, use_container_width=True)

# 8. Humidity Over Time as an Area Chart
    with col2:
        # Create an area chart for humidity
        fig_humidity = go.Figure()

        # Plot Humidity with fill
        fig_humidity.add_trace(go.Scatter(
            x=df_daily['date'],
            y=df_daily['humidity'],
            name='Humidity',
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(225, 69, 0, 0.6)',  
        ))

        # Update layout for humidity plot
        fig_humidity.update_layout(
            title=dict(
                text='Today & A 5-Day Humidity Forecast',
                x=0.5,  # Center the title
                xanchor='center',  # Align title center
                yanchor='top',  # Keep the title at the top
                font=dict(size=20, color='#2ca02c', family="Arial Black")  # Green title
            ),
            xaxis=dict(
                title='Date',
                title_font=dict(size=14, color='#ff7f0e'),  # Warm orange for x-axis title
                tickformat='%d %b'  # Format date as "23 Aug"
            ),
            yaxis=dict(
                title='Humidity (%)',
                title_font=dict(size=14, color='#ff7f0e')  # Warm orange for y-axis title
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            showlegend=True,  # Enable the legend
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1
            )  # Horizontal legend at the top
        )

        # Display the area plot in col2
        st.plotly_chart(fig_humidity, use_container_width=True)

# Step 1: Calculate the correlation matrix for the weather data
    corr_matrix = df_daily[['temperature', 'feels_like_temperature', 'humidity', 'cloudiness', 'precipitation_probability', 'wind_speed', 'pressure']].corr()

    # Step 2: Convert correlation matrix to a 2D array for plotting
    z = corr_matrix.values
    x_labels = corr_matrix.columns.tolist()
    y_labels = corr_matrix.columns.tolist()

    # Step 3: Create the heatmap using Plotly
    fig_heatmap = ff.create_annotated_heatmap(
        z, 
        x=x_labels, 
        y=y_labels, 
        colorscale='RdBu',  # Red-Blue color scheme for weather
        reversescale=True,  # To match the coolwarm theme
        annotation_text=np.round(z, decimals=2),  # Display correlation values
        showscale=True  # Color bar scale
    )

    # Step 4: Update the layout for the heatmap
    fig_heatmap.update_layout(
        title=dict(
            text='Correlation Heatmap of Weather Variables',
            x=0.5,  # Center the title horizontally
            xanchor='center',  # Anchor the title to the center
            yanchor='top',  # Keep the title at the top
            font=dict(size=20, color='#FF8C00', family="Arial Black")  # Warm orange for the title
        ),
        xaxis_nticks=len(x_labels),  # Ensure we have labels for all columns
        yaxis_nticks=len(y_labels),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
    )

    # Display the Plotly heatmap in Streamlit
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer in Streamlit using st.markdown with enhanced styling
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #333333;
        text-align: center;
        padding: 10px;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
    }
    .footer a {
        color: #2980b9;
        text-decoration: none;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        <p><strong>Project by Freda</strong> | 
        <a href="https://github.com/your-github-repo-link" target="_blank">See my GitHub repo</a> |
        <a href="https://linkedin.com/your-profile" target="_blank">LinkedIn</a>
        </p>
        <p>© 2024 Freda's Weather Dashboard</p>
    </div>
    """

# Display the footer using markdown
st.markdown(footer, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json

# Sample data for demonstration
data = pd.DataFrame({
    'Date': pd.date_range('2022-01-01', '2022-01-31', freq='D'),
    'Active_Users': np.random.randint(100, 500, size=31),
    'Session_Duration': np.random.uniform(5, 30, size=31),
    'User_Retention': np.random.uniform(20, 60, size=31),
    'Videos_Processed': np.random.randint(50, 200, size=31),
    'User_Satisfaction': np.random.uniform(3.5, 5, size=31),
    'Popular_Themes': np.random.choice(['Theme A', 'Theme B', 'Theme C'], size=31),
    'Trending_Topic': np.random.choice(['Topic X', 'Topic Y', 'Topic Z'], size=31),
    'Most_Used_Feature': np.random.choice(['Feature 1', 'Feature 2', 'Feature 3'], size=31),
    'User_Location': np.random.choice(['USA', 'Europe', 'Asia'], size=len(pd.date_range('2022-01-01', '2022-01-31', freq='D')))
})
st.set_page_config(layout="wide")
# Sidebar with logo and user choices
with st.sidebar:
    st.image("hero.png", width=100, use_column_width=True)


    st.title("Analytics Dashboard")
    st.subheader("User Options")

    # User choices
    selected_metric = st.selectbox("Select Metric", ['Active_Users', 'Session_Duration', 'User_Retention'])
    
    # Convert date_input to pandas Timestamp
    selected_date_range = pd.to_datetime(st.date_input("Select Date Range", [data['Date'].min(), data['Date'].max()]))

    st.subheader("Social Media Platform")
    selected_platform = st.radio("Select Platform", ['Twitter', 'Facebook', 'Instagram', 'LinkedIn'])

# Filter data based on user choices
filtered_data = data[(data['Date'] >= selected_date_range[0]) & (data['Date'] <= selected_date_range[1])]

# Main content area
st.title("User Engagement Metrics and Content Metrics")

# First row with two columns
col1, col2 = st.columns(2)

# Column 1: User Engagement Metrics
with col1:
    st.subheader("User Engagement Metrics")
    
    # Chart 1: Active Users over Time
    fig1 = px.line(filtered_data, x='Date', y='Active_Users', title='Active Users Over Time')
    st.plotly_chart(fig1)

    # Additional user engagement details
    st.metric("Session Duration", round(filtered_data['Session_Duration'].mean(), 2))
    st.metric("User Retention", round(filtered_data['User_Retention'].mean(), 2))

# Column 2: Content Metrics
with col2:
    st.subheader("Content Metrics")
    
    # Chart 2: Videos Processed over Time
    fig2 = px.line(filtered_data, x='Date', y='Active_Users', title='Active Users Over Time')
    st.plotly_chart(fig2)

    # Additional content metrics
    st.metric("User Satisfaction", round(filtered_data['User_Satisfaction'].mean(), 2))
    st.subheader("Popular Themes")
    st.bar_chart(filtered_data['Popular_Themes'].value_counts())

# Trends Section
st.title("Trends Section")

# User input for platform choice
selected_trend_platform = st.selectbox("Select Platform for Trends", ['Twitter', 'Facebook', 'Instagram', 'LinkedIn'])

# Filter data for trends based on user input
trends_data = data[data['User_Location'] == selected_trend_platform]

# Chart 3: Trending Topics
st.subheader("Trending Topics")
st.bar_chart(trends_data['Trending_Topic'].value_counts())

# Chart 4: Trend Analysis Over Time
fig3 = px.line(trends_data, x='Date', y='User_Satisfaction', title=f"Trend Analysis Over Time - {selected_trend_platform}")
st.plotly_chart(fig3)

# Next section divided into 2 columns
st.title("Feature and Format Usage")


with st.container():
    st.subheader("Most Used Features")
    st.bar_chart(data['Most_Used_Feature'].value_counts())

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",dtype={"fips": str})
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:counties = json.load(response)

with st.container():
    st.subheader("Geographical Distribution of Users")
    
    fig_map = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Blues",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'user':'engagement rate'}
                          )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map)

import streamlit as st
import numpy as np
import joblib
import pickle

model = joblib.load("Air-Quality-Prediction-Model.pkl")

with open("label_encoder.pkl", "rb") as file:
    label_encoder = pickle.load(file)

def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://your-image-url.com/bg.jpg");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

st.image("aqi.jpg", use_container_width=True)
st.title("🌍 Air Quality Prediction App 🏭")


st.sidebar.image("side_bar.jpg", use_container_width=True)
st.sidebar.header("⚙️ Enter Input Values")

pm25 = st.sidebar.number_input("PM2.5", min_value=0.0, step=0.1)
pm10 = st.sidebar.number_input("PM10", min_value=0.0, step=0.1)
no = st.sidebar.number_input("NO", min_value=0.0, step=0.1)
no2 = st.sidebar.number_input("NO2", min_value=0.0, step=0.1)
nox = st.sidebar.number_input("NOx", min_value=0.0, step=0.1)
nh3 = st.sidebar.number_input("NH3", min_value=0.0, step=0.1)
co = st.sidebar.number_input("CO", min_value=0.0, step=0.01)
so2 = st.sidebar.number_input("SO2", min_value=0.0, step=0.1)
o3 = st.sidebar.number_input("O3", min_value=0.0, step=0.1)
benzene = st.sidebar.number_input("Benzene", min_value=0.0, step=0.1)
toluene = st.sidebar.number_input("Toluene", min_value=0.0, step=0.1)
xylene = st.sidebar.number_input("Xylene", min_value=0.0, step=0.1)
aqi = st.sidebar.number_input("AQI", min_value=0.0, step=0.1)

# Prediction Button
if st.sidebar.button("Predict AQI Bucket"):
    features = np.array([[pm25, pm10, no, no2, nox, nh3, co, so2, o3, benzene, toluene, xylene, aqi]])

    # Get AQI Bucket Prediction (numeric)
    predicted_bucket_encoded = model.predict(features)[0]

    # Convert numeric prediction to AQI category
    predicted_bucket = label_encoder.inverse_transform([predicted_bucket_encoded])[0]

    # AQI Color Mapping
    aqi_colors = {
        "Good": "green",
        "Satisfactory": "blue",
        "Moderate": "yellow",
        "Poor": "orange",
        "Very Poor": "red",
        "Severe": "purple"
    }

    st.markdown(f"<h2 style='color:{aqi_colors[predicted_bucket]};'>Predicted AQI Category: {predicted_bucket}</h2>",
                unsafe_allow_html=True)

    health_recommendations = {
        "Good": "🟢 **Good**: The air quality is excellent! You can safely enjoy outdoor activities like walking, running, or cycling. 🌳🌞",
        "Satisfactory": "🔵 **Satisfactory**: The air quality is decent. Sensitive individuals might feel mild effects. Consider staying inside for extended periods if you have respiratory issues. 🏃‍♂️🌿",
        "Moderate": "🟡 **Moderate**: Air quality is moderate. Sensitive individuals may experience mild respiratory effects. Limit outdoor activities like jogging. 🌫️💨",
        "Poor": "🟠 **Poor**: Air quality is poor. Limit outdoor physical activities, and consider using a mask if you need to go outside. 🏙️🚶‍♀️🛑",
        "Very Poor": "🔴 **Very Poor**: The air quality is very poor. It's highly recommended to stay indoors and avoid any outdoor activities. Use air purifiers if possible. 😷🏠",
        "Severe": "🟣 **Severe**: The air quality is hazardous! Stay indoors at all costs and avoid outdoor physical activities. Consider using HEPA air purifiers. 😷💨🚫"
    }


    st.markdown(f"### Health Recommendation:\n\n{health_recommendations[predicted_bucket]}")

    environmental_suggestions = {
        "Good": "🌱 **Good**: Keep up the great work! Continue using eco-friendly transportation (e.g., cycling, walking) and reducing emissions. 🚶‍♂️🚴‍♀️",
        "Satisfactory": "🛣️ **Satisfactory**: Consider reducing vehicle use or switching to electric cars to further improve air quality. 🚗💨➡️🚙🔋",
        "Moderate": "🌳 **Moderate**: Plant more trees in urban areas and consider using public transportation to reduce pollution. 🏙️🌳🚍",
        "Poor": "🚶‍♂️ **Poor**: Limit car use and consider using cleaner energy sources. Walk or use public transport instead. 🌱🌍",
        "Very Poor": "🏙️ **Very Poor**: Encourage your community to plant trees and support eco-friendly policies. Reduce industrial emissions! 🌍🌿",
        "Severe": "⚡ **Severe**: Immediate action is needed: Reduce traffic emissions, switch to renewable energy, and advocate for stricter pollution control measures. 🚗💨⛔"
    }

    st.markdown(f"### Environmental Suggestion:\n\n{environmental_suggestions[predicted_bucket]}")

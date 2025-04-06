import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# ---------------------- SQLite DB Setup ----------------------
conn = sqlite3.connect('farm_data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        soil_ph REAL,
        moisture REAL,
        temperature REAL,
        rainfall REAL,
        crop TEXT,
        yield_prediction REAL,
        sustainability_score INTEGER,
        expert_advice TEXT
    )
''')
conn.commit()

# ---------------------- Utility Functions ----------------------

def predict_crop(soil_ph, moisture, temp, rainfall):
    # Dummy logic for example
    if soil_ph < 6.5 and rainfall > 300:
        return "Rice or Corn"
    elif soil_ph >= 6.5 and temp > 30:
        return "Millet or Sorghum"
    else:
        return "Wheat or Barley"

def estimate_yield(moisture, rainfall):
    return round((moisture * 0.3 + rainfall * 0.7) / 10, 2)

def compute_sustainability(fertilizer, pesticide):
    score = 10 - (fertilizer + pesticide) / 20
    return max(0, round(score, 1))

def generate_advice(crop):
    return f"Optimal conditions for growing {crop.split()[0]} based on your inputs."

# ---------------------- UI ----------------------

st.set_page_config(page_title="AgroAdvisor AI", layout="centered")
st.title("🌾 Sustainable Agriculture Advisor")

# Input Form
with st.form("input_form"):
    st.subheader("Enter Farm Details")

    soil_ph = st.slider("Soil pH", 3.5, 9.0, 6.5)
    moisture = st.slider("Soil Moisture (%)", 0.0, 100.0, 45.0)
    temp = st.slider("Temperature (°C)", 10, 45, 28)
    rainfall = st.slider("Rainfall (mm)", 0, 500, 200)
    fertilizer = st.slider("Fertilizer Used (kg)", 0, 100, 20)
    pesticide = st.slider("Pesticide Used (kg)", 0, 100, 10)

    submitted = st.form_submit_button("🌿 Get Recommendation")

# ---------------------- Recommendation Logic ----------------------

if submitted:
    final_crop = predict_crop(soil_ph, moisture, temp, rainfall)
    yield_pred = estimate_yield(moisture, rainfall)
    sustainability = compute_sustainability(fertilizer, pesticide)
    advice = generate_advice(final_crop)

    # Save to DB
    cursor.execute('''
        INSERT INTO recommendations 
        (soil_ph, moisture, temperature, rainfall, crop, yield_prediction, sustainability_score, expert_advice)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (soil_ph, moisture, temp, rainfall, final_crop, yield_pred, sustainability, advice))
    conn.commit()

    # Apply Custom CSS
    st.markdown("""
        <style>
            .card {
                background-color: #fff3e0;
                border-radius: 16px;
                padding: 24px;
                margin-top: 1rem;
                box-shadow: 0 6px 20px rgba(0,0,0,0.12);
                transition: all 0.3s ease;
            }
            .card:hover {
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                transform: translateY(-5px);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card'>
        <h2 style='color:#4e342e;'>🌱 Suggested Crop: 
            <span style='color:#2e7d32; font-weight: bold;'>{final_crop}</span>
        </h2>
        <p style='font-size: 18px; color: #6d4c41;'>
            <strong>📈 Predicted Yield:</strong> 
            <span style='font-weight:bold'>{yield_pred:.2f} tons/acre</span>
        </p>
        <p style='font-size: 18px; color: #4e342e;'>
            <strong>🌍 Sustainability Score:</strong> 
            <span style='font-weight:bold'>{sustainability}/10</span>
        </p>
        <p style='font-size: 17px; color:#5d4037;'>
            <strong>🧠 Expert Advice:</strong> 
            <em>{advice}</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- View Previous Recommendations ----------------------

st.subheader("📊 Recent Recommendations")
df = pd.read_sql_query("SELECT * FROM recommendations ORDER BY id DESC LIMIT 5", conn)
if not df.empty:
    st.dataframe(df[['soil_ph', 'moisture', 'temperature', 'rainfall', 'crop', 'yield_prediction', 'sustainability_score']])
else:
    st.info("No past recommendations yet.")

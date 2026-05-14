import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# --- Page Configuration ---
st.set_page_config(page_title="5G Network Intelligence", layout="wide", page_icon="📡")

# Custom CSS to make it look modern
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 5G Smart Network Intelligence Dashboard")
st.markdown("---")

# --- Load Model ---
@st.cache_resource
def load_model():
    return joblib.load("power_model.pkl")

model = load_model()

# --- Sidebar Design ---
with st.sidebar:
    st.header("🎛️ Network Control")
    st.info("Adjust parameters to test real-time predictions.")
    
    signal    = st.slider("Signal Strength (dBm)", -120, -30, -75)
    snr       = st.slider("SNR (Signal-to-Noise)", 0, 30, 15)
    traffic   = st.slider("Network Traffic (%)", 0, 100, 50)
    distance  = st.slider("Distance to Tower (m)", 50, 1000, 300)
    data_rate = st.slider("Current Data Rate (Mbps)", 1, 100, 20)
    
    st.divider()
    st.write("📍 **Location:** IIEST Shibpur Campus")

# --- Logic Section ---
features = pd.DataFrame(
    [[signal, snr, traffic, distance, data_rate]], 
    columns=['signal', 'snr', 'traffic', 'distance', 'data_rate']
)
prediction = model.predict(features)[0]
labels = {0: "LOW POWER", 1: "MODERATE POWER", 2: "HIGH POWER"}
colors = {0: "🟢", 1: "🟡", 2: "🔴"}
result_text = labels.get(prediction, "UNKNOWN")

# --- Main Dashboard Layout ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric(label="Predicted Power Class", value=f"{colors.get(prediction, '')} {result_text}")

with col2:
    st.metric(label="Target SNR", value=f"{snr} dB")

with col3:
    st.metric(label="Traffic Load", value=f"{traffic}%")

st.markdown("### Live Network Analytics")
tab1, tab2 = st.tabs([" Real-time Feed", "Signal Trend"])

with tab1:
    try:
        df = pd.read_csv("network_data.csv")
        st.dataframe(df.tail(10), use_container_width=True)
    except:
        st.warning("Waiting for simulate.py to start...")

with tab2:
    if 'df' in locals() and not df.empty:
        # Show a simple line chart of the last 20 signal readings
        st.line_chart(df['signal'].tail(20))
    else:
        st.info("Start simulation to view signal trends.")

st.markdown("---")
st.caption("Mini Project | Computer Science & Technology | 5G Network Traffic Prediction")
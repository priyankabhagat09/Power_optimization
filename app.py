import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- TECH-THEME CONFIGURATION ---
st.set_page_config(page_title="SIGNAL_CORE_V1", layout="wide")

# Custom CSS for a professional "Command Center" look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains+Mono', monospace;
        background-color: #0e1117;
    }
    
    /* Technical Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00e6e6;
        font-weight: 500;
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px;
        color: #808495;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Clean Sidebar */
    .css-1d391kg {
        background-color: #161b22;
    }
    
    /* Bordered sections for a structured look */
    .stMetric {
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 4px;
        background-color: #0d1117;
    }

    hr {
        margin: 1em 0;
        border: 0;
        border-top: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL UTILITY ---
@st.cache_resource
def load_system_model():
    # Ensure this matches the file name in your directory
    return joblib.load("power_model.pkl")

model = load_system_model()

# --- HEADER SECTION ---
st.text("NETWORK_ANALYSIS_SYSTEM // VERSION_1.0.4")
st.title("5G BEAMFORMING & POWER CONTROL")
st.caption("IIEST SHIBPUR | COMPUTER SCIENCE & TECHNOLOGY")
st.markdown("---")

# --- CONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### SYSTEM_PARAMETERS")
    st.markdown("---")
    
    # Using specific ranges relevant to 5G signaling
    signal    = st.slider("SIGNAL_INPUT (dBm)", -120, -30, -75)
    snr       = st.slider("SNR_THRESHOLD (dB)", 0, 30, 15)
    traffic   = st.slider("TRAFFIC_LOAD (%)", 0, 100, 50)
    distance  = st.slider("NODE_DISTANCE (m)", 50, 1000, 300)
    data_rate = st.slider("THROUGHPUT (Mbps)", 1, 100, 20)
    
    st.markdown("---")
    st.text("STATUS: CORE_ACTIVE")
    st.text("MODE: REAL_TIME_INFERENCE")

# --- INFERENCE ENGINE ---
features = pd.DataFrame(
    [[signal, snr, traffic, distance, data_rate]], 
    columns=['signal', 'snr', 'traffic', 'distance', 'data_rate']
)
prediction = model.predict(features)[0]

# Mapping numeric results to technical string labels
labels = {0: "LOW_POWER_OUTPUT", 1: "MODERATE_POWER_OUTPUT", 2: "CRITICAL_HIGH_POWER"}
system_status = labels.get(prediction, "UNKNOWN_STATE")

# --- PRIMARY DISPLAY ---
# Three columns for metrics to keep the top of the screen balanced
m1, m2, m3 = st.columns(3)

with m1:
    st.metric(label="PREDICTED_STATE", value=system_status)
with m2:
    st.metric(label="SNR_VALUE", value=f"{snr} dB")
with m3:
    st.metric(label="NETWORK_CONGESTION", value=f"{traffic} %")

st.markdown("---")

# --- DATA VISUALIZATION TABS ---
st.text("ANALYSIS_STREAM")
tab_data, tab_plot = st.tabs(["[ DATA_LOG ]", "[ SIGNAL_WAVEFORM ]"])

with tab_data:
    try:
        df = pd.read_csv("network_data.csv")
        # Displaying with full width to fill empty space
        st.dataframe(df.tail(12), use_container_width=True)
    except:
        st.info("SYSTEM_MESSAGE: No historical data found. Initiate simulate.py to populate log.")

with tab_plot:
    if 'df' in locals() and not df.empty:
        # Minimalist line chart with a custom cyan-tech color
        st.line_chart(df['signal'].tail(40), color="#00e6e6")
    else:
        st.text("SYSTEM_MESSAGE: Waiting for signal detection...")

st.markdown("---")
st.caption("INTERNAL_USE_ONLY // ADITYA_KUMAR")
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Power Optimization",
    page_icon="📡",
    layout="wide"
)

# --- CUSTOM TECH THEME CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root {
    --bg: #dbe6f5;
    --panel: #ffffff;
    --border: rgba(20, 60, 120, 0.08);
    --text: #143a72;
    --muted: #7d8fa8;
    --accent: #15468b;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg);
    color: var(--text);
}

.stApp {
    background: linear-gradient(135deg, #dbe6f5 0%, #edf3fb 100%);
}

h1 {
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: var(--accent);
    margin-bottom: 0.2rem;
}

.dashboard-subtitle {
    color: var(--muted);
    font-size: 0.9rem;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 22px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 8px 24px rgba(21, 70, 139, 0.06);
}

.status-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    background: rgba(21, 70, 139, 0.08);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
}

.section-label {
    color: var(--muted);
    font-size: 0.78rem;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* Tab text styling */
button[data-baseweb="tab"] p {
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --- MODEL UTILITY ---
@st.cache_resource
def load_system_model():
    return joblib.load("power_model.pkl")

model = load_system_model()

# --- HEADER ---
st.title("POWER OPTIMIZATION")
st.markdown('<div class="dashboard-subtitle">Real-Time Signal Analysis</div>', unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### SYSTEM PARAMETERS")
    st.markdown("---")

    signal = st.slider("SIGNAL INPUT (dBm)", -120, -30, -75)
    snr = st.slider("SNR THRESHOLD (dB)", 0, 30, 15)
    traffic = st.slider("TRAFFIC LOAD (%)", 0, 100, 50)
    distance = st.slider("NODE DISTANCE (m)", 50, 1000, 300)
    data_rate = st.slider("THROUGHPUT (Mbps)", 1, 100, 20)

    st.markdown("---")
    st.markdown('<div class="status-badge">● Core Active</div>', unsafe_allow_html=True)
    st.caption("MODE: REAL-TIME INFERENCE")

# --- INFERENCE ENGINE ---
features = pd.DataFrame(
    [[signal, snr, traffic, distance, data_rate]],
    columns=["signal", "snr", "traffic", "distance", "data_rate"]
)

prediction = model.predict(features)[0]
labels = {0: "LOW_POWER_OUTPUT", 1: "MODERATE_POWER_OUTPUT", 2: "CRITICAL_HIGH_POWER"}
system_status = labels.get(prediction, "UNKNOWN_STATE")

# --- PRIMARY METRICS ---
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("PREDICTED STATE", system_status)
with m2:
    st.metric("SNR VALUE", f"{snr} dB")
with m3:
    st.metric("NETWORK CONGESTION", f"{traffic} %")

st.markdown("---")

# --- ANALYSIS SECTION ---
st.markdown('<div class="section-label">Analysis_Output</div>', unsafe_allow_html=True)

# Define the two distinct tabs
tab_data, tab_plot = st.tabs(["[ DATA_LOG ]", "[ SIGNAL_WAVEFORM ]"])

# Try to load the CSV data once for use in both tabs
try:
    df = pd.read_csv("network_data.csv")
except Exception:
    df = pd.DataFrame() # Create empty if not found

with tab_data:
    if not df.empty:
        st.dataframe(df.tail(12), use_container_width=True, hide_index=True)
    else:
        st.info("SYSTEM_MESSAGE: No historical data found. Initiate simulate.py to populate the log.")

with tab_plot:
    if not df.empty and "signal" in df.columns:
        st.line_chart(df["signal"].tail(40), use_container_width=True)
    else:
        st.text("SYSTEM_MESSAGE: Waiting for signal detection stream...")

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="SIGNAL_CORE_V1", page_icon="📡", layout="wide")

# 2. CSS STYLING (Paste your long <style> block here)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #dbe6f5;                 /* Light blue background */
    --panel: #ffffff;              /* White cards */
    --panel-2: #f5f8fd;            /* Secondary panels */
    --border: rgba(20, 60, 120, 0.08);

    --text: #143a72;               /* Deep blue text */
    --muted: #7d8fa8;              /* Gray-blue secondary text */

    --accent: #15468b;             /* Royal blue */
    --accent-dark: #0f3870;        /* Darker title blue */
    --accent-soft: rgba(21, 70, 139, 0.08);

    --success: #15468b;
}

/* Global */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg);
    color: var(--text);
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #dbe6f5 0%, #edf3fb 50%, #f7fbff 100%);
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
    box-shadow: 4px 0 20px rgba(21, 70, 139, 0.04);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* Sidebar heading */
section[data-testid="stSidebar"] h3 {
    color: var(--accent);
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* Main Title */
h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px;
    color: var(--accent-dark) !important;
    margin-bottom: 0.2rem;
    text-shadow: 0 2px 8px rgba(21, 70, 139, 0.08);
}

/* Subtitle */
.dashboard-subtitle {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid rgba(21, 70, 139, 0.08);
    margin: 1.2rem 0;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 22px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 8px 24px rgba(21, 70, 139, 0.06);
    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(21, 70, 139, 0.10);
    border-color: rgba(21, 70, 139, 0.18);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: var(--accent-dark);
    font-size: 1.4rem;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: #ffffff;
    color: var(--accent);
    border: 1px solid rgba(21, 70, 139, 0.10);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(21, 70, 139, 0.05);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff;
    color: var(--text);
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 12px;
}

/* Sliders */
.stSlider > div[data-baseweb="slider"] > div {
    color: var(--accent);
}

/* Tabs */
button[data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border: none;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-dark);
    font-weight: 700;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(21, 70, 139, 0.05);
}

/* Info Box */
[data-testid="stInfo"] {
    background: #ffffff;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 14px;
    color: var(--text);
}

/* Status Badge */
.status-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    background: rgba(21, 70, 139, 0.08);
    border: 1px solid rgba(21, 70, 139, 0.10);
    color: var(--accent-dark);
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
}

/* Section Label */
.section-label {
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* Charts */
[data-testid="stVerticalBlock"] > div:has(canvas),
[data-testid="stPlotlyChart"],
[data-testid="stLineChart"] {
    background: #ffffff;
    border-radius: 18px;
    padding: 0.5rem;
}

/* Generic Containers */
div[data-testid="stContainer"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)


# 3. MODEL LOADING
@st.cache_resource
def load_system_model():
    return joblib.load("power_model.pkl")

model = load_system_model()

# 4. SIDEBAR (Define these variables BEFORE the loop)
with st.sidebar:
    st.markdown("### SYSTEM PARAMETERS")
    signal = st.slider("SIGNAL INPUT (dBm)", -120, -30, -75)
    snr = st.slider("SNR THRESHOLD (dB)", 0, 30, 15)
    traffic = st.slider("TRAFFIC LOAD (%)", 0, 100, 50)
    distance = st.slider("NODE DISTANCE (m)", 50, 1000, 300)
    data_rate = st.slider("THROUGHPUT (Mbps)", 1, 100, 20)

# 5. STATIC HEADER
st.title("POWER OPTIMIZATION")
st.markdown('<div class="dashboard-subtitle">Real-Time Signal Analysis & Inference Engine</div>', unsafe_allow_html=True)

# 6. INITIALIZE DYNAMIC ASSETS
labels = {0: "LOW_POWER_OUTPUT", 1: "MODERATE_POWER_OUTPUT", 2: "CRITICAL_HIGH_POWER"}
dynamic_container = st.empty()

# 7. THE LIVE LOOP (Place this at the very bottom)
while True:
    try:
        df = pd.read_csv("network_data.csv")
        latest_data = df.iloc[-1]
        live_signal = latest_data.get('signal', signal)
        live_snr = latest_data.get('snr', snr)
        live_traffic = latest_data.get('traffic', traffic)
    except Exception:
        live_signal, live_snr, live_traffic = signal, snr, traffic
        df = pd.DataFrame()

    # Inference logic
    features = pd.DataFrame(
        [[live_signal, live_snr, live_traffic, distance, data_rate]],
        columns=["signal", "snr", "traffic", "distance", "data_rate"]
    )
    prediction = model.predict(features)[0]
    system_status = labels.get(prediction, "UNKNOWN_STATE")

    # Update UI inside the placeholder
    with dynamic_container.container():
        m1, m2, m3 = st.columns(3)
        m1.metric("PREDICTED STATE", system_status)
        m2.metric("SNR VALUE", f"{live_snr} dB")
        m3.metric("NETWORK CONGESTION", f"{live_traffic} %")

        st.markdown("---")
        st.markdown('<div class="section-label">Analysis</div>', unsafe_allow_html=True)
        tab_data, tab_plot = st.tabs(["[ DATA LOG ]", "[ SIGNAL WAVEFORM ]"])

        with tab_data:
            if not df.empty:
                st.dataframe(df.tail(12), use_container_width=True, hide_index=True)
        with tab_plot:
            if not df.empty and "signal" in df.columns:
                st.line_chart(df["signal"].tail(40), use_container_width=True)

    time.sleep(3)
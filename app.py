import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="SIGNAL_CORE_V1", page_icon="📡", layout="wide")

# 2. CSS STYLING (Paste your long <style> block here)
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

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
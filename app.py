import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from datetime import datetime

# Configure the web page
st.set_page_config(page_title="🛡️ AI-Powered USB Threat Detection System")

# Title and Header
st.title("🛡️ AI-Powered USB Threat Detection System")
st.markdown("Real-time behavioral anomaly scanning using Isolation Forest machine learning.")
st.divider()

# Load the trained AI model
@st.cache_resource
def load_model():
    if os.path.exists("models/usb_threat_detector.pkl"):
        return joblib.load("models/usb_threat_detector.pkl")
    return None

model = load_model()

if model is None:
    st.error("❌ AI Model file not found! Please run train_model.py first.")
    st.stop()

# Sidebar for controls and actions
st.sidebar.header("🛡️ System Controls")
st.sidebar.success("AI Engine State: ACTIVE")

# Simulation button to mimic a live USB insertion event
st.sidebar.subheader("Simulate USB Attachment")
device_type = st.sidebar.selectbox("Select Device Behavior Profile", ["Normal Flash Drive", "BadUSB (Rubber Ducky)", "Ransomware Script"])
trigger_scan = st.sidebar.button("Plug In Selected Device")

# Define profiles for simulation
if trigger_scan:
    if device_type == "Normal Flash Drive":
        delay, vol, entropy = np.random.uniform(120, 180), np.random.uniform(0.1, 1.2), np.random.uniform(2.0, 4.5)
    elif device_type == "BadUSB (Rubber Ducky)":
        delay, vol, entropy = np.random.uniform(2, 8), np.random.uniform(0.01, 0.05), np.random.uniform(3.0, 5.0)
    else: # Ransomware Script
        delay, vol, entropy = np.random.uniform(100, 150), np.random.uniform(35, 60), np.random.uniform(7.4, 7.9)

    # Run AI prediction (-1 = Anomaly, 1 = Normal)
    input_data = pd.DataFrame([[delay, vol, entropy]], columns=["keystroke_delay", "transfer_volume", "entropy"])
    prediction = model.predict(input_data)[0]
    
    # Save log entry
    status = "🚨 THREAT BLOCKED" if prediction == -1 else "✅ SAFE"
    new_log = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Profile Name": device_type,
        "Keystroke Delay (ms)": round(delay, 2),
        "Data Volume (GB)": round(vol, 2),
        "File Entropy": round(entropy, 2),
        "AI Status": status
    }])
    
    # Persistent logs saving to CSV
    log_file = "data/live_scan_history.csv"
    if os.path.exists(log_file):
        existing_logs = pd.read_csv(log_file)
        updated_logs = pd.concat([new_log, existing_logs], ignore_index=True)
    else:
        updated_logs = new_log
    updated_logs.to_csv(log_file, index=False)

# Main Dashboard layout metrics
log_file = "data/live_scan_history.csv"
if os.path.exists(log_file):
    history_df = pd.read_csv(log_file)
    total_scans = len(history_df)
    threats_found = len(history_df[history_df["AI Status"] == "🚨 THREAT BLOCKED"])
else:
    history_df = pd.DataFrame()
    total_scans = 0
    threats_found = 0

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Devices Analyzed", value=total_scans)
col2.metric(label="Active Threats Intercepted", value=threats_found, delta=f"{threats_found} blocked", delta_color="inverse")
col3.metric(label="System Core Health", value="100% Safe")

st.markdown("### 📊 Real-Time Scanning Stream")
if not history_df.empty:
    # Stylize the table rows depending on threat level
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("Waiting for device insertion telemetry logs... Use the sidebar simulation tool to test live events instantly.")
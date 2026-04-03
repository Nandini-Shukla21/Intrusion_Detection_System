import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Intrusion Detection System", layout="wide")

st.title("🚨 Intelligent Intrusion Detection System")

# Load your saved results
df = pd.read_csv("intrusion_logs.csv")

# Metrics
total = len(df)
attacks = df[df['Predicted'] == 1].shape[0]
normal = df[df['Predicted'] == 0].shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Traffic", total)
col2.metric("Normal Traffic", normal)
col3.metric("Attacks Detected", attacks)

st.markdown("---")

# Anomaly Score Graph
st.subheader("📉 Anomaly Score Distribution")
st.line_chart(df['Anomaly_Score'])

# Filter
st.subheader("🔍 Filter Data")

option = st.selectbox(
    "Select Traffic Type",
    ("All", "Normal", "Attack")
)

if option == "Normal":
    filtered_df = df[df['Predicted'] == 0]
elif option == "Attack":
    filtered_df = df[df['Predicted'] == 1]
else:
    filtered_df = df

# Show Table
st.subheader("📋 Traffic Logs with Explanation")
st.dataframe(filtered_df)

# Alerts
st.subheader("🚨 Recent Alerts")

alerts = df[df['Predicted'] == 1].tail(5)

for i, row in alerts.iterrows():
    st.error(f"Attack Detected → {row['Explanation']}")
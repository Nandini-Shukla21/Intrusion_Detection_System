import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Intrusion Detection System", layout="wide")

st.title("🚨 Intelligent Intrusion Detection System")
st.markdown("### 🔐 AI-Powered Network Security Dashboard")

# -------------------- LOAD DATA --------------------
df = pd.read_csv("intrusion_logs.csv")

# -------------------- METRICS --------------------
total = len(df)
attacks = df[df['Predicted'] == 1].shape[0]
normal = df[df['Predicted'] == 0].shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Traffic", total)
col2.metric("✅ Normal Traffic", normal)
col3.metric("🚨 Attacks Detected", attacks)

st.markdown("---")

# -------------------- MODEL DETAILS --------------------
st.subheader("⚙️ Model Details")

st.markdown("""
- **Model Used:** Isolation Forest  
- **Training:** Only Normal Traffic  
- **Technique:** Anomaly Detection  
- **Feature Engineering:** Packet Rate, Byte Ratio, Traffic Intensity  
- **Goal:** Detect Zero-Day & Unknown Attacks  
""")

# -------------------- MODEL PERFORMANCE --------------------
st.subheader("🧠 Model Performance")

try:
    with open("metrics.json", "r") as f:
        report = json.load(f)

    cm = np.load("confusion_matrix.npy")

    st.write("### 📄 Classification Report")
    st.json(report)

    st.write("### 📊 Confusion Matrix")

    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)

except:
    st.warning("⚠️ Metrics files not found. Please run notebook to generate them.")

st.markdown("---")

# -------------------- ANOMALY SCORE --------------------
st.subheader("📉 Anomaly Score Distribution")
st.line_chart(df['Anomaly_Score'])

st.markdown("---")

# -------------------- FEATURE IMPORTANCE --------------------
st.subheader("📊 Feature Importance")

try:
    feat_df = pd.read_csv("feature_importance.csv")
    st.bar_chart(feat_df.head(10).set_index('Feature'))
except:
    st.warning("⚠️ Feature importance file not found.")

st.markdown("---")

# -------------------- FILTER --------------------
st.subheader("🔍 Filter Traffic")

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

# -------------------- TABLE --------------------
st.subheader("📋 Traffic Logs with Explanation")
st.dataframe(filtered_df)

st.markdown("---")

# -------------------- ALERTS --------------------
st.subheader("🚨 Recent Alerts")

alerts = df[df['Predicted'] == 1].tail(5)

for i, row in alerts.iterrows():
    st.error(f"⚠️ Attack Detected → {row['Explanation']}")

st.markdown("---")

# -------------------- DOWNLOAD --------------------
st.subheader("⬇️ Download Logs")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Intrusion Logs",
    data=csv,
    file_name='intrusion_logs.csv',
    mime='text/csv',
)
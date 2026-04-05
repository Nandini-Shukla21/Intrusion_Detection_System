import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- CONFIG --------------------
st.set_page_config(page_title="IDS Dashboard", layout="wide")

# -------------------- GLASSMORPHISM CSS --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}
h1, h2, h3 {
    color: white;
}
.metric {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🚨 Intelligent Intrusion Detection System")
st.caption("Real-Time AI-Based Network Threat Monitoring")

# -------------------- AUTO REFRESH --------------------
refresh_rate = st.sidebar.slider("⏱ Refresh Interval (sec)", 2, 10, 5)

# -------------------- LOAD DATA --------------------
@st.cache_data(ttl=refresh_rate)
def load_data():
    return pd.read_csv("intrusion_logs.csv")

df = load_data()

# -------------------- RISK SCORE --------------------
attack_ratio = (df['Predicted'] == 1).sum() / len(df)

if attack_ratio > 0.6:
    risk_level = "HIGH 🚨"
elif attack_ratio > 0.3:
    risk_level = "MEDIUM ⚠️"
else:
    risk_level = "LOW ✅"

# -------------------- METRICS --------------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='glass'>Total<br><span class='metric'>{len(df)}</span></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='glass'>Normal<br><span class='metric'>{(df['Predicted']==0).sum()}</span></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='glass'>Attacks<br><span class='metric'>{(df['Predicted']==1).sum()}</span></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='glass'>Risk Level<br><span class='metric'>{risk_level}</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- MAIN LAYOUT --------------------
left, right = st.columns([2, 1])

# -------------------- LEFT --------------------
with left:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📉 Anomaly Score Trend")
    st.line_chart(df['Anomaly_Score'], height=250)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📋 Traffic Logs")

    option = st.selectbox("Filter Traffic", ["All", "Normal", "Attack"])

    if option == "Normal":
        filtered_df = df[df['Predicted'] == 0]
    elif option == "Attack":
        filtered_df = df[df['Predicted'] == 1]
    else:
        filtered_df = df

    st.dataframe(filtered_df, height=300)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RIGHT --------------------
with right:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🧠 Model Info")

    st.markdown("""
    **Model:** Isolation Forest  
    **Approach:** Anomaly Detection  
    **Training:** Normal Traffic Only  
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------- SMALL CONFUSION MATRIX --------------------
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📊 Confusion Matrix")

    try:
        cm = np.load("confusion_matrix.npy")

        fig, ax = plt.subplots(figsize=(3,3))
        sns.heatmap(cm, annot=True, fmt="d", cmap="coolwarm", cbar=False, ax=ax)

        ax.set_xticklabels(["Normal", "Attack"])
        ax.set_yticklabels(["Normal", "Attack"])

        st.pyplot(fig)
    except:
        st.info("Run notebook to generate confusion matrix.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------- FEATURE IMPORTANCE --------------------
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📊 Top Features")

    try:
        feat_df = pd.read_csv("feature_importance.csv")
        st.bar_chart(feat_df.head(5).set_index('Feature'))
    except:
        st.info("Feature importance not available.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ALERTS --------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("🚨 Live Alerts")

alerts = df[df['Predicted'] == 1].tail(3)

for _, row in alerts.iterrows():
    st.warning(f"{row['Explanation']}")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- DOWNLOAD --------------------
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    "⬇️ Download Logs",
    df.to_csv(index=False),
    file_name="intrusion_logs.csv"
)

# -------------------- AUTO REFRESH LOOP --------------------
time.sleep(refresh_rate)
st.rerun()
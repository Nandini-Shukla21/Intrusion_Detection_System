# 🚨 Intelligent Intrusion Detection System (IDS)

### 🔐 AI-Powered Network Threat Detection with Explainable Intelligence

---

## 📌 Overview

This project presents an **Intelligent Intrusion Detection System (IDS)** built using Machine Learning and Anomaly Detection techniques.  

It is designed to detect **known and unknown (zero-day) cyber attacks** by analyzing network traffic patterns and identifying anomalies.

The system goes beyond basic classification by integrating:
- **Explainable AI**
- **Pattern Analysis**
- **Real-time Monitoring Dashboard**

---

## 🎯 Key Features

### 🧠 Intelligent Detection
- Uses **Isolation Forest** for anomaly detection  
- Trained only on **normal traffic** to detect unknown attacks  

### 📊 Feature Engineering
- Packet Rate Analysis  
- Byte Ratio Analysis  
- Traffic Intensity  
- Error Pattern Detection  

### 🚨 Explainable AI
- Provides **human-readable explanations** for detected attacks  
- Example:
  > High packet rate + error spikes → **HIGH RISK 🚨**

### 📉 Model Performance
- Accuracy: **~84%**  
- Strong recall for attack detection  
- Includes **confusion matrix & classification report**

### 💎 Premium Dashboard (Streamlit)
- Real-time monitoring  
- Glassmorphism UI  
- Risk level indicator  
- Live alerts  
- Feature importance visualization  

### ⚡ Real-Time Simulation
- Auto-refreshing dashboard  
- Simulates live intrusion detection system  

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **Matplotlib, Seaborn**
- **Streamlit (Frontend Dashboard)**

---

## 📂 Project Structure
├── app.py # Streamlit Dashboard
├── intrusion_logs.csv # Model Output Data
├── metrics.json # Classification Report
├── confusion_matrix.npy # Confusion Matrix
├── feature_importance.csv # Feature Importance
├── intrusion detection.ipynb # Model Development
└── README.md


---

## ⚙️ Installation

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit

streamlit run app.py
"""
ResistNet - Streamlit Dashboard
Interactive AMR surveillance dashboard connected to FastAPI backend.
"""

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="ResistNet - AMR Dashboard",
    page_icon="🦠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🦠 ResistNet")
st.sidebar.markdown("---")
st.sidebar.markdown("### AMR Early Warning System")
st.sidebar.markdown("*Antimicrobial Resistance Surveillance*")
st.sidebar.markdown("---")

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")

# ============================================================
# DATA FETCHING
# ============================================================

@st.cache_data(ttl=60)
def fetch_stats():
    try:
        resp = requests.get(f"{API_URL}/api/stats", timeout=5)
        return resp.json()
    except:
        return None

@st.cache_data(ttl=60)
def fetch_districts():
    try:
        resp = requests.get(f"{API_URL}/api/districts", timeout=5)
        return resp.json()
    except:
        return {"districts": []}

@st.cache_data(ttl=60)
def fetch_predictions(district=None, severity=None):
    try:
        params = {"limit": 50}
        if district:
            params["district"] = district
        if severity:
            params["severity"] = severity
        resp = requests.get(f"{API_URL}/api/predictions", params=params, timeout=5)
        return resp.json()
    except:
        return {"predictions": []}

@st.cache_data(ttl=60)
def fetch_alerts(severity=None):
    try:
        params = {"limit": 20}
        if severity:
            params["severity"] = severity
        resp = requests.get(f"{API_URL}/api/alerts", params=params, timeout=5)
        return resp.json()
    except:
        return {"alerts": []}

# ============================================================
# MAIN PAGE
# ============================================================

st.title("ResistNet — AMR Early Warning Dashboard")
st.markdown("---")

# Fetch data
stats = fetch_stats()

# ---- TOP METRICS ROW ----
if stats:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Districts", stats.get("total_districts", 0))
    with col2:
        st.metric("🦠 Avg Resistance", f"{stats.get('average_resistance', 0)}%")
    with col3:
        st.metric("🔴 Red Alerts", stats.get("red_alerts", 0))
    with col4:
        st.metric("🟠 Orange Alerts", stats.get("orange_alerts", 0))
    with col5:
        top = stats.get("top_risk_district", {})
        st.metric("⚠️ Highest Risk", top.get("name", "N/A"))
else:
    st.warning("⚠️ Cannot connect to API. Make sure FastAPI is running on port 8000.")

st.markdown("---")

# ---- PREDICTIONS TABLE ----
st.subheader("🔮 Latest AMR Predictions")

col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    severity_filter = st.selectbox("Severity", ["All", "RED", "ORANGE", "YELLOW", "GREEN"])
with col_filter2:
    districts_data = fetch_districts()
    district_list = ["All"] + [d["district_name"] for d in districts_data.get("districts", [])]
    district_filter = st.selectbox("District", district_list)

preds = fetch_predictions(
    district=None if district_filter == "All" else district_filter,
    severity=None if severity_filter == "All" else severity_filter
)

if preds and preds["predictions"]:
    df_preds = pd.DataFrame(preds["predictions"])
    
    # Color code severity
    def color_severity(val):
        colors = {"RED": "🔴", "ORANGE": "🟠", "YELLOW": "🟡", "GREEN": "🟢"}
        return colors.get(val, "⚪")
    
    df_preds["Severity"] = df_preds["severity"].apply(color_severity)
    
    st.dataframe(
        df_preds[["Severity", "district_name", "state_name", "pathogen_name", 
                   "antibiotic_name", "predicted_resistance", "quarter"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No predictions found. Populate the database first.")

st.markdown("---")

# ---- CHARTS ROW ----
st.subheader("📈 Resistance Analysis")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Top High-Risk Districts**")
    if preds and preds["predictions"]:
        df_chart = df_preds.groupby("district_name")["predicted_resistance"].mean().sort_values(ascending=True).tail(10)
        fig1 = px.bar(
            x=df_chart.values, y=df_chart.index,
            orientation='h',
            color=df_chart.values,
            color_continuous_scale="Reds",
            labels={"x": "Avg Resistance (%)", "y": ""}
        )
        fig1.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.markdown("**Resistance by Pathogen**")
    if preds and preds["predictions"]:
        df_pathogen = df_preds.groupby("pathogen_name")["predicted_resistance"].mean().sort_values()
        fig2 = px.bar(
            x=df_pathogen.values, y=df_pathogen.index,
            orientation='h',
            color=df_pathogen.values,
            color_continuous_scale="Oranges",
            labels={"x": "Avg Resistance (%)", "y": ""}
        )
        fig2.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---- ALERTS PANEL ----
st.subheader("🚨 Recent Alerts")

alert_filter = st.radio("Filter by:", ["All", "RED", "ORANGE"], horizontal=True)
alerts = fetch_alerts(severity=None if alert_filter == "All" else alert_filter)

if alerts and alerts["alerts"]:
    for alert in alerts["alerts"][:5]:
        severity_colors = {
            "RED": "🔴", "ORANGE": "🟠", "YELLOW": "🟡", "GREEN": "🟢"
        }
        emoji = severity_colors.get(alert.get("severity", ""), "⚪")
        
        with st.expander(f"{emoji} {alert.get('district_name', 'Unknown')} — {alert.get('severity', 'N/A')} Risk"):
            st.markdown(alert.get("alert_text", "No details available"))
            st.caption(f"Generated: {alert.get('created_at', 'N/A')}")
else:
    st.info("No alerts generated yet.")

# ---- FOOTER ----
st.markdown("---")
st.caption("ResistNet v1.0 | AMR Early Warning System | Built with ❤️ for India")
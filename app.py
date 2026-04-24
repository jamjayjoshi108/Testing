# app.py

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------
st.set_page_config(
    page_title="Utility Operations Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------
def load_css(file_name: str):
    """Injects custom CSS securely into the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Cannot find '{file_name}'. Ensure it's in the same directory.")

def load_lottieurl(url: str):
    """Fetches a Lottie animation JSON from a given URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# -----------------------------------------
# NAVIGATION LOGIC
# -----------------------------------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Homepage"

def navigate(page_name):
    """Updates session state to route to a new page."""
    st.session_state.current_page = page_name

# -----------------------------------------
# VIEW FUNCTIONS
# -----------------------------------------
def render_homepage(lottie_anim):
    """Renders the main grid menu based on the wireframe."""
    
    # Hero Section
    col_anim, col_text = st.columns([1, 3], gap="large")
    with col_anim:
        if lottie_anim:
            st_lottie(lottie_anim, height=180, key="hero_animation")
    with col_text:
        st.markdown("<h1>⚡ Utility Operations Command Center</h1>", unsafe_allow_html=True)
        st.write("Select an operational module below to access real-time dashboards and management tools.")

    st.markdown("---")

    # The 6 Grid Buttons (3x2 Layout for Elite UI)
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        if st.button("🛠️ PTW, LM-ALM Application", use_container_width=True):
            navigate("PTW_LM_ALM")
            st.rerun()
        if st.button("📡 Smart Meter", use_container_width=True):
            navigate("Smart_Meter")
            st.rerun()
            
    with col2:
        if st.button("📉 Outage Reduction Plan (ORP)", use_container_width=True):
            navigate("ORP")
            st.rerun()
        if st.button("🔌 New Connections", use_container_width=True):
            navigate("New_Connections")
            st.rerun()
            
    with col3:
        if st.button("🏢 RDSS", use_container_width=True):
            navigate("RDSS")
            st.rerun()
        if st.button("🚨 Outage Monitoring", use_container_width=True):
            navigate("Outage_Monitoring")
            st.rerun()

def render_subpage(title, description, metric_label, metric_val, chart_title):
    """A dynamic template for the individual module pages."""
    
    # Navigation Back Button
    if st.button("← Return to Homepage", use_container_width=False):
        navigate("Homepage")
        st.rerun()
        
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    st.write(description)
    
    # Trigger a visually pleasing toast notification on load
    st.toast(f"{title} data streams connected.", icon="✅")

    # Metrics Layout
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric(label=metric_label, value=metric_val, delta="↑ 4.2%")
    col_m2.metric(label="System Uptime", value="99.9%", delta="Stable", delta_color="off")
    col_m3.metric(label="Pending Alerts", value="3", delta="-2", delta_color="inverse")
    
    # Dynamic Plotly Visualization
    st.markdown("### Real-Time Telemetry")
    
    # Generate dummy data
    time_series = pd.date_range("2026-04-20", periods=20, freq="H")
    data = pd.DataFrame({
        "Time": time_series,
        "Value": np.random.normal(100, 15, 20).cumsum()
    })
    
    # Elite Plotly Chart
    fig = px.area(
        data, x="Time", y="Value", 
        title=chart_title,
        color_discrete_sequence=["#5bc0be"]
    )
    
    # Transparent background to blend with CSS
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------
# MAIN EXECUTION
# -----------------------------------------
load_css("style.css")

# Load a relevant abstract/tech lottie animation (Placeholder URL)
LOTTIE_URL = "https://assets2.lottiefiles.com/packages/lf20_1yzdv8qx.json" 
anim = load_lottieurl(LOTTIE_URL)

# Route to the correct view based on session state
if st.session_state.current_page == "Homepage":
    render_homepage(anim)
elif st.session_state.current_page == "PTW_LM_ALM":
    render_subpage("🛠️ PTW, LM-ALM Application", "Permit to Work and Asset Lifecycle Management operations.", "Active Permits", "1,204", "Asset Utilization Index")
elif st.session_state.current_page == "ORP":
    render_subpage("📉 Outage Reduction Plan", "Monitoring and executing the ORP guidelines.", "Outage Incidents", "14", "Reduction Trend (MTBF)")
elif st.session_state.current_page == "RDSS":
    render_subpage("🏢 RDSS", "Revamped Distribution Sector Scheme analytics.", "Funds Disbursed", "₹420Cr", "Implementation Progress")
elif st.session_state.current_page == "Smart_Meter":
    render_subpage("📡 Smart Meter", "AMI (Advanced Metering Infrastructure) tracking.", "Meters Installed", "45,210", "Deployment Velocity")
elif st.session_state.current_page == "New_Connections":
    render_subpage("🔌 New Connections", "Processing pipeline for new utility requests.", "Pending Connections", "312", "Application Clearance Rate")
elif st.session_state.current_page == "Outage_Monitoring":
    render_subpage("🚨 Outage Monitoring", "Live tracking of grid disruptions and resolution status.", "Active Outages", "2", "Grid Stability Metric")
    

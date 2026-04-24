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

def render_orp_page():
    """Dedicated view for the Outage Reduction Plan (ORP) module."""
    
    # Navigation Back Button
    if st.button("← Return to Homepage", use_container_width=False):
        navigate("Homepage")
        st.rerun()
        
    st.markdown("<h2>📉 Outage Reduction Plan (ORP)</h2>", unsafe_allow_html=True)
    st.write("Regional progress tracking and execution metrics.")
    st.toast("ORP regional data loaded.", icon="✅")

    # 1. Define the Data from the User's Image
    orp_data = {
        "%age progress in ORP": [
            "Feeder deloading", 
            "DT Transformers New", 
            "DT Transformers Augmentation", 
            "66kV transformers deloaded"
        ],
        "South": [89, 98, 100, 60],
        "East": [82, 99, 100, 89],
        "North": [80, 100, 100, 75],
        "Border": [84, 95, 95, 83],
        "West": [79, 93, 100, 69],
        "Central": [93, 100, 100, 77]
    }
    df = pd.DataFrame(orp_data)
    numeric_cols = ["South", "East", "North", "Border", "West", "Central"]

    # 2. Custom Conditional Formatting Logic
    def color_coding(val):
        """Applies traffic-light color coding matching the provided image."""
        if isinstance(val, (int, float)):
            if val == 100:
                # Green for 100%
                return 'background-color: rgba(91, 192, 190, 0.4); color: #ffffff;'
            elif val >= 80:
                # Yellow for 80% - 99%
                return 'background-color: rgba(244, 208, 63, 0.4); color: #ffffff;'
            else:
                # Red for below 80%
                return 'background-color: rgba(231, 76, 60, 0.4); color: #ffffff;'
        return ''

    # Apply styles and format as percentages
    styled_df = df.style.map(color_coding, subset=numeric_cols).format(
        {col: "{:.0f}%" for col in numeric_cols}
    )

    st.markdown("### Progress till 25-Apr-26")
    
    # 3. Layout: Table on Top, Visuals Below
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 4. Elite Interactive Heatmap
    st.markdown("### Regional Heatmap Analysis")
    
    # Set the index so the Y-axis labels are the categories
    heatmap_df = df.set_index("%age progress in ORP")
    
    # Build Plotly Heatmap
    fig = px.imshow(
        heatmap_df,
        text_auto="%d%%", 
        aspect="auto",
        color_continuous_scale=[
            [0.0, "rgba(231, 76, 60, 0.8)"],   # Red
            [0.5, "rgba(244, 208, 63, 0.8)"],  # Yellow
            [1.0, "rgba(91, 192, 190, 0.8)"]   # Green
        ],
        zmin=60, zmax=100
    )
    
    # Apply glassmorphism styling to the chart
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=14),
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="", showgrid=False)
    )
    
    # Hide the color scale bar for a cleaner look since text is auto-applied
    fig.update_traces(showscale=False)
    
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
    render_orp_page() # <-- Call the new function here instead of render_subpage
elif st.session_state.current_page == "RDSS":
    render_subpage("🏢 RDSS", "Revamped Distribution Sector Scheme analytics.", "Funds Disbursed", "₹420Cr", "Implementation Progress")
elif st.session_state.current_page == "Smart_Meter":
    render_subpage("📡 Smart Meter", "AMI (Advanced Metering Infrastructure) tracking.", "Meters Installed", "45,210", "Deployment Velocity")
elif st.session_state.current_page == "New_Connections":
    render_subpage("🔌 New Connections", "Processing pipeline for new utility requests.", "Pending Connections", "312", "Application Clearance Rate")
elif st.session_state.current_page == "Outage_Monitoring":
    render_subpage("🚨 Outage Monitoring", "Live tracking of grid disruptions and resolution status.", "Active Outages", "2", "Grid Stability Metric")


# -----------------------------------------
# ARTIST MARK (Global Footer)
# -----------------------------------------
st.markdown("<div class='artist-mark'>Wrought with ❤️ by Jay Joshi</div>", unsafe_allow_html=True)

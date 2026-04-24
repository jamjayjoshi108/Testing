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
    page_title="Elite Interface",
    page_icon="✨",
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
    except Exception as e:
        return None

# -----------------------------------------
# INITIALIZATION & STATE
# -----------------------------------------
# 1. Load the customized UI theme
load_css("style.css")

# 2. Initialize interactive session state variables
if 'system_activated' not in st.session_state:
    st.session_state.system_activated = False

# 3. Fetch premium Lottie animation (Placeholder: Abstract Tech Sphere)
LOTTIE_URL = "https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json"
lottie_anim = load_lottieurl(LOTTIE_URL)

# -----------------------------------------
# MAIN LAYOUT
# -----------------------------------------
st.markdown("<h1>⚡ Advanced Operations Dashboard</h1>", unsafe_allow_html=True)

# Top Grid Layout
col_anim, col_text = st.columns([1, 2.5], gap="large")

with col_anim:
    if lottie_anim:
        st_lottie(lottie_anim, height=220, key="hero_animation")
    else:
        st.warning("Animation failed to load.")

with col_text:
    st.markdown("### Next-Generation Data Interaction")
    st.write(
        "Welcome to a fully customized Streamlit environment. By leveraging injected CSS, "
        "interactive state management, and high-performance charting, we break free from "
        "standard column layouts."
    )
    
    # Interactive trigger changing session state with a "Wow" factor
    if st.button("Initialize Core Systems"):
        st.session_state.system_activated = True
        st.toast("Core systems online. Data successfully mapped.", icon="🚀")
        st.balloons()

st.markdown("---")

# -----------------------------------------
# DYNAMIC TABS & DATA VISUALIZATION
# -----------------------------------------
tab_analytics, tab_config, tab_logs = st.tabs(["📊 Analytics Engine", "⚙️ Parameters", "📋 System Logs"])

with tab_analytics:
    if st.session_state.system_activated:
        # Generate dynamic dummy data
        df = pd.DataFrame(
            np.random.randn(100, 3),
            columns=["Alpha", "Beta", "Gamma"]
        )
        # Shift data to be strictly positive for better visual scaling
        df = df - df.min() + 1 
        
        # Advanced Plotly Visualization
        fig = px.scatter(
            df, 
            x="Alpha", 
            y="Beta", 
            size="Gamma", 
            color="Gamma",
            color_continuous_scale=px.colors.sequential.Tealgrn,
            title="Multidimensional Cluster Analysis"
        )
        
        # Transparent background to inherit our CSS gradient
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Collapsible detailed view
        with st.expander("🔍 Inspect Raw Data Matrices"):
            col_data1, col_data2 = st.columns(2)
            with col_data1:
                st.dataframe(df.head(10).style.background_gradient(cmap='Teal', axis=0))
            with col_data2:
                st.metric(label="System Efficiency", value="98.4%", delta="2.1%")
                st.metric(label="Data Throughput", value="1.2 GB/s", delta="0.4 GB/s")
                
    else:
        # Guidance state before activation
        st.info("👈 System is currently idle. Click 'Initialize Core Systems' above to generate visualizations.")

with tab_config:
    st.subheader("Global Settings")
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        st.slider("Render Resolution (px)", min_value=720, max_value=2160, value=1080, step=100)
        st.toggle("Enable Hardware Acceleration", value=True)
    with col_set2:
        st.selectbox("Data Stream Protocol", ["WebSocket", "REST API", "GraphQL via Polling"])

with tab_logs:
    st.code("""
    [STATUS] Boot sequence initiated...
    [SUCCESS] CSS stylesheet successfully injected.
    [SUCCESS] Lottie assets retrieved from CDN.
    [WAITING] Awaiting user prompt for system activation...
    """, language="bash")

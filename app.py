import streamlit as st

st.set_page_config(
    page_title="Utility Operations Command Center",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        height: 100%;
        overflow: hidden;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* Lock entire app to viewport — no scroll */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2347 40%, #0a1f3f 100%);
        height: 100vh;
        overflow: hidden;
    }

    /* Remove default streamlit block padding */
    .block-container {
        padding: 0 2rem !important;
        max-width: 100% !important;
        height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Hero section — compact */
    .hero {
        text-align: center;
        padding: 18px 20px 6px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 180, 255, 0.15);
        border: 1px solid rgba(0, 180, 255, 0.4);
        color: #00b4ff;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 8px;
    }
    .hero h1 {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 4px;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero h1 span {
        background: linear-gradient(90deg, #00b4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,180,255,0.4), transparent);
        margin: 6px 40px 10px;
    }

    /* Section label */
    .section-label {
        color: #3d6a8a;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Module cards — compact height */
    .module-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 18px 16px 28px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }
    .module-card:hover {
        border-color: rgba(0, 180, 255, 0.5);
        background: linear-gradient(145deg, rgba(0,180,255,0.1), rgba(0,114,255,0.05));
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 114, 255, 0.2);
    }
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 6px rgba(0,180,255,0.5));
    }
    .card-title {
        color: #e0eaf5;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 4px;
        letter-spacing: 0.2px;
    }
    .card-arrow {
        position: absolute;
        bottom: 10px; right: 14px;
        color: rgba(0,180,255,0.4);
        font-size: 0.85rem;
        transition: all 0.3s;
    }
    .module-card:hover .card-arrow {
        color: #00b4ff;
        transform: translateX(3px);
    }

    /* Hide the streamlit buttons visually but keep them functional */
    .stButton > button {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 0px !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 0 !important;
        font-size: 0 !important;
        cursor: pointer !important;
        position: relative;
        top: -134px;
        width: 100%;
        z-index: 10;
    }
    .stButton > button:hover {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #2d4a62;
        font-size: 0.72rem;
        padding: 8px 20px 12px;
        letter-spacing: 0.3px;
    }

    /* Remove gap between streamlit column elements */
    [data-testid="column"] {
        padding: 0 8px !important;
    }
    [data-testid="stVerticalBlock"] > div {
        gap: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Live Operations</div>
    <h1>Utility Operations <span>Command Center</span></h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Module Data ───────────────────────────────────────────────────────────────
modules = [
    {"icon": "🔐", "title": "PTW, LM-ALM Application",    "color": "#00b4ff", "key": "ptw"},
    {"icon": "📉", "title": "Outage Reduction Plan (ORP)", "color": "#ff6b35", "key": "orp"},
    {"icon": "🛡️", "title": "RDSS",                        "color": "#7c4dff", "key": "rdss"},
    {"icon": "📟", "title": "Smart Meter",                  "color": "#00e676", "key": "smart_meter"},
    {"icon": "🔌", "title": "New Connections",              "color": "#ffca28", "key": "new_conn"},
    {"icon": "⚠️", "title": "Outage Monitoring",            "color": "#ff4081", "key": "outage_mon"},
]

# ── Section Label ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Operational Modules</div>', unsafe_allow_html=True)

# ── Cards Grid ────────────────────────────────────────────────────────────────
cols1 = st.columns(3, gap="medium")
cols2 = st.columns(3, gap="medium")

for i, (col, mod) in enumerate(zip(cols1 + cols2, modules)):
    with col:
        st.markdown(f"""
        <div class="module-card">
            <div class="card-icon">{mod['icon']}</div>
            <div class="card-title">{mod['title']}</div>
            <div class="card-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open {mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Wrought with ❤️ by Jay Joshi
</div>
""", unsafe_allow_html=True)

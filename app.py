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
        margin: 0; padding: 0;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2347 40%, #0a1f3f 100%);
        height: 100vh;
        overflow: hidden;
    }

    /* Make the main block fill full height with flex column */
    .block-container {
        padding: 0 3rem !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Remove excess gaps from streamlit internals */
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        height: 100%;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: 0 20px 12px;
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
        padding: 50px 16px;
        border-radius: 20px;
        margin-bottom: 10px;
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0px;
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
        margin: 10px 40px 16px;
    }

    /* Section label */
    .section-label {
        color: #3d6a8a;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 14px;
    }

    /* Cards — tall and spacious */
    .module-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 26vh;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }
    .module-card:hover {
        border-color: rgba(0, 180, 255, 0.55);
        background: linear-gradient(145deg, rgba(0,180,255,0.1), rgba(0,114,255,0.05));
        transform: translateY(-4px);
        box-shadow: 0 14px 40px rgba(0, 114, 255, 0.25);
    }
    .card-icon {
        font-size: 2.6rem;
        margin-bottom: 14px;
        filter: drop-shadow(0 0 8px rgba(0,180,255,0.5));
    }
    .card-title {
        color: #e0eaf5;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.2px;
        padding: 0 12px;
    }
    .card-arrow {
        position: absolute;
        bottom: 12px; right: 16px;
        color: rgba(0,180,255,0.35);
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    .module-card:hover .card-arrow {
        color: #00b4ff;
        transform: translateX(3px);
    }

    /* Invisible Streamlit buttons overlaid on cards */
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
        top: -26vh;
        width: 100%;
        z-index: 10;
    }
    .stButton > button:hover {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Column padding */
    [data-testid="column"] {
        padding: 0 10px !important;
    }

    /* Row gap between two card rows */
    .row-gap {
        height: 16px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #2d4a62;
        font-size: 0.72rem;
        padding: 14px 20px 0;
        letter-spacing: 0.3px;
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

# ── Modules ───────────────────────────────────────────────────────────────────
modules = [
    {"icon": "🔐", "title": "PTW, LM-ALM Application",    "key": "ptw"},
    {"icon": "📉", "title": "Outage Reduction Plan (ORP)", "key": "orp"},
    {"icon": "🛡️", "title": "RDSS",                        "key": "rdss"},
    {"icon": "📟", "title": "Smart Meter",                  "key": "smart_meter"},
    {"icon": "🔌", "title": "New Connections",              "key": "new_conn"},
    {"icon": "⚠️", "title": "Outage Monitoring",            "key": "outage_mon"},
]

st.markdown('<div class="section-label">Operational Modules</div>', unsafe_allow_html=True)

cols1 = st.columns(3, gap="medium")
cols2 = st.columns(3, gap="medium")

for col, mod in zip(cols1, modules[:3]):
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

st.markdown('<div class="row-gap"></div>', unsafe_allow_html=True)

for col, mod in zip(cols2, modules[3:]):
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
<div class="footer">Wrought with ❤️ by Jay Joshi</div>
""", unsafe_allow_html=True)

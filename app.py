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
    }

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2347 40%, #0a1f3f 100%);
        min-height: 100vh;
    }

    .block-container {
        padding-top: clamp(10px, 2vh, 30px) !important;
        padding-bottom: clamp(10px, 2vh, 20px) !important;
        padding-left: clamp(16px, 3vw, 48px) !important;
        padding-right: clamp(16px, 3vw, 48px) !important;
        max-width: 100% !important;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: clamp(8px, 1.5vh, 24px) 20px clamp(4px, 0.8vh, 12px);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 180, 255, 0.15);
        border: 1px solid rgba(0, 180, 255, 0.4);
        color: #00b4ff;
        font-size: clamp(0.58rem, 0.9vw, 0.72rem);
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 20px;
        margin-bottom: clamp(6px, 1vh, 14px);
    }
    .hero h1 {
        font-size: clamp(1.5rem, 3.5vw, 2.8rem);
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero h1 span {
        background: linear-gradient(90deg, #00b4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,180,255,0.4), transparent);
        margin: clamp(6px, 1vh, 14px) 40px clamp(8px, 1.5vh, 20px);
    }

    .section-label {
        color: #3d6a8a;
        font-size: clamp(0.58rem, 0.9vw, 0.72rem);
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: clamp(8px, 1.5vh, 18px);
    }

    /* THE CARD — styled as a full Streamlit button */
    div[data-testid="column"] .stButton > button {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        width: 100% !important;
        height: clamp(140px, 22vh, 240px) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        padding: clamp(12px, 2vh, 28px) clamp(10px, 2vw, 20px) !important;
        margin-bottom: clamp(6px, 1vh, 14px) !important;
        backdrop-filter: blur(10px) !important;
        color: #e0eaf5 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.82rem, 1.3vw, 1rem) !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        white-space: normal !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        border-color: rgba(0, 180, 255, 0.55) !important;
        background: linear-gradient(145deg, rgba(0,180,255,0.12), rgba(0,114,255,0.06)) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 36px rgba(0, 114, 255, 0.22) !important;
        color: #ffffff !important;
    }
    div[data-testid="column"] .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
        border-color: rgba(0,180,255,0.4) !important;
    }

    [data-testid="column"] { padding: 0 clamp(4px, 0.6vw, 10px) !important; }

    .footer {
        text-align: center;
        color: #2d4a62;
        font-size: clamp(0.62rem, 0.9vw, 0.75rem);
        padding: clamp(6px, 1vh, 14px) 20px clamp(4px, 0.6vh, 8px);
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
st.markdown('<div class="section-label">Operational Modules</div>', unsafe_allow_html=True)

# ── Modules ───────────────────────────────────────────────────────────────────
modules = [
    {"icon": "🔐", "title": "PTW, LM-ALM Application",    "key": "ptw"},
    {"icon": "📉", "title": "Outage Reduction Plan (ORP)", "key": "orp"},
    {"icon": "🛡️", "title": "RDSS",                        "key": "rdss"},
    {"icon": "📟", "title": "Smart Meter",                  "key": "smart_meter"},
    {"icon": "🔌", "title": "New Connections",              "key": "new_conn"},
    {"icon": "⚠️", "title": "Outage Monitoring",            "key": "outage_mon"},
]

cols1 = st.columns(3, gap="medium")
cols2 = st.columns(3, gap="medium")

for col, mod in zip(cols1, modules[:3]):
    with col:
        if st.button(f"{mod['icon']}\n\n{mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

for col, mod in zip(cols2, modules[3:]):
    with col:
        if st.button(f"{mod['icon']}\n\n{mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

st.markdown('<div class="footer">Wrought with ❤️ by Jay Joshi</div>', unsafe_allow_html=True)

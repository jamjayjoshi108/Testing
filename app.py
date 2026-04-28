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

    /* Remove streamlit default padding */
    .block-container {
        padding-top: 2vh !important;
        padding-bottom: 2vh !important;
        padding-left: 3vw !important;
        padding-right: 3vw !important;
        max-width: 100% !important;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: clamp(10px, 2vh, 30px) 20px clamp(6px, 1vh, 20px);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 180, 255, 0.15);
        border: 1px solid rgba(0, 180, 255, 0.4);
        color: #00b4ff;
        font-size: clamp(0.6rem, 1vw, 0.75rem);
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 20px;
        margin-bottom: clamp(6px, 1vh, 16px);
    }
    .hero h1 {
        font-size: clamp(1.4rem, 4vw, 2.8rem);
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 clamp(4px, 0.8vh, 14px);
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
        margin: clamp(4px, 0.8vh, 10px) 40px clamp(8px, 1.5vh, 24px);
    }

    /* Section label */
    .section-label {
        color: #3d6a8a;
        font-size: clamp(0.6rem, 1vw, 0.72rem);
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: clamp(8px, 1.5vh, 20px);
    }

    /* Cards */
    .module-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: clamp(18px, 3vh, 36px) clamp(12px, 2vw, 24px);
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-height: clamp(120px, 18vh, 200px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
        margin-bottom: clamp(8px, 1.5vh, 16px);
    }
    .module-card:hover {
        border-color: rgba(0, 180, 255, 0.5);
        background: linear-gradient(145deg, rgba(0,180,255,0.1), rgba(0,114,255,0.05));
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 114, 255, 0.2);
    }
    .card-icon {
        font-size: clamp(1.6rem, 3vw, 2.4rem);
        margin-bottom: clamp(8px, 1.2vh, 14px);
        filter: drop-shadow(0 0 8px rgba(0,180,255,0.5));
    }
    .card-title {
        color: #e0eaf5;
        font-size: clamp(0.78rem, 1.4vw, 1rem);
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    .card-arrow {
        position: absolute;
        bottom: 12px; right: 16px;
        color: rgba(0,180,255,0.4);
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    .module-card:hover .card-arrow { color: #00b4ff; transform: translateX(3px); }

    /* Streamlit buttons styled to look like "Open" links */
    .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(0,180,255,0.2) !important;
        color: #3d6a8a !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 4px 0 !important;
        margin-top: 2px !important;
        width: 100% !important;
        transition: all 0.2s !important;
        letter-spacing: 0.5px;
    }
    .stButton > button:hover {
        border-color: #00b4ff !important;
        color: #00b4ff !important;
        background: rgba(0,180,255,0.05) !important;
    }

    /* Column spacing */
    [data-testid="column"] { padding: 0 clamp(4px, 0.5vw, 10px) !important; }

    /* Footer */
    .footer {
        text-align: center;
        color: #2d4a62;
        font-size: clamp(0.65rem, 1vw, 0.75rem);
        padding: clamp(8px, 1.5vh, 20px) 20px clamp(4px, 0.8vh, 10px);
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
        if st.button(f"Open →  {mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

for col, mod in zip(cols2, modules[3:]):
    with col:
        st.markdown(f"""
        <div class="module-card">
            <div class="card-icon">{mod['icon']}</div>
            <div class="card-title">{mod['title']}</div>
            <div class="card-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open →  {mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Wrought with ❤️ by Jay Joshi</div>', unsafe_allow_html=True)

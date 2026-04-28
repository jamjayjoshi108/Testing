import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Utility Operations Command Center",
    page_icon="⚡",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header {visibility: hidden;}

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2347 40%, #0a1f3f 100%);
        min-height: 100vh;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 50px 20px 30px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 180, 255, 0.15);
        border: 1px solid rgba(0, 180, 255, 0.4);
        color: #00b4ff;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 18px;
        border-radius: 20px;
        margin-bottom: 18px;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 14px;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero h1 span {
        background: linear-gradient(90deg, #00b4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #8daec8;
        font-size: 1.05rem;
        max-width: 560px;
        margin: 0 auto 10px;
        line-height: 1.7;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,180,255,0.4), transparent);
        margin: 10px 40px 40px;
    }

    /* Status bar */
    .status-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 40px;
        flex-wrap: wrap;
    }
    .status-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #8daec8;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #00e676;
        box-shadow: 0 0 6px #00e676;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* Module cards */
    .module-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 36px 24px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-height: 170px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }
    .module-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .module-card:hover {
        border-color: rgba(0, 180, 255, 0.5);
        background: linear-gradient(145deg, rgba(0,180,255,0.1), rgba(0,114,255,0.05));
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 114, 255, 0.2);
    }
    .card-icon {
        font-size: 2.2rem;
        margin-bottom: 14px;
        filter: drop-shadow(0 0 8px rgba(0,180,255,0.5));
    }
    .card-title {
        color: #e0eaf5;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 8px;
        letter-spacing: 0.2px;
    }
    .card-desc {
        color: #5a7a96;
        font-size: 0.78rem;
        line-height: 1.5;
    }
    .card-arrow {
        position: absolute;
        bottom: 14px; right: 18px;
        color: rgba(0,180,255,0.4);
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    .module-card:hover .card-arrow {
        color: #00b4ff;
        transform: translateX(3px);
    }

    /* Section label */
    .section-label {
        color: #3d6a8a;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 24px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #2d4a62;
        font-size: 0.75rem;
        padding: 40px 20px 20px;
        letter-spacing: 0.3px;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Live Operations</div>
    <h1>Utility Operations <span>Command Center</span></h1>
</div>
""", unsafe_allow_html=True)

# st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Module Data ───────────────────────────────────────────────────────────────
modules = [
    {
        "icon": "🔐",
        "title": "PTW, LM-ALM Application",
        "color": "#00b4ff",
        "key": "ptw",
    },
    {
        "icon": "📉",
        "title": "Outage Reduction Plan (ORP)",
        "color": "#ff6b35",
        "key": "orp",
    },
    {
        "icon": "🛡️",
        "title": "RDSS",
        "color": "#7c4dff",
        "key": "rdss",
    },
    {
        "icon": "📟",
        "title": "Smart Meter",
        "color": "#00e676",
        "key": "smart_meter",
    },
    {
        "icon": "🔌",
        "title": "New Connections",
        "color": "#ffca28",
        "key": "new_conn",
    },
    {
        "icon": "⚠️",
        "title": "Outage Monitoring",
        "color": "#ff4081",
        "key": "outage_mon",
    },
]

# ── Section Label ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Operational Modules</div>', unsafe_allow_html=True)

# ── Cards Grid ────────────────────────────────────────────────────────────────
cols1 = st.columns(3, gap="large")
cols2 = st.columns(3, gap="large")

all_cols = cols1 + cols2

for i, (col, mod) in enumerate(zip(all_cols, modules)):
    with col:
        st.markdown(f"""
        <div class="module-card" style="--accent:{mod['color']};">
            <div class="card-icon">{mod['icon']}</div>
            <div class="card-title">{mod['title']}</div>
            <div class="card-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
        # Actual Streamlit button (invisible trigger below each card)
        if st.button(f"Open {mod['title']}", key=mod['key'], use_container_width=True):
            st.toast(f"🚀 Opening {mod['title']}...", icon="⚡")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Wrought with ❤️ by Jay Joshi
</div>
""", unsafe_allow_html=True)

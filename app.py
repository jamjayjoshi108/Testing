import streamlit as st
import streamlit.components.v1 as components

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
        margin: 0; padding: 0;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: linear-gradient(145deg, #f8f9fb 0%, #eef1f7 50%, #f4f6fa 100%);
        min-height: 100vh;
    }

    .block-container {
        padding-top: clamp(10px, 2.5vh, 36px) !important;
        padding-bottom: clamp(10px, 2vh, 24px) !important;
        padding-left: clamp(16px, 4vw, 64px) !important;
        padding-right: clamp(16px, 4vw, 64px) !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] { display: none !important; }
    [   data-testid="collapsedControl"] { display: none !important; }
    /* ── Hero ── */
    .hero {
        text-align: center;
        padding: clamp(8px, 1.5vh, 20px) 20px clamp(4px, 0.8vh, 12px);
        animation: fadeSlideDown 0.7s ease both;
    }
    @keyframes fadeSlideDown {
        from { opacity: 0; transform: translateY(-24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .hero-badge {
        display: inline-block;
        background: rgba(0, 102, 204, 0.08);
        border: 1px solid rgba(0, 102, 204, 0.25);
        color: #0066cc;
        font-size: clamp(0.58rem, 0.85vw, 0.72rem);
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        padding: 5px 18px;
        border-radius: 20px;
        margin-bottom: clamp(6px, 1vh, 14px);
    }

    .hero h1 {
        font-size: clamp(1.6rem, 3.8vw, 3rem);
        font-weight: 800;
        color: #0d1f3c;
        margin: 0 0 clamp(2px, 0.5vh, 8px);
        letter-spacing: -0.5px;
        line-height: 1.15;
    }

    .hero h1 span {
        background: linear-gradient(90deg, #0066cc, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ── Divider ── */
    .divider {
        height: 1.5px;
        background: linear-gradient(90deg, transparent, rgba(0,102,204,0.3), transparent);
        margin: clamp(6px, 1vh, 14px) 60px clamp(8px, 1.5vh, 20px);
        animation: fadeSlideDown 0.9s ease both;
    }

    /* ── Section label ── */
    .section-label {
        color: #8a9ab5;
        font-size: clamp(0.58rem, 0.85vw, 0.7rem);
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: clamp(10px, 1.8vh, 22px);
        animation: fadeSlideDown 1s ease both;
    }

    /* ── Cards ── */
    .module-card {
        background: #ffffff;
        border: 1.5px solid rgba(0, 102, 204, 0.1);
        border-radius: 18px;
        padding: clamp(20px, 3.5vh, 48px) clamp(12px, 2vw, 24px);
        text-align: center;
        cursor: pointer;
        transition: all 0.32s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-height: clamp(130px, 20vh, 220px);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        margin-bottom: clamp(8px, 1.4vh, 18px);
        text-decoration: none;
    }

    .module-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0066cc, #0099ff, #00ccff);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.35s ease;
        border-radius: 18px 18px 0 0;
    }
    .module-card:hover::before { transform: scaleX(1); }

    .module-card:hover {
        border-color: rgba(0, 102, 204, 0.3);
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(0, 102, 204, 0.14);
    }

    .card-0 { animation: cardIn 0.5s ease 0.1s both; }
    .card-1 { animation: cardIn 0.5s ease 0.2s both; }
    .card-2 { animation: cardIn 0.5s ease 0.3s both; }
    .card-3 { animation: cardIn 0.5s ease 0.4s both; }
    .card-4 { animation: cardIn 0.5s ease 0.5s both; }
    .card-5 { animation: cardIn 0.5s ease 0.6s both; }

    @keyframes cardIn {
        from { opacity: 0; transform: translateY(20px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    .card-icon {
        font-size: clamp(2rem, 3.5vw, 2.8rem);
        margin-bottom: clamp(8px, 1.2vh, 16px);
        transition: transform 0.3s ease;
        filter: drop-shadow(0 2px 6px rgba(0,102,204,0.15));
    }
    .module-card:hover .card-icon { transform: scale(1.12) rotate(-4deg); }

    .card-title {
        color: #0d1f3c;
        font-size: clamp(0.82rem, 1.3vw, 1rem);
        font-weight: 700;
        letter-spacing: 0.1px;
        line-height: 1.4;
        padding: 0 8px;
    }

    .card-arrow {
        position: absolute;
        bottom: 12px; right: 16px;
        color: rgba(0, 102, 204, 0.25);
        font-size: 0.85rem;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .module-card:hover .card-arrow {
        color: #0066cc;
        transform: translateX(4px);
    }

    [data-testid="column"] { padding: 0 clamp(4px, 0.5vw, 10px) !important; }

    .footer {
        text-align: center;
        color: #b0bdd0;
        font-size: clamp(0.62rem, 0.85vw, 0.73rem);
        padding: clamp(6px, 1vh, 12px) 20px 4px;
        letter-spacing: 0.3px;
        animation: fadeSlideDown 1.2s ease both;
    }

    .pulse-dot {
        display: inline-block;
        width: 7px; height: 7px;
        background: #00cc66;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 0 0 rgba(0,204,102,0.4);
        animation: pulseAnim 2s infinite;
        vertical-align: middle;
    }
    @keyframes pulseAnim {
        0%   { box-shadow: 0 0 0 0 rgba(0,204,102,0.5); }
        70%  { box-shadow: 0 0 0 7px rgba(0,204,102,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,204,102,0); }
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge"><span class="pulse-dot"></span>Live Operations</div>
    <h1>Utility Operations <span>Command Center</span></h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Operational Modules</div>', unsafe_allow_html=True)

# ── Modules ───────────────────────────────────────────────────────────────────
modules = [
    {"icon": "📱", "title": "PTW Application",    "page": "ptw"},
    {"icon": "💡", "title": "Outage Reduction Plan (ORP)", "page": "orp"},
    {"icon": "🛡️", "title": "RDSS",                        "page": "rdss"},
    {"icon": "📟", "title": "Smart Meter",                  "page": "smart_meter"},
    {"icon": "🔌", "title": "New Connections",              "page": "new_conn"},
    {"icon": "🚨", "title": "Outage Monitoring",            "page": "outage_mon"},
]

cols1 = st.columns(3, gap="medium")
cols2 = st.columns(3, gap="medium")

for i, (col, mod) in enumerate(zip(cols1, modules[:3])):
    with col:
        st.markdown(f"""
        <a href="/{mod['page']}" target="_self" class="module-card card-{i}">
            <div class="card-icon">{mod['icon']}</div>
            <div class="card-title">{mod['title']}</div>
            <div class="card-arrow">→</div>
        </a>
        """, unsafe_allow_html=True)

for i, (col, mod) in enumerate(zip(cols2, modules[3:])):
    with col:
        st.markdown(f"""
        <a href="/{mod['page']}" target="_self" class="module-card card-{i+3}">
            <div class="card-icon">{mod['icon']}</div>
            <div class="card-title">{mod['title']}</div>
            <div class="card-arrow">→</div>
        </a>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Wrought with ❤️ by Jay Joshi</div>', unsafe_allow_html=True)

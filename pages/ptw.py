import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="PTW Tracker", layout="wide")

# ─────────────────────────────────────────────────────────────
# HIDE SIDEBAR + GLOBAL STYLES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"]       { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu, footer, header       { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #004481 0%, #0066cc 100%);
        border-radius: 6px;
        padding: 1.2rem 1.2rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        /* height: 100%;  ← REMOVE THIS, causes overlap */
        min-height: 130px;             /* consistent height without overflow */
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        border: 1px solid #003366;
        margin-bottom: 0;              /* let st.columns gap handle spacing */
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 16px rgba(0,68,129,0.2); }
    .kpi-title { color: #FFC107 !important; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem; }
    .kpi-value { color: #FFFFFF !important; font-weight: 700; font-size: 2.6rem; margin-bottom: 0; line-height: 1.1; }
    .kpi-subtext { color: #F8F9FA !important; font-size: 0.85rem; margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid rgba(255,255,255,0.2); display: flex; justify-content: flex-start; gap: 15px; }
    .status-badge { background-color: rgba(0,0,0,0.25); padding: 3px 8px; border-radius: 4px; font-weight: 500; color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# st.markdown("""
# <style>
#     .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
#     p, span, div, caption, .stMarkdown { color: #000000 !important; }
#     h1, h2, h3, h4, h5, h6 { color: #004085 !important; font-weight: 700 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
#     div.block-container h1 { text-align: center; border-bottom: 3px solid #004085 !important; padding-bottom: 10px; margin-bottom: 30px !important; font-size: 2.2rem !important; }
#     h2 { font-size: 1.3rem !important; border-bottom: 2px solid #004085 !important; padding-bottom: 5px; margin-bottom: 10px !important; }
#     h3 { font-size: 1.05rem !important; margin-bottom: 12px !important; text-transform: uppercase; letter-spacing: 0.5px; }
#     hr { border: 0; border-top: 1px solid #004085; margin: 1.5rem 0; opacity: 0.3; }

#     .kpi-card {
#         background: linear-gradient(135deg, #004481 0%, #0066cc 100%);
#         border-radius: 6px;
#         padding: 1.2rem 1.2rem;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#         height: 100%;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.08);
#         transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
#         border: 1px solid #003366;
#     }
#     .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 16px rgba(0,68,129,0.2); }
#     .kpi-title { color: #FFC107 !important; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem; }
#     .kpi-value { color: #FFFFFF !important; font-weight: 700; font-size: 2.6rem; margin-bottom: 0; line-height: 1.1; }
#     .kpi-subtext { color: #F8F9FA !important; font-size: 0.85rem; margin-top: 1rem; padding-top: 0.6rem; border-top: 1px solid rgba(255,255,255,0.2); display: flex; justify-content: flex-start; gap: 15px; }
#     .status-badge { background-color: rgba(0,0,0,0.25); padding: 3px 8px; border-radius: 4px; font-weight: 500; color: #FFFFFF !important; }

#     [data-testid="stDataFrame"] > div { border: 2px solid #004085 !important; border-radius: 6px; overflow: hidden; }

#     div[data-testid="stButton"] > button[kind="secondary"] {
#         background: #ffffff; border: 1.5px solid rgba(0,102,204,0.2); color: #0066cc;
#         font-size: 0.82rem; font-weight: 600; padding: 8px 20px; border-radius: 10px;
#         box-shadow: 0 2px 8px rgba(0,102,204,0.08); transition: all 0.2s ease;
#         font-family: 'Inter', sans-serif; margin-bottom: 16px;
#     }
#     div[data-testid="stButton"] > button[kind="secondary"]:hover {
#         background: #0066cc; color: #ffffff; border-color: #0066cc;
#         box-shadow: 0 4px 16px rgba(0,102,204,0.2);
#     }
# </style>
# """, unsafe_allow_html=True)

HEADER_STYLES = [
    {'selector': 'th',     'props': [('background-color','#004085 !important'),('color','#FFC107 !important'),('font-weight','bold !important'),('text-align','center !important')]},
    {'selector': 'th div', 'props': [('color','#FFC107 !important'),('font-weight','bold !important')]},
]

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
ZONES = ['Border', 'Central', 'North', 'South', 'East', 'West']
ZONE_TOTALS = {
    'Border': {'Total JEs': 419, 'PSPCL_G': 148, 'PSTCL_G': 38},
    'Central': {'Total JEs': 222, 'PSPCL_G': 92,  'PSTCL_G': 25},
    'North':   {'Total JEs': 273, 'PSPCL_G': 128, 'PSTCL_G': 34},
    'South':   {'Total JEs': 294, 'PSPCL_G': 219, 'PSTCL_G': 38},
    'East':    {'Total JEs': 134, 'PSPCL_G': 219, 'PSTCL_G': 38},
    'West':    {'Total JEs': 346, 'PSPCL_G': 256, 'PSTCL_G': 44},
}
SYSTEM_TOTAL_JES   = 1688
SYSTEM_TOTAL_GRIDS = 1022
S3_CSV_URL         = "https://pspcl-dashboard-data.s3.ap-south-1.amazonaws.com/ptw_requests.csv"

IST     = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(IST)

# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
# @st.cache_data(ttl=300)
# def load_csv_data():
#     df = pd.read_csv(S3_CSV_URL, low_memory=False, dtype={'ptw_id': 'str', 'permit_je': 'str', 'grid_code': 'str'})
#     df['start_time']    = pd.to_datetime(df['start_time'],    errors='coerce')
#     df['end_time']      = pd.to_datetime(df['end_time'],      errors='coerce')
#     df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')
#     df['duration_hrs']  = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600
#     df['zone_name']      = df['zone_name'].astype(str).str.replace(' Zone', '', case=False).str.strip().str.title()
#     df['grid_ownership'] = df['grid_ownership'].astype(str).str.strip().str.upper()
#     df['current_status'] = df['current_status'].astype(str).str.strip().str.title()
#     df['grid_type']      = df['grid_type'].astype(str).str.strip().str.title()
#     return df

@st.cache_data(ttl=300, show_spinner=False)   # ← disabling the ugly default
def load_csv_data():
    df = pd.read_csv(S3_CSV_URL, low_memory=False, dtype={'ptw_id': 'str', 'permit_je': 'str', 'grid_code': 'str'})
    df['start_time']    = pd.to_datetime(df['start_time'],    errors='coerce')
    df['end_time']      = pd.to_datetime(df['end_time'],      errors='coerce')
    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')
    df['duration_hrs']  = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600
    df['zone_name']      = df['zone_name'].astype(str).str.replace(' Zone', '', case=False).str.strip().str.title()
    df['grid_ownership'] = df['grid_ownership'].astype(str).str.strip().str.upper()
    df['current_status'] = df['current_status'].astype(str).str.strip().str.title()
    df['grid_type']      = df['grid_type'].astype(str).str.strip().str.title()
    return df

# ─────────────────────────────────────────────────────────────
# DATE SELECTOR
# ─────────────────────────────────────────────────────────────
def handle_period_change(tab_key):
    period = st.session_state[f"{tab_key}_radio"]
    today  = now_ist.date()
    if period == "Today":
        st.session_state[f"{tab_key}_start_date"] = today
        st.session_state[f"{tab_key}_end_date"]   = today
    elif period == "Current Month":
        st.session_state[f"{tab_key}_start_date"] = today.replace(day=1)
        st.session_state[f"{tab_key}_end_date"]   = today
    elif period == "Last Month":
        first = today.replace(day=1)
        last  = first - timedelta(days=1)
        st.session_state[f"{tab_key}_start_date"] = last.replace(day=1)
        st.session_state[f"{tab_key}_end_date"]   = last
    elif period == "Last 3 Months":
        st.session_state[f"{tab_key}_start_date"] = today - timedelta(days=90)
        st.session_state[f"{tab_key}_end_date"]   = today
    elif period == "Last 6 Months":
        st.session_state[f"{tab_key}_start_date"] = today - timedelta(days=180)
        st.session_state[f"{tab_key}_end_date"]   = today

def render_date_selector(tab_key):
    st.markdown("📅 **Select Time Period:**")
    if f"{tab_key}_start_date" not in st.session_state:
        st.session_state[f"{tab_key}_start_date"] = now_ist.date().replace(day=1)
        st.session_state[f"{tab_key}_end_date"]   = now_ist.date()

    period = st.radio(
        "Select Time Period",
        options=["Today", "Current Month", "Last Month", "Last 3 Months", "Last 6 Months", "Custom"],
        horizontal=True, label_visibility="collapsed",
        key=f"{tab_key}_radio", on_change=handle_period_change, args=(tab_key,)
    )
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date", format="DD/MM/YYYY", disabled=(period != "Custom"), key=f"{tab_key}_start_date")
    with col2:
        end_date   = st.date_input("To Date",   format="DD/MM/YYYY", disabled=(period != "Custom"), key=f"{tab_key}_end_date")
    return start_date, end_date

# ─────────────────────────────────────────────────────────────
# BACK BUTTON
# ─────────────────────────────────────────────────────────────
if st.button("← Back to Command Center"):
    st.switch_page("app.py")

# ─────────────────────────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────────────────────────
st.title("📱 PTW Tracker")

# full_df = load_csv_data()
# ── Custom Loading Screen ─────────────────────────────────────────────────────
loader = st.empty()

loader.markdown("""
<style>
    .loader-overlay {
        position: fixed; inset: 0;
        background: rgba(255,255,255,0.92);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .loader-title {
        color: #004085;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .loader-sub {
        color: #666;
        font-size: 0.88rem;
        margin-bottom: 1.8rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .loader-bar-track {
        width: 320px;
        height: 6px;
        background: #dce8f7;
        border-radius: 999px;
        overflow: hidden;
    }
    .loader-bar-fill {
        height: 100%;
        width: 40%;
        background: linear-gradient(90deg, #004481, #0066cc, #33aaff);
        border-radius: 999px;
        animation: slide 1.4s ease-in-out infinite;
        background-size: 200% 100%;
    }
    @keyframes slide {
        0%   { transform: translateX(-100%); }
        100% { transform: translateX(350%);  }
    }
</style>
<div class="loader-overlay">
    <div class="loader-title">⚡ PTW & LM-ALM Tracker</div>
    <div class="loader-sub">Fetching latest data from PSPCL database…</div>
    <div class="loader-bar-track">
        <div class="loader-bar-fill"></div>
    </div>
</div>
""", unsafe_allow_html=True)

full_df = load_csv_data()

loader.empty()   # ← NOW this works — clears the exact element it was written into

start_date, end_date = render_date_selector("ptw")
st.divider()

df = full_df[
    (full_df['start_time'].dt.date >= start_date) &
    (full_df['start_time'].dt.date <= end_date)
].copy()

if df.empty:
    st.warning(f"No data found for the selected period ({start_date} to {end_date}).")
    st.stop()

# ─────────────────────────────────────────────────────────────
# KPI SECTION — 3 columns, exactly like reference code
# ─────────────────────────────────────────────────────────────
total_ptws         = df['ptw_id'].nunique()
total_jes_active   = df['permit_je'].nunique()
total_grids_active = df['grid_code'].nunique()
je_adoption_rate   = total_jes_active / SYSTEM_TOTAL_JES
grid_adoption_rate = total_grids_active / SYSTEM_TOTAL_GRIDS
avg_duration       = df['duration_hrs'].dropna().mean()
avg_dur_str        = f"{avg_duration:.1f} hrs" if not pd.isna(avg_duration) else "N/A"

st.subheader(f"📊 Global Performance ({start_date.strftime('%d %b')} to {end_date.strftime('%d %b %Y')})")

kpi1, kpi2, kpi3 = st.columns(3)
st.write("")
with kpi1:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">Total PTWs Issued</div>'
        f'<div class="kpi-value">{total_ptws:,}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">📅 {start_date.strftime("%d %b")} – {end_date.strftime("%d %b %Y")}</span>'
        f'</div></div>', unsafe_allow_html=True
    )
with kpi2:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">JEs Using PTW</div>'
        f'<div class="kpi-value">{total_jes_active:,}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">📈 Adoption: {je_adoption_rate:.1%}</span>'
        f'</div></div>', unsafe_allow_html=True
    )
with kpi3:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">Grids Using PTW</div>'
        f'<div class="kpi-value">{total_grids_active:,}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">📡 Adoption: {grid_adoption_rate:.1%}</span>'
        f'</div></div>', unsafe_allow_html=True
    )

kpi4, kpi5, kpi6 = st.columns(3)
with kpi4:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">JE Adoption Rate</div>'
        f'<div class="kpi-value">{je_adoption_rate:.1%}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">👷 {total_jes_active} of {SYSTEM_TOTAL_JES} JEs</span>'
        f'</div></div>', unsafe_allow_html=True
    )
with kpi5:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">Grid Adoption Rate</div>'
        f'<div class="kpi-value">{grid_adoption_rate:.1%}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">🏭 {total_grids_active} of {SYSTEM_TOTAL_GRIDS} Grids</span>'
        f'</div></div>', unsafe_allow_html=True
    )
with kpi6:
    st.markdown(
        f'<div class="kpi-card"><div>'
        f'<div class="kpi-title">Avg PTW Duration</div>'
        f'<div class="kpi-value">{avg_dur_str}</div>'
        f'</div><div class="kpi-subtext">'
        f'<span class="status-badge">⏱️ Per Permit</span>'
        f'</div></div>', unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# PTW STATUS OVERVIEW
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("📋 PTW Status Overview")

status_counts = df['current_status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
status_counts['% Share'] = (status_counts['Count'] / status_counts['Count'].sum() * 100).map("{:.1f}%".format)

s1, s2 = st.columns([0.4, 0.6])
with s1:
    st.dataframe(status_counts.style.set_table_styles(HEADER_STYLES), hide_index=True, use_container_width=True)
with s2:
    grid_type_counts = (
        df.drop_duplicates('grid_code')[['grid_code', 'grid_type']]
        .value_counts('grid_type').reset_index()
    )
    grid_type_counts.columns = ['Grid Type', 'Unique Grids']
    st.markdown("**Grids by Type**")
    st.dataframe(grid_type_counts.style.set_table_styles(HEADER_STYLES), hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# CIRCLE / DIVISION DRILL-DOWN
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🔍 Circle & Division Drill-Down")

selected_zone = st.selectbox("Filter by Zone", options=["All"] + ZONES)
filtered = df if selected_zone == "All" else df[df['zone_name'] == selected_zone]

circle_df = (
    filtered.groupby(['zone_name', 'circle_name'])
    .agg(
        PTWs_Issued   = ('ptw_id',       'nunique'),
        JEs_Active    = ('permit_je',    'nunique'),
        Grids_Covered = ('grid_code',    'nunique'),
        Avg_Duration  = ('duration_hrs', 'mean'),
    )
    .reset_index()
    .rename(columns={'zone_name': 'Zone', 'circle_name': 'Circle'})
)
circle_df['Avg_Duration'] = circle_df['Avg_Duration'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
st.dataframe(circle_df.style.set_table_styles(HEADER_STYLES), hide_index=True, use_container_width=True)

if selected_zone != "All":
    selected_circle = st.selectbox(
        "Filter by Circle",
        options=["All"] + sorted(filtered['circle_name'].dropna().unique().tolist())
    )
    filtered_div = filtered if selected_circle == "All" else filtered[filtered['circle_name'] == selected_circle]

    div_df = (
        filtered_div.groupby(['circle_name', 'division_name'])
        .agg(
            PTWs_Issued   = ('ptw_id',       'nunique'),
            JEs_Active    = ('permit_je',    'nunique'),
            Grids_Covered = ('grid_code',    'nunique'),
            Avg_Duration  = ('duration_hrs', 'mean'),
        )
        .reset_index()
        .rename(columns={'circle_name': 'Circle', 'division_name': 'Division'})
    )
    div_df['Avg_Duration'] = div_df['Avg_Duration'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
    st.markdown("**Division-Level Breakdown**")
    st.dataframe(div_df.style.set_table_styles(HEADER_STYLES), hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# FEEDER ACTIVITY
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("⚡ Feeder Activity")

feeder_df = (
    df.groupby('feeders')
    .agg(
        PTWs    = ('ptw_id',       'nunique'),
        JEs     = ('permit_je',    'nunique'),
        Avg_Dur = ('duration_hrs', 'mean'),
    )
    .reset_index()
    .sort_values('PTWs', ascending=False)
    .head(20)
)
feeder_df['Avg_Dur'] = feeder_df['Avg_Dur'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
feeder_df.rename(columns={'feeders': 'Feeder', 'PTWs': 'PTWs Issued', 'JEs': 'JEs Active', 'Avg_Dur': 'Avg Duration'}, inplace=True)
st.caption("Top 20 Feeders by PTW Activity")
st.dataframe(feeder_df.style.set_table_styles(HEADER_STYLES), hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# REGIONAL BREAKDOWN
# ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🗺️ Regional Breakdown")

jes   = df.groupby('zone_name')['permit_je'].nunique().reindex(ZONES, fill_value=0)
grids = df.groupby('zone_name')['grid_code'].nunique().reindex(ZONES, fill_value=0)
pspcl = df[df['grid_ownership'] == 'PSPCL'].groupby('zone_name')['grid_code'].nunique().reindex(ZONES, fill_value=0)
pstcl = df[df['grid_ownership'] == 'PSTCL'].groupby('zone_name')['grid_code'].nunique().reindex(ZONES, fill_value=0)
ptws  = df.groupby('zone_name')['ptw_id'].nunique().reindex(ZONES, fill_value=0)
dur   = df.groupby('zone_name')['duration_hrs'].mean().reindex(ZONES)

data_dict = {
    "Metric": [
        "Total PTWs Issued",
        "JEs Using PTW",
        "Share: JEs Using PTW / Total JEs",
        "Grids Using PTW",
        "PSPCL Grids Using PTW",
        "PSTCL Grids Using PTW",
        "Share: PSPCL Grids / Total PSPCL",
        "Share: PSTCL Grids / Total PSTCL",
        "Avg PTW Duration (hrs)",
    ]
}

for z in ZONES:
    je_den    = ZONE_TOTALS[z]['Total JEs']
    je_share  = f"{(jes[z] / je_den):.1%}" if je_den > 0 else "0.0%"
    pspcl_den = ZONE_TOTALS[z]['PSPCL_G']
    pstcl_den = ZONE_TOTALS[z]['PSTCL_G']

    if z in ['South', 'East']:
        combined_pspcl = pspcl['South'] + pspcl['East']
        pspcl_share    = f"{(combined_pspcl / 219):.1%}"
        combined_pstcl = pstcl['South'] + pstcl['East']
        pstcl_share    = f"{(combined_pstcl / 38):.1%}"
    else:
        pspcl_share = f"{(pspcl[z] / pspcl_den):.1%}" if pspcl_den > 0 else "0.0%"
        pstcl_share = f"{(pstcl[z] / pstcl_den):.1%}" if pstcl_den > 0 else "0.0%"

    avg_d = f"{dur[z]:.1f}" if pd.notna(dur[z]) else "N/A"

    data_dict[z] = [
        int(ptws[z]), int(jes[z]), je_share,
        int(grids[z]), int(pspcl[z]), int(pstcl[z]),
        pspcl_share, pstcl_share, avg_d,
    ]

performance_df = pd.DataFrame(data_dict)

def apply_gradient(row):
    styles = [''] * len(row)
    if "Share" in str(row.iloc[0]):
        vals = []
        for val in row.iloc[1:]:
            try:    vals.append(float(str(val).strip('%')))
            except: vals.append(None)
        valid_vals = [v for v in vals if v is not None]
        if not valid_vals:
            return styles
        min_val, max_val = min(valid_vals), max(valid_vals)
        for i, val in enumerate(vals):
            if val is not None:
                norm = (val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                if norm < 0.5:
                    pct = norm / 0.5
                    r, g, b = int(248+(255-248)*pct), int(105+(235-105)*pct), int(107+(132-107)*pct)
                else:
                    pct = (norm-0.5)/0.5
                    r, g, b = int(255+(99-255)*pct), int(235+(195-235)*pct), int(132+(132-132)*pct)
                styles[i+1] = f'background-color:rgba({r},{g},{b},0.6);color:#000000;font-weight:500;'
    return styles

styled_df = performance_df.style.apply(apply_gradient, axis=1).set_table_styles(HEADER_STYLES)
st.dataframe(styled_df, hide_index=True, use_container_width=True)

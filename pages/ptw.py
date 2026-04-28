import streamlit as st
import pandas as pd

# --- CONSTANTS & MAPPINGS ---
ZONES = ['Border', 'Central', 'North', 'South', 'East', 'West']
ZONE_TOTALS = {
    'Border': {'Total JEs': 419, 'PSPCL_G': 148, 'PSTCL_G': 38},
    'Central': {'Total JEs': 222, 'PSPCL_G': 92, 'PSTCL_G': 25},
    'North': {'Total JEs': 273, 'PSPCL_G': 128, 'PSTCL_G': 34},
    'South': {'Total JEs': 294, 'PSPCL_G': 219, 'PSTCL_G': 38},
    'East': {'Total JEs': 134, 'PSPCL_G': 219, 'PSTCL_G': 38},
    'West': {'Total JEs': 346, 'PSPCL_G': 256, 'PSTCL_G': 44}
}
SYSTEM_TOTAL_JES = 1688
SYSTEM_TOTAL_GRIDS = 1022

# ── S3 CSV URL (public bucket) ────────────────────────────────────────────────
S3_CSV_URL = "https://pspcl-dashboard-data.s3.ap-south-1.amazonaws.com/ptw_requests.csv"

# ── CSV Format Expected ───────────────────────────────────────────────────────
# ptw_id, zone_name, circle_name, division_name, employee_subdivision,
# permit_no, permit_je, current_status, grid_code, grid_name, grid_type,
# grid_ownership, pm_circle, om_division, creation_date, start_time, end_time, feeders
#
# Date/Time format expected:  YYYY-MM-DD HH:MM:SS  (or YYYY-MM-DD for dates)

@st.cache_data(ttl=300)  # Auto-refresh every 5 minutes from S3
def load_csv_data():
    df = pd.read_csv(S3_CSV_URL)

    # Parse datetime columns
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
    df['end_time']   = pd.to_datetime(df['end_time'],   errors='coerce')
    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')

    # Compute PTW duration in hours
    df['duration_hrs'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600

    # Clean key columns
    df['zone_name']      = df['zone_name'].astype(str).str.replace(' Zone', '', case=False).str.strip().str.title()
    df['grid_ownership'] = df['grid_ownership'].astype(str).str.strip().str.upper()
    df['current_status'] = df['current_status'].astype(str).str.strip().str.title()
    df['grid_type']      = df['grid_type'].astype(str).str.strip().str.title()

    return df


def render_ptw_lm_dashboard():

    # ── Back Button ───────────────────────────────────────────────────────────
    st.markdown("""
    <style>
        .kpi-card {
            background: linear-gradient(135deg, #004481 0%, #0066cc 100%);
            border-radius: 6px;
            padding: 1rem 0.8rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            min-width: 0;
        }
        .kpi-title {
            color: #FFC107;
            font-weight: 600;
            font-size: 0.75rem;          /* slightly smaller label */
            text-transform: uppercase;
            margin-bottom: 0.3rem;
            line-height: 1.3;
        }
        .kpi-value {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 1.6rem;           /* reduced from 2.2rem */
            line-height: 1.2;
            white-space: nowrap;         /* prevent mid-number line breaks */
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
""", unsafe_allow_html=True)

    col_title, col_btn = st.columns([0.85, 0.15])
    with col_title:
        st.title("🛠️ PTW & LM-ALM Tracker")
    with col_btn:
        st.write("")
        if st.button("⬅️ Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    # ── Date Range Selection ──────────────────────────────────────────────────
    today = pd.to_datetime("today").date()

    if 'ptw_start' not in st.session_state:
        st.session_state.ptw_start = today.replace(day=1)
    if 'ptw_end' not in st.session_state:
        st.session_state.ptw_end = today

    st.write("---")
    st.markdown("**📅 Select Time Period**")

    btn_cols = st.columns(5)
    if btn_cols[0].button("Today", use_container_width=True):
        st.session_state.ptw_start = today
        st.session_state.ptw_end   = today
    if btn_cols[1].button("Current Month", use_container_width=True):
        st.session_state.ptw_start = today.replace(day=1)
        st.session_state.ptw_end   = today
    if btn_cols[2].button("Last Month", use_container_width=True):
        st.session_state.ptw_end   = today.replace(day=1) - pd.Timedelta(days=1)
        st.session_state.ptw_start = st.session_state.ptw_end.replace(day=1)
    if btn_cols[3].button("Last 3 Months", use_container_width=True):
        st.session_state.ptw_start = (today - pd.DateOffset(months=3)).date()
        st.session_state.ptw_end   = today
    if btn_cols[4].button("Last 6 Months", use_container_width=True):
        st.session_state.ptw_start = (today - pd.DateOffset(months=6)).date()
        st.session_state.ptw_end   = today

    c1, c2 = st.columns(2)
    with c1: start_date = st.date_input("From Date", key="ptw_start")
    with c2: end_date   = st.date_input("To Date",   key="ptw_end")

    # ── Load & Filter Data ────────────────────────────────────────────────────
    full_df = load_csv_data()
    df = full_df[
        (full_df['start_time'].dt.date >= start_date) &
        (full_df['start_time'].dt.date <= end_date)
    ].copy()

    if df.empty:
        st.warning(f"No data found for the selected period ({start_date} to {end_date}).")
        return

    # ── KPI Section ───────────────────────────────────────────────────────────
    total_jes_active   = df['permit_je'].nunique()
    total_grids_active = df['grid_code'].nunique()
    je_adoption_rate   = total_jes_active / SYSTEM_TOTAL_JES
    grid_adoption_rate = total_grids_active / SYSTEM_TOTAL_GRIDS
    total_ptws         = df['ptw_id'].nunique()
    avg_duration       = df['duration_hrs'].dropna().mean()

    st.write("---")
    st.subheader(f"📊 Global Performance ({start_date.strftime('%d %b')} to {end_date.strftime('%d %b %Y')})")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpis = [
        (k1, "Total PTWs Issued",        f"{total_ptws:,}"),
        (k2, "JEs Using PTW",            f"{total_jes_active}"),
        (k3, "JE Adoption Rate",         f"{je_adoption_rate:.1%}"),
        (k4, "Grids Using PTW",          f"{total_grids_active}"),
        (k5, "Grid Adoption Rate",       f"{grid_adoption_rate:.1%}"),
        (k6, "Avg PTW Duration (hrs)",   f"{avg_duration:.1f}" if not pd.isna(avg_duration) else "N/A"),
    ]
    for col, title, value in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-title">{title}</div>'
                f'<div class="kpi-value">{value}</div></div>',
                unsafe_allow_html=True
            )

    # ── PTW Status Breakdown ──────────────────────────────────────────────────
    st.write("---")
    st.subheader("📋 PTW Status Overview")

    status_counts = df['current_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    status_counts['% Share'] = (status_counts['Count'] / status_counts['Count'].sum() * 100).map("{:.1f}%".format)

    s1, s2 = st.columns([0.4, 0.6])
    with s1:
        st.dataframe(status_counts, hide_index=True, use_container_width=True)
    with s2:
        # Grid Type split
        grid_type_counts = df.drop_duplicates('grid_code')[['grid_code', 'grid_type']].value_counts('grid_type').reset_index()
        grid_type_counts.columns = ['Grid Type', 'Unique Grids']
        st.markdown("**Grids by Type**")
        st.dataframe(grid_type_counts, hide_index=True, use_container_width=True)

    # ── Circle / Division Drill-Down ──────────────────────────────────────────
    st.write("---")
    st.subheader("🔍 Circle & Division Drill-Down")

    selected_zone = st.selectbox("Filter by Zone", options=["All"] + ZONES)
    filtered = df if selected_zone == "All" else df[df['zone_name'] == selected_zone]

    circle_df = (
        filtered.groupby(['zone_name', 'circle_name'])
        .agg(
            PTWs_Issued   = ('ptw_id',      'nunique'),
            JEs_Active    = ('permit_je',   'nunique'),
            Grids_Covered = ('grid_code',   'nunique'),
            Avg_Duration  = ('duration_hrs','mean'),
        )
        .reset_index()
        .rename(columns={'zone_name':'Zone','circle_name':'Circle'})
    )
    circle_df['Avg_Duration'] = circle_df['Avg_Duration'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
    st.dataframe(circle_df, hide_index=True, use_container_width=True)

    # Division breakdown within selected circle
    if selected_zone != "All":
        selected_circle = st.selectbox("Filter by Circle", options=["All"] + sorted(filtered['circle_name'].dropna().unique().tolist()))
        filtered_div = filtered if selected_circle == "All" else filtered[filtered['circle_name'] == selected_circle]

        div_df = (
            filtered_div.groupby(['circle_name', 'division_name'])
            .agg(
                PTWs_Issued   = ('ptw_id',      'nunique'),
                JEs_Active    = ('permit_je',   'nunique'),
                Grids_Covered = ('grid_code',   'nunique'),
                Avg_Duration  = ('duration_hrs','mean'),
            )
            .reset_index()
            .rename(columns={'circle_name':'Circle','division_name':'Division'})
        )
        div_df['Avg_Duration'] = div_df['Avg_Duration'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
        st.markdown("**Division-Level Breakdown**")
        st.dataframe(div_df, hide_index=True, use_container_width=True)

    # ── Feeder Activity ───────────────────────────────────────────────────────
    st.write("---")
    st.subheader("⚡ Feeder Activity")

    feeder_df = (
        df.groupby('feeders')
        .agg(
            PTWs      = ('ptw_id',    'nunique'),
            JEs       = ('permit_je', 'nunique'),
            Avg_Dur   = ('duration_hrs', 'mean'),
        )
        .reset_index()
        .sort_values('PTWs', ascending=False)
        .head(20)
    )
    feeder_df['Avg_Dur'] = feeder_df['Avg_Dur'].map(lambda x: f"{x:.1f} hrs" if pd.notna(x) else "N/A")
    feeder_df.rename(columns={'feeders':'Feeder','PTWs':'PTWs Issued','JEs':'JEs Active','Avg_Dur':'Avg Duration'}, inplace=True)
    st.caption("Top 20 Feeders by PTW Activity")
    st.dataframe(feeder_df, hide_index=True, use_container_width=True)

    # ── Regional Breakdown Table ──────────────────────────────────────────────
    st.write("---")
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
        je_den     = ZONE_TOTALS[z]['Total JEs']
        je_share   = f"{(jes[z] / je_den):.1%}" if je_den > 0 else "0.0%"
        pspcl_den  = ZONE_TOTALS[z]['PSPCL_G']
        pstcl_den  = ZONE_TOTALS[z]['PSTCL_G']

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
            int(ptws[z]),
            int(jes[z]),
            je_share,
            int(grids[z]),
            int(pspcl[z]),
            int(pstcl[z]),
            pspcl_share,
            pstcl_share,
            avg_d,
        ]

    performance_df = pd.DataFrame(data_dict)

    def apply_gradient(row):
        styles = [''] * len(row)
        if "Share" in str(row.iloc[0]):
            vals = []
            for val in row.iloc[1:]:
                try:
                    vals.append(float(str(val).strip('%')))
                except ValueError:
                    vals.append(None)
            valid_vals = [v for v in vals if v is not None]
            if not valid_vals:
                return styles
            min_val, max_val = min(valid_vals), max(valid_vals)
            for i, val in enumerate(vals):
                if val is not None:
                    norm = (val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                    if norm < 0.5:
                        pct = norm / 0.5
                        r, g, b = int(248 + (255-248)*pct), int(105 + (235-105)*pct), int(107 + (132-107)*pct)
                    else:
                        pct = (norm - 0.5) / 0.5
                        r, g, b = int(255 + (99-255)*pct), int(235 + (195-235)*pct), int(132 + (132-132)*pct)
                    styles[i+1] = f'background-color:rgba({r},{g},{b},0.6);color:#000000;font-weight:500;'
        return styles

    styled_df = performance_df.style.apply(apply_gradient, axis=1)
    st.dataframe(styled_df, hide_index=True, use_container_width=True)


# ── Entry Point ───────────────────────────────────────────────────────────────
render_ptw_lm_dashboard()

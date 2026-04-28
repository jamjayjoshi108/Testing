import streamlit as st
import pandas as pd
import requests

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Outage Reduction Plan", page_icon="📉", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    .stApp { background: linear-gradient(145deg, #f8f9fb 0%, #eef1f7 50%, #f4f6fa 100%); }

    .block-container {
        padding-top: clamp(10px, 2vh, 28px) !important;
        padding-left: clamp(16px, 4vw, 64px) !important;
        padding-right: clamp(16px, 4vw, 64px) !important;
        max-width: 100% !important;
    }

    /* Back button */
    .back-btn-wrap { margin-bottom: 16px; }
    div[data-testid="stButton"] > button {
        background: #ffffff;
        border: 1.5px solid rgba(0,102,204,0.2);
        color: #0066cc;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 8px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,102,204,0.08);
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: #0066cc;
        color: #ffffff;
        border-color: #0066cc;
    }

    /* Page title */
    .page-title {
        font-size: clamp(1.4rem, 3vw, 2.2rem);
        font-weight: 800;
        color: #0d1f3c;
        margin: 0 0 4px;
    }
    .page-title span {
        background: linear-gradient(90deg, #0066cc, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .page-subtitle {
        color: #8a9ab5;
        font-size: 0.85rem;
        margin-bottom: 24px;
    }

    /* Section header */
    .section-header {
        background: linear-gradient(90deg, #0d2d6b, #1a4a9e);
        color: white;
        font-size: clamp(0.95rem, 1.5vw, 1.15rem);
        font-weight: 700;
        text-align: center;
        padding: 12px 20px;
        border-radius: 10px 10px 0 0;
        margin-bottom: 0;
        letter-spacing: 0.3px;
    }

    /* Table */
    .orp-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 0 0 12px 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        margin-bottom: 32px;
    }
    .orp-table th {
        background: #1a4a9e;
        color: white;
        font-size: clamp(0.72rem, 1.1vw, 0.85rem);
        font-weight: 700;
        padding: 10px 16px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .orp-table th.label-col {
        background: #0d2d6b;
        text-align: left;
        width: 22%;
    }
    .orp-table td {
        font-size: clamp(0.72rem, 1.1vw, 0.85rem);
        font-weight: 600;
        padding: 10px 16px;
        text-align: center;
        border: 1px solid #e8edf5;
    }
    .orp-table td.label-td {
        text-align: left;
        color: #0d1f3c;
        font-weight: 500;
        background: #f8f9fb;
    }
    .orp-table tr:hover td { filter: brightness(0.97); }

    /* Progress cell colors */
    .cell-green  { background: #c8f5d8; color: #0a5c2e; }
    .cell-yellow { background: #fff3c4; color: #7a5c00; }
    .cell-red    { background: #ffd6d6; color: #7a0000; }

    /* Divider */
    .divider {
        height: 1.5px;
        background: linear-gradient(90deg, transparent, rgba(0,102,204,0.3), transparent);
        margin: 8px 0 28px;
    }
</style>
""", unsafe_allow_html=True)

# ── Back Button ───────────────────────────────────────────────────────────────
if st.button("← Back to Command Center"):
    st.switch_page("app.py")

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">💡 Outage Reduction Plan <span>(ORP)</span></div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Fetch Google Sheet ─────────────────────────────────────────────────────────
SHEET_ID = "1fO3ED1HsQLhhmAK62wyf3O9ebx5mV6VOtU579eiEIAM"
GID      = "798036434"
CSV_URL  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_data():
    df = pd.read_csv(CSV_URL, header=None)
    return df

try:
    df = load_data()

    # ── Extract date from row 2 (index 2), merged cell area ──────────────────
    date_val = ""
    for cell in df.iloc[2].values:
        if isinstance(cell, str) and "Progress" in cell:
            date_val = cell.strip()
            break

    # ── ORP rows: row index 3=headers(zones), rows 4-7 = data (0-indexed) ────
    zones    = ["South", "East", "North", "Border", "West", "Central"]
    metrics  = ["Feeder deloading", "DT Transformers New",
                "DT Transformers Augmentation", "66kV transformers deloaded"]

    # Extract zone values from row index 3 (B to G columns = index 1 to 6)
    data_rows = df.iloc[4:8, 1:7].values  # rows 5–8, columns B–G

    # ── Color function ────────────────────────────────────────────────────────
    def get_row_classes(row_vals):
        
        """Rank values within a row: highest=green, lowest=red, middle=yellow"""
        parsed = []
        for v in row_vals:
            try:
                parsed.append(float(str(v).replace('%', '').strip()))
            except:
                parsed.append(None)
    
        valid = [v for v in parsed if v is not None]
        if not valid:
            return [""] * len(row_vals)
    
        max_val = max(valid)
        min_val = min(valid)
    
        classes = []
        for v in parsed:
            if v is None:
                classes.append("")
            elif v == max_val:
                classes.append("cell-green")
            elif v == min_val:
                classes.append("cell-red")
            else:
                classes.append("cell-yellow")
        return classes


    # ── Render Section Header ─────────────────────────────────────────────────
    st.markdown(f'<div class="section-header">%age Progress in ORP &nbsp;·&nbsp; {date_val}</div>', unsafe_allow_html=True)

    # ── Build HTML Table ──────────────────────────────────────────────────────
    thead = "<tr><th class='label-col'>Metric</th>" + "".join(f"<th>{z}</th>" for z in zones) + "</tr>"

    tbody = ""
    for row_idx, metric in enumerate(metrics):
        row_vals = [data_rows[row_idx][col_idx] for col_idx in range(6)]
        row_classes = get_row_classes(row_vals)
    
        row_html = f"<tr><td class='label-td'>{metric}</td>"
        for col_idx in range(6):
            val = row_vals[col_idx]
            display = str(val).strip() if str(val).strip() not in ["nan", ""] else "—"
            css = row_classes[col_idx]
            row_html += f"<td class='{css}'>{display}</td>"
        row_html += "</tr>"
        tbody += row_html
    
    st.markdown(f"""
    <table class="orp-table">
        <thead>{thead}</thead>
        <tbody>{tbody}</tbody>
    </table>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Could not load data from Google Sheet. Error: {e}")
    st.info("Make sure the sheet is publicly accessible: File → Share → Anyone with the link → Viewer")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IT Program Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'IBM Plex Mono', monospace;
    }
    .rag-red    { background:#ff4b4b22; border-left:4px solid #ff4b4b; padding:8px 12px; border-radius:4px; color:#ff4b4b; font-weight:600; }
    .rag-amber  { background:#ffa50022; border-left:4px solid #ffa500; padding:8px 12px; border-radius:4px; color:#ffa500; font-weight:600; }
    .rag-green  { background:#00c85322; border-left:4px solid #00c853; padding:8px 12px; border-radius:4px; color:#00c853; font-weight:600; }
    .metric-card { background:#1e1e2e; border-radius:8px; padding:20px; text-align:center; }
    .stDataFrame { font-family: 'IBM Plex Mono', monospace; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ── Data helpers ──────────────────────────────────────────────────────────────
DATA_FILE = "programs.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return get_sample_data()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def get_sample_data():
    return [
        {"Program": "Cloud Migration", "Owner": "Alice Chen", "Status": "Green",
         "Phase": "Execution", "Progress": 72, "Blockers": 0,
         "Budget_Used": 68, "Budget_Total": 500000, "Due": "2025-09-30",
         "Notes": "On track. GCP lift-and-shift 70% complete."},

        {"Program": "ERP Upgrade", "Owner": "Bob Nguyen", "Status": "Amber",
         "Phase": "Planning", "Progress": 35, "Blockers": 2,
         "Budget_Used": 120000, "Budget_Total": 800000, "Due": "2025-12-15",
         "Notes": "Vendor contract delayed. Legal review in progress."},

        {"Program": "Zero Trust Security", "Owner": "Sara Patel", "Status": "Red",
         "Phase": "Execution", "Progress": 20, "Blockers": 3,
         "Budget_Used": 210000, "Budget_Total": 300000, "Due": "2025-07-01",
         "Notes": "Critical: Identity provider integration blocked. Escalated to CISO."},

        {"Program": "ITSM Rollout", "Owner": "James Liu", "Status": "Green",
         "Phase": "Closing", "Progress": 90, "Blockers": 0,
         "Budget_Used": 95000, "Budget_Total": 100000, "Due": "2025-05-15",
         "Notes": "ServiceNow live. Final UAT signoffs pending."},

        {"Program": "Data Center Consolidation", "Owner": "Maria Gomez", "Status": "Amber",
         "Phase": "Execution", "Progress": 55, "Blockers": 1,
         "Budget_Used": 340000, "Budget_Total": 600000, "Due": "2026-01-30",
         "Notes": "Network re-routing causing minor delays in DC3 decom."},
    ]

# ── RAG badge helper ──────────────────────────────────────────────────────────
def rag_badge(status):
    cls = {"Red": "rag-red", "Amber": "rag-amber", "Green": "rag-green"}.get(status, "rag-green")
    icon = {"Red": "🔴", "Amber": "🟡", "Green": "🟢"}.get(status, "🟢")
    return f'<span class="{cls}">{icon} {status}</span>'

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Controls")
    st.markdown("---")
    view = st.radio("View", ["📊 Dashboard", "📋 Program List", "➕ Add / Edit Program", "📥 Import CSV"])
    st.markdown("---")
    st.caption(f"Last refreshed: {datetime.now().strftime('%b %d, %Y %H:%M')}")
    if st.button("🔄 Reset to Sample Data"):
        save_data(get_sample_data())
        st.success("Reset done!")
        st.rerun()

# ── Load data ─────────────────────────────────────────────────────────────────
programs = load_data()
df = pd.DataFrame(programs)

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if view == "📊 Dashboard":
    st.title("📊 IT Program Dashboard")
    st.markdown(f"**{len(df)} active programs** &nbsp;|&nbsp; as of {date.today().strftime('%B %d, %Y')}")
    st.markdown("---")

    # ── KPI row ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Programs", len(df))
    c2.metric("🟢 On Track",    len(df[df.Status == "Green"]))
    c3.metric("🟡 At Risk",     len(df[df.Status == "Amber"]))
    c4.metric("🔴 Critical",    len(df[df.Status == "Red"]))
    c5.metric("Total Blockers", int(df.Blockers.sum()))

    st.markdown("---")

    # ── Charts row ────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Status Distribution")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        color_map = {"Green": "#00c853", "Amber": "#ffa500", "Red": "#ff4b4b"}
        fig_pie = px.pie(
            status_counts, names="Status", values="Count",
            color="Status", color_discrete_map=color_map,
            hole=0.45
        )
        fig_pie.update_layout(margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", font_color="#ccc")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("Program Progress (%)")
        df_sorted = df.sort_values("Progress", ascending=True)
        colors = [color_map[s] for s in df_sorted["Status"]]
        fig_bar = go.Figure(go.Bar(
            x=df_sorted["Progress"],
            y=df_sorted["Program"],
            orientation="h",
            marker_color=colors,
            text=df_sorted["Progress"].astype(str) + "%",
            textposition="outside"
        ))
        fig_bar.update_layout(
            xaxis=dict(range=[0, 110]),
            margin=dict(t=20, b=20, l=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Budget utilization ────────────────────────────────────────────────────
    st.subheader("💰 Budget Utilization")
    df["Budget_%"] = (df["Budget_Used"] / df["Budget_Total"] * 100).round(1)
    df["Budget_Remaining"] = df["Budget_Total"] - df["Budget_Used"]

    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(name="Used", x=df["Program"], y=df["Budget_Used"],
                                marker_color="#4c9be8"))
    fig_budget.add_trace(go.Bar(name="Remaining", x=df["Program"], y=df["Budget_Remaining"],
                                marker_color="#2d2d3e"))
    fig_budget.update_layout(
        barmode="stack", margin=dict(t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ccc", yaxis_title="USD"
    )
    st.plotly_chart(fig_budget, use_container_width=True)

    # ── Blockers spotlight ────────────────────────────────────────────────────
    blocked = df[df.Blockers > 0][["Program", "Owner", "Blockers", "Status", "Notes"]]
    if not blocked.empty:
        st.subheader("🚧 Programs with Blockers")
        for _, row in blocked.iterrows():
            with st.expander(f"{row['Program']}  —  {row['Blockers']} blocker(s)"):
                st.markdown(rag_badge(row["Status"]), unsafe_allow_html=True)
                st.write(f"**Owner:** {row['Owner']}")
                st.write(f"**Notes:** {row['Notes']}")

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — PROGRAM LIST
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "📋 Program List":
    st.title("📋 All Programs")

    # Filters
    fc1, fc2 = st.columns(2)
    status_filter = fc1.multiselect("Filter by Status", ["Green", "Amber", "Red"],
                                     default=["Green", "Amber", "Red"])
    phase_filter  = fc2.multiselect("Filter by Phase",
                                     df["Phase"].unique().tolist(),
                                     default=df["Phase"].unique().tolist())

    filtered = df[(df["Status"].isin(status_filter)) & (df["Phase"].isin(phase_filter))]

    for _, row in filtered.iterrows():
        with st.expander(f"**{row['Program']}**  —  {row['Phase']}  ({row['Progress']}% complete)"):
            left, right = st.columns([1, 2])
            with left:
                st.markdown(rag_badge(row["Status"]), unsafe_allow_html=True)
                st.write(f"**Owner:** {row['Owner']}")
                st.write(f"**Due:** {row['Due']}")
                st.write(f"**Blockers:** {row['Blockers']}")
                budget_pct = round(row["Budget_Used"] / row["Budget_Total"] * 100, 1)
                st.write(f"**Budget:** ${row['Budget_Used']:,} / ${row['Budget_Total']:,} ({budget_pct}%)")
            with right:
                st.progress(int(row["Progress"]) / 100)
                st.write(f"**Notes:** {row['Notes']}")

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 3 — ADD / EDIT
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "➕ Add / Edit Program":
    st.title("➕ Add or Edit a Program")

    action = st.radio("Action", ["Add new program", "Edit existing program"])

    if action == "Edit existing program":
        prog_names = [p["Program"] for p in programs]
        selected = st.selectbox("Select program to edit", prog_names)
        idx = prog_names.index(selected)
        existing = programs[idx]
    else:
        idx = None
        existing = {"Program": "", "Owner": "", "Status": "Green", "Phase": "Planning",
                    "Progress": 0, "Blockers": 0, "Budget_Used": 0, "Budget_Total": 0,
                    "Due": str(date.today()), "Notes": ""}

    with st.form("program_form"):
        c1, c2 = st.columns(2)
        name    = c1.text_input("Program Name",  existing["Program"])
        owner   = c2.text_input("Owner",          existing["Owner"])
        status  = c1.selectbox("RAG Status",     ["Green", "Amber", "Red"],
                                index=["Green","Amber","Red"].index(existing["Status"]))
        phase   = c2.selectbox("Phase",          ["Planning","Execution","Closing"],
                                index=["Planning","Execution","Closing"].index(existing["Phase"]))
        progress = c1.slider("Progress (%)", 0, 100, int(existing["Progress"]))
        blockers = c2.number_input("Blockers", 0, 20, int(existing["Blockers"]))
        bused   = c1.number_input("Budget Used ($)",  0, 10_000_000, int(existing["Budget_Used"]), step=10000)
        btotal  = c2.number_input("Budget Total ($)", 0, 10_000_000, int(existing["Budget_Total"]), step=10000)
        due     = st.text_input("Due Date (YYYY-MM-DD)", existing["Due"])
        notes   = st.text_area("Notes / Status Update", existing["Notes"])
        submitted = st.form_submit_button("💾 Save Program")

    if submitted:
        entry = {"Program": name, "Owner": owner, "Status": status, "Phase": phase,
                 "Progress": progress, "Blockers": blockers, "Budget_Used": bused,
                 "Budget_Total": btotal, "Due": due, "Notes": notes}
        if idx is not None:
            programs[idx] = entry
        else:
            programs.append(entry)
        save_data(programs)
        st.success(f"✅ '{name}' saved!")
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 4 — IMPORT CSV
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "📥 Import CSV":
    st.title("📥 Import Programs from CSV")

    # ── Download template ─────────────────────────────────────────────────────
    st.subheader("Step 1 — Download the Template")
    st.markdown("Start from this template so your columns match exactly what the dashboard expects.")

    template_csv = """Program,Owner,Status,Phase,Progress,Blockers,Budget_Used,Budget_Total,Due,Notes
Cloud Migration,Alice Chen,Green,Execution,72,0,68000,500000,2025-09-30,On track. GCP lift-and-shift 70% complete.
ERP Upgrade,Bob Nguyen,Amber,Planning,35,2,120000,800000,2025-12-15,Vendor contract delayed. Legal review in progress.
"""
    st.download_button(
        label="⬇️ Download CSV Template",
        data=template_csv,
        file_name="programs_template.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # ── Upload CSV ────────────────────────────────────────────────────────────
    st.subheader("Step 2 — Fill it in & Upload")
    st.markdown("""
**Column rules:**
- `Status` → must be `Green`, `Amber`, or `Red`
- `Phase` → must be `Planning`, `Execution`, or `Closing`
- `Progress` → number 0–100
- `Budget_Used` / `Budget_Total` → numbers, no $ or commas
- `Due` → format `YYYY-MM-DD`
""")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        try:
            csv_df = pd.read_csv(uploaded_file)

            # ── Validate required columns ─────────────────────────────────────
            required_cols = ["Program","Owner","Status","Phase","Progress",
                             "Blockers","Budget_Used","Budget_Total","Due","Notes"]
            missing = [c for c in required_cols if c not in csv_df.columns]
            if missing:
                st.error(f"❌ Missing columns: {', '.join(missing)}")
                st.stop()

            # ── Validate Status values ────────────────────────────────────────
            bad_status = csv_df[~csv_df["Status"].isin(["Green","Amber","Red"])]["Status"].unique()
            if len(bad_status):
                st.error(f"❌ Invalid Status values found: {list(bad_status)}. Must be Green, Amber, or Red.")
                st.stop()

            # ── Validate Phase values ─────────────────────────────────────────
            bad_phase = csv_df[~csv_df["Phase"].isin(["Planning","Execution","Closing"])]["Phase"].unique()
            if len(bad_phase):
                st.error(f"❌ Invalid Phase values found: {list(bad_phase)}. Must be Planning, Execution, or Closing.")
                st.stop()

            # ── Preview ───────────────────────────────────────────────────────
            st.success(f"✅ File looks good! Found **{len(csv_df)} programs**.")
            st.subheader("Preview")
            st.dataframe(csv_df, use_container_width=True)

            # ── Import options ────────────────────────────────────────────────
            st.markdown("---")
            st.subheader("Step 3 — Choose Import Mode")
            import_mode = st.radio(
                "How should this data be imported?",
                ["Replace all existing programs", "Append to existing programs"]
            )

            if st.button("🚀 Import Now", type="primary"):
                new_records = csv_df[required_cols].fillna("").to_dict(orient="records")
                # Coerce numeric fields
                for r in new_records:
                    r["Progress"]     = int(float(r["Progress"]))
                    r["Blockers"]     = int(float(r["Blockers"]))
                    r["Budget_Used"]  = int(float(r["Budget_Used"]))
                    r["Budget_Total"] = int(float(r["Budget_Total"]))

                if import_mode == "Replace all existing programs":
                    save_data(new_records)
                    st.success(f"✅ Replaced all data with {len(new_records)} programs from CSV!")
                else:
                    existing_programs = load_data()
                    combined = existing_programs + new_records
                    save_data(combined)
                    st.success(f"✅ Appended {len(new_records)} programs. Total: {len(combined)}.")

                st.balloons()
                st.rerun()

        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

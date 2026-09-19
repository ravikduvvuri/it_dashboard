import json
import os
from datetime import date, datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="IT Program Command Center",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "programs.json"
REQUIRED_COLS = [
    "Program",
    "Owner",
    "Status",
    "Phase",
    "Progress",
    "Blockers",
    "Budget_Used",
    "Budget_Total",
    "Due",
    "Notes",
]
STATUS_OPTIONS = ["Green", "Amber", "Red"]
PHASE_OPTIONS = ["Planning", "Execution", "Closing"]
STATUS_TO_COLOR = {"Green": "#2f7b4a", "Amber": "#b76b21", "Red": "#a93f32"}


def render_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Manrope:wght@400;500;700&display=swap');

:root {
  --paper: oklch(0.978 0.017 72);
  --paper-deep: oklch(0.944 0.021 72);
  --ink: oklch(0.255 0.035 62);
  --muted-ink: oklch(0.43 0.022 62);
  --line: oklch(0.83 0.027 70);
  --green-bg: oklch(0.95 0.03 155);
  --green-ink: oklch(0.43 0.09 152);
  --amber-bg: oklch(0.95 0.035 72);
  --amber-ink: oklch(0.5 0.11 72);
  --red-bg: oklch(0.95 0.04 26);
  --red-ink: oklch(0.49 0.12 24);
  --brand: oklch(0.51 0.09 47);
}

html, body, [class*="css"] {
  font-family: 'Manrope', sans-serif;
  color: var(--ink);
}

[data-testid="stAppViewContainer"] {
  background:
      radial-gradient(1600px 700px at 80% -10%, oklch(0.92 0.05 78 / 0.45), transparent 62%),
      radial-gradient(900px 500px at -5% 10%, oklch(0.9 0.05 32 / 0.22), transparent 70%),
      repeating-linear-gradient(
        -45deg,
        transparent,
        transparent 22px,
        oklch(0.92 0.02 70 / 0.44) 22px,
        oklch(0.92 0.02 70 / 0.44) 23px
      ),
      var(--paper);
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, oklch(0.93 0.03 72), oklch(0.9 0.03 65));
  border-right: 1px solid var(--line);
}

h1, h2, h3 {
  font-family: 'Fraunces', serif;
  letter-spacing: 0.01em;
  color: oklch(0.21 0.045 58);
}

h1 {
  font-size: clamp(1.8rem, 2.4vw, 2.8rem);
  margin-bottom: 0.25rem;
}

h2 {
  font-size: clamp(1.25rem, 1.4vw, 1.8rem);
  margin-top: 1.6rem;
}

p, li, label, .stMarkdown, .stCaption {
  color: var(--ink);
}

[data-testid="stMetricValue"] {
  font-family: 'Fraunces', serif;
  font-size: clamp(1.4rem, 2vw, 2.1rem);
  color: oklch(0.22 0.045 60);
}

[data-testid="stMetricLabel"] {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.72rem;
  color: var(--muted-ink);
}

.panel {
  border: 1px solid var(--line);
  background: color-mix(in oklch, var(--paper-deep) 84%, white 16%);
  border-radius: 16px;
  padding: clamp(0.9rem, 1.1vw, 1.2rem);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 999px;
  padding: 0.36rem 0.86rem;
  border: 1px solid transparent;
  font-weight: 700;
  letter-spacing: 0.01em;
  font-size: 0.87rem;
}

.status-dot {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
}

.badge-green {
  background: var(--green-bg);
  color: var(--green-ink);
  border-color: color-mix(in oklch, var(--green-ink) 22%, var(--green-bg));
}

.badge-amber {
  background: var(--amber-bg);
  color: var(--amber-ink);
  border-color: color-mix(in oklch, var(--amber-ink) 20%, var(--amber-bg));
}

.badge-red {
  background: var(--red-bg);
  color: var(--red-ink);
  border-color: color-mix(in oklch, var(--red-ink) 22%, var(--red-bg));
}

.hero-note {
  border-left: 3px solid var(--brand);
  margin: 0.6rem 0 1rem;
  padding: 0.2rem 0 0.2rem 0.85rem;
  color: color-mix(in oklch, var(--ink) 82%, var(--brand));
}

.dataframe tbody tr td {
  font-size: 0.93rem;
}

.empty-state {
  border: 1px dashed color-mix(in oklch, var(--line) 78%, var(--brand));
  border-radius: 16px;
  padding: 1rem;
  background: color-mix(in oklch, var(--paper) 92%, var(--brand));
}

.kpi-slab {
  margin-top: 0.75rem;
  margin-bottom: 1.1rem;
  padding: 0.8rem 1rem;
  border-radius: 14px;
  border: 1px solid color-mix(in oklch, var(--line) 82%, var(--brand));
  background:
      linear-gradient(93deg,
      color-mix(in oklch, var(--paper-deep) 84%, var(--brand)) 0%,
      color-mix(in oklch, var(--paper-deep) 89%, var(--paper)) 48%,
      color-mix(in oklch, var(--paper-deep) 84%, var(--brand)) 100%);
}

.stButton > button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"] {
  border-radius: 12px;
  border: 1px solid color-mix(in oklch, var(--line) 58%, var(--brand));
  background: color-mix(in oklch, var(--paper-deep) 86%, var(--brand));
  color: oklch(0.26 0.03 60);
  min-height: 44px;
  transition: transform 180ms cubic-bezier(.19,1,.22,1),
              background-color 180ms cubic-bezier(.19,1,.22,1),
              border-color 180ms cubic-bezier(.19,1,.22,1);
}

.stButton > button:hover,
[data-testid="baseButton-secondary"]:hover,
[data-testid="baseButton-primary"]:hover {
  transform: translateY(-1px);
  border-color: color-mix(in oklch, var(--line) 34%, var(--brand));
  background: color-mix(in oklch, var(--paper-deep) 74%, var(--brand));
}

.stButton > button:focus-visible,
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
[data-baseweb="select"] div:focus-visible {
  outline: 3px solid color-mix(in oklch, var(--brand) 55%, white);
  outline-offset: 2px;
  box-shadow: none !important;
}

[data-testid="stHorizontalBlock"] [data-testid="column"] {
  container-type: inline-size;
}

@container (max-width: 480px) {
  .hero-note {
    padding-left: 0.65rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .stButton > button,
  [data-testid="baseButton-secondary"],
  [data-testid="baseButton-primary"] {
    transition: none;
  }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def get_sample_data() -> list[dict]:
    return [
        {
            "Program": "Cloud Migration",
            "Owner": "Alice Chen",
            "Status": "Green",
            "Phase": "Execution",
            "Progress": 72,
            "Blockers": 0,
            "Budget_Used": 68000,
            "Budget_Total": 500000,
            "Due": "2025-09-30",
            "Notes": "On track. GCP lift-and-shift 70% complete.",
        },
        {
            "Program": "ERP Upgrade",
            "Owner": "Bob Nguyen",
            "Status": "Amber",
            "Phase": "Planning",
            "Progress": 35,
            "Blockers": 2,
            "Budget_Used": 120000,
            "Budget_Total": 800000,
            "Due": "2025-12-15",
            "Notes": "Vendor contract delayed. Legal review in progress.",
        },
        {
            "Program": "Zero Trust Security",
            "Owner": "Sara Patel",
            "Status": "Red",
            "Phase": "Execution",
            "Progress": 20,
            "Blockers": 3,
            "Budget_Used": 210000,
            "Budget_Total": 300000,
            "Due": "2025-07-01",
            "Notes": "Identity provider integration blocked. Escalated to CISO.",
        },
        {
            "Program": "ITSM Rollout",
            "Owner": "James Liu",
            "Status": "Green",
            "Phase": "Closing",
            "Progress": 90,
            "Blockers": 0,
            "Budget_Used": 95000,
            "Budget_Total": 100000,
            "Due": "2025-05-15",
            "Notes": "ServiceNow live. Final UAT signoffs pending.",
        },
        {
            "Program": "Data Center Consolidation",
            "Owner": "Maria Gomez",
            "Status": "Amber",
            "Phase": "Execution",
            "Progress": 55,
            "Blockers": 1,
            "Budget_Used": 340000,
            "Budget_Total": 600000,
            "Due": "2026-01-30",
            "Notes": "Network re-routing is slowing DC3 decommissioning.",
        },
    ]


def coerce_program_record(record: dict) -> dict:
    due_value = str(record.get("Due", "")).strip()
    try:
        due_iso = datetime.strptime(due_value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        due_iso = date.today().isoformat()

    return {
        "Program": str(record.get("Program", "")).strip(),
        "Owner": str(record.get("Owner", "")).strip(),
        "Status": str(record.get("Status", "Green")).strip().title(),
        "Phase": str(record.get("Phase", "Planning")).strip().title(),
        "Progress": int(float(record.get("Progress", 0) or 0)),
        "Blockers": int(float(record.get("Blockers", 0) or 0)),
        "Budget_Used": int(float(record.get("Budget_Used", 0) or 0)),
        "Budget_Total": int(float(record.get("Budget_Total", 0) or 0)),
        "Due": due_iso,
        "Notes": str(record.get("Notes", "")).strip(),
    }


def normalize_data(records: list[dict]) -> list[dict]:
    cleaned = [coerce_program_record(r) for r in records]
    return [r for r in cleaned if r["Program"]]


def load_data() -> list[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as file_obj:
            raw = json.load(file_obj)
        return normalize_data(raw)
    return get_sample_data()


def save_data(data: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file_obj:
        json.dump(normalize_data(data), file_obj, indent=2, default=str)


def rag_badge(status: str) -> str:
    css_map = {
        "Green": "badge-green",
        "Amber": "badge-amber",
        "Red": "badge-red",
    }
    dot_color = STATUS_TO_COLOR.get(status, STATUS_TO_COLOR["Green"])
    css = css_map.get(status, "badge-green")
    return (
        f'<span class="status-badge {css}">'
        f'<span class="status-dot" style="background:{dot_color};"></span>{status}</span>'
    )


def validate_frame(input_df: pd.DataFrame) -> tuple[bool, str]:
    missing = [col for col in REQUIRED_COLS if col not in input_df.columns]
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"

    bad_status = input_df[~input_df["Status"].isin(STATUS_OPTIONS)]["Status"].dropna().unique().tolist()
    if bad_status:
        return False, f"Invalid Status values: {bad_status}. Allowed: Green, Amber, Red."

    bad_phase = input_df[~input_df["Phase"].isin(PHASE_OPTIONS)]["Phase"].dropna().unique().tolist()
    if bad_phase:
        return False, f"Invalid Phase values: {bad_phase}. Allowed: Planning, Execution, Closing."

    for numeric in ["Progress", "Blockers", "Budget_Used", "Budget_Total"]:
        if pd.to_numeric(input_df[numeric], errors="coerce").isnull().any():
            return False, f"Column {numeric} contains non-numeric values."

    due_parsed = pd.to_datetime(input_df["Due"], errors="coerce", format="%Y-%m-%d")
    if due_parsed.isnull().any():
        return False, "Due must use YYYY-MM-DD format."

    return True, ""


def compute_health_score(frame: pd.DataFrame) -> int:
    if frame.empty:
        return 100
    status_penalty = frame["Status"].map({"Green": 0, "Amber": 10, "Red": 24}).sum()
    blocker_penalty = int(frame["Blockers"].sum()) * 4
    overdue_penalty = int((pd.to_datetime(frame["Due"]) < pd.Timestamp.today()).sum()) * 5
    score = 100 - status_penalty - blocker_penalty - overdue_penalty
    return max(0, min(100, score))


def chart_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=28, b=18, l=16, r=10),
        font=dict(color="#3f342d", family="Manrope, sans-serif"),
        legend=dict(orientation="h", y=1.12),
    )
    fig.update_xaxes(gridcolor="rgba(139,122,107,0.18)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(139,122,107,0.18)", zeroline=False)
    return fig


render_css()
programs = load_data()
df = pd.DataFrame(programs)
if df.empty:
    df = pd.DataFrame(get_sample_data())

with st.sidebar:
    st.markdown("## Mission Control")
    st.caption("Program portfolio tracking for IT leadership")
    view = st.radio(
        "Navigate",
        ["Dashboard", "Program List", "Add / Edit Program", "Import CSV"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.caption(f"Snapshot generated {datetime.now().strftime('%b %d, %Y at %H:%M')}")
    if st.button("Reset to Sample Data", use_container_width=True):
        save_data(get_sample_data())
        st.success("Sample dataset restored.")
        st.rerun()


if view == "Dashboard":
    st.title("IT Program Command Center")
    st.markdown(
        "<p class='hero-note'>A portfolio view tuned for fast executive triage: risk, delivery velocity, and budget runway in one scan.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='kpi-slab'>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    on_track = int((df["Status"] == "Green").sum())
    at_risk = int((df["Status"] == "Amber").sum())
    critical = int((df["Status"] == "Red").sum())
    blockers = int(df["Blockers"].sum())
    health_score = compute_health_score(df)

    c1.metric("Programs", int(len(df)))
    c2.metric("On Track", on_track)
    c3.metric("At Risk", at_risk)
    c4.metric("Critical", critical)
    c5.metric("Blockers", blockers)
    c6.metric("Portfolio Health", f"{health_score}/100")
    st.markdown("</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.18], gap="large")

    with left_col:
        st.markdown("### Status Mix")
        status_counts = df["Status"].value_counts().reindex(STATUS_OPTIONS, fill_value=0).reset_index()
        status_counts.columns = ["Status", "Count"]
        pie = px.pie(
            status_counts,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map=STATUS_TO_COLOR,
            hole=0.52,
        )
        pie.update_traces(textposition="outside", textfont_size=13)
        pie.update_layout(showlegend=True)
        st.plotly_chart(chart_theme(pie), use_container_width=True)

        st.markdown("### Blockers Radar")
        blocker_df = df.sort_values("Blockers", ascending=False).head(6)
        blocker_fig = go.Figure(
            data=go.Scatterpolar(
                r=blocker_df["Blockers"],
                theta=blocker_df["Program"],
                fill="toself",
                line_color="#8f4e2f",
                fillcolor="rgba(186, 104, 69, 0.35)",
            )
        )
        blocker_fig.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, gridcolor="rgba(139,122,107,0.2)")),
            margin=dict(t=18, b=18, l=18, r=18),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3f342d", family="Manrope, sans-serif"),
            showlegend=False,
        )
        st.plotly_chart(blocker_fig, use_container_width=True)

    with right_col:
        st.markdown("### Progress by Program")
        progress_df = df.sort_values("Progress", ascending=True)
        progress_fig = go.Figure(
            go.Bar(
                x=progress_df["Progress"],
                y=progress_df["Program"],
                orientation="h",
                marker_color=[STATUS_TO_COLOR[s] for s in progress_df["Status"]],
                text=progress_df["Progress"].astype(str) + "%",
                textposition="outside",
                hovertemplate="%{y}<br>Progress: %{x}%<extra></extra>",
            )
        )
        progress_fig.update_layout(xaxis=dict(range=[0, 110]))
        st.plotly_chart(chart_theme(progress_fig), use_container_width=True)

        st.markdown("### Budget Runway")
        budget_df = df.copy()
        budget_df["Remaining"] = budget_df["Budget_Total"] - budget_df["Budget_Used"]
        budget_fig = go.Figure()
        budget_fig.add_trace(
            go.Bar(
                name="Used",
                x=budget_df["Program"],
                y=budget_df["Budget_Used"],
                marker_color="#9f6644",
                hovertemplate="%{x}<br>Used: $%{y:,.0f}<extra></extra>",
            )
        )
        budget_fig.add_trace(
            go.Bar(
                name="Remaining",
                x=budget_df["Program"],
                y=budget_df["Remaining"],
                marker_color="#d6b79e",
                hovertemplate="%{x}<br>Remaining: $%{y:,.0f}<extra></extra>",
            )
        )
        budget_fig.update_layout(barmode="stack", yaxis_title="USD")
        st.plotly_chart(chart_theme(budget_fig), use_container_width=True)

    st.markdown("### Programs with Active Blockers")
    blocked = df[df["Blockers"] > 0].sort_values(["Blockers", "Status"], ascending=[False, True])
    if blocked.empty:
        st.markdown(
            "<div class='empty-state'><strong>No active blockers.</strong><br/>This portfolio currently has a clean critical path.</div>",
            unsafe_allow_html=True,
        )
    else:
        for _, row in blocked.iterrows():
            due_text = pd.to_datetime(row["Due"]).strftime("%b %d, %Y")
            with st.expander(f"{row['Program']} - {int(row['Blockers'])} blocker(s)"):
                st.markdown(rag_badge(row["Status"]), unsafe_allow_html=True)
                info_left, info_right = st.columns([1, 2])
                info_left.markdown(f"**Owner**  \n{row['Owner']}  \n**Due**  \n{due_text}")
                info_right.markdown(f"**Current note**  \n{row['Notes']}")


elif view == "Program List":
    st.title("Program Register")
    st.caption("Filter, inspect, and review the current execution posture.")

    f1, f2, f3 = st.columns([1.1, 1.1, 1.4])
    status_filter = f1.multiselect("Status", STATUS_OPTIONS, default=STATUS_OPTIONS)
    phase_filter = f2.multiselect("Phase", PHASE_OPTIONS, default=PHASE_OPTIONS)
    owner_filter = f3.multiselect("Owner", sorted(df["Owner"].unique().tolist()), default=sorted(df["Owner"].unique().tolist()))
    keyword = st.text_input("Search in program name or notes", placeholder="Try cloud, security, migration...").strip().lower()

    filtered = df[
        (df["Status"].isin(status_filter))
        & (df["Phase"].isin(phase_filter))
        & (df["Owner"].isin(owner_filter))
    ].copy()

    if keyword:
        filtered = filtered[
            filtered["Program"].str.lower().str.contains(keyword)
            | filtered["Notes"].str.lower().str.contains(keyword)
        ]

    st.markdown(f"<div class='hero-note'>{len(filtered)} of {len(df)} programs match current filters.</div>", unsafe_allow_html=True)

    if filtered.empty:
        st.markdown(
            "<div class='empty-state'><strong>No matches yet.</strong><br/>Clear one or more filters or search for a broader keyword.</div>",
            unsafe_allow_html=True,
        )
    else:
        for _, row in filtered.sort_values(["Status", "Progress"]).iterrows():
            budget_total = max(1, int(row["Budget_Total"]))
            budget_pct = round((int(row["Budget_Used"]) / budget_total) * 100, 1)
            due_readable = pd.to_datetime(row["Due"]).strftime("%b %d, %Y")
            with st.expander(f"{row['Program']} | {row['Phase']} | {int(row['Progress'])}% complete"):
                left, right = st.columns([1.05, 1.95])
                with left:
                    st.markdown(rag_badge(row["Status"]), unsafe_allow_html=True)
                    st.markdown(
                        f"**Owner**: {row['Owner']}  \n**Due**: {due_readable}  \n**Blockers**: {int(row['Blockers'])}  \n**Budget**: ${int(row['Budget_Used']):,} / ${int(row['Budget_Total']):,} ({budget_pct}%)"
                    )
                with right:
                    st.progress(int(row["Progress"]) / 100)
                    st.markdown(f"**Latest note**  \n{row['Notes']}")


elif view == "Add / Edit Program":
    st.title("Program Intake and Updates")
    st.caption("Add new initiatives or update existing records with validated fields.")

    action = st.radio("Mode", ["Add new program", "Edit existing program"], horizontal=True)

    if action == "Edit existing program" and programs:
        program_names = [p["Program"] for p in programs]
        selected_program = st.selectbox("Select program", program_names)
        idx = program_names.index(selected_program)
        existing = programs[idx]
    else:
        idx = None
        existing = {
            "Program": "",
            "Owner": "",
            "Status": "Green",
            "Phase": "Planning",
            "Progress": 0,
            "Blockers": 0,
            "Budget_Used": 0,
            "Budget_Total": 100000,
            "Due": date.today().isoformat(),
            "Notes": "",
        }

    with st.form("program_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        program_name = c1.text_input("Program name", value=existing["Program"], max_chars=120)
        owner = c2.text_input("Owner", value=existing["Owner"], max_chars=80)
        status = c1.selectbox("Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(existing["Status"]))
        phase = c2.selectbox("Phase", PHASE_OPTIONS, index=PHASE_OPTIONS.index(existing["Phase"]))
        progress = c1.slider("Progress (%)", 0, 100, int(existing["Progress"]))
        blockers = c2.number_input("Blockers", min_value=0, max_value=99, value=int(existing["Blockers"]), step=1)
        budget_used = c1.number_input("Budget used ($)", min_value=0, max_value=50_000_000, value=int(existing["Budget_Used"]), step=1000)
        budget_total = c2.number_input("Budget total ($)", min_value=1, max_value=50_000_000, value=max(1, int(existing["Budget_Total"])), step=1000)

        try:
            default_due = datetime.strptime(str(existing["Due"]), "%Y-%m-%d").date()
        except ValueError:
            default_due = date.today()
        due_date = st.date_input("Due date", value=default_due)

        notes = st.text_area(
            "Status update",
            value=existing["Notes"],
            placeholder="Capture material risks, decisions, and next milestones.",
            max_chars=800,
        )
        submitted = st.form_submit_button("Save Program", type="primary")

    if submitted:
        errors = []
        if not program_name.strip():
            errors.append("Program name is required.")
        if not owner.strip():
            errors.append("Owner is required.")
        if budget_used > budget_total:
            errors.append("Budget used cannot exceed budget total.")

        if errors:
            for msg in errors:
                st.error(msg)
        else:
            entry = {
                "Program": program_name.strip(),
                "Owner": owner.strip(),
                "Status": status,
                "Phase": phase,
                "Progress": int(progress),
                "Blockers": int(blockers),
                "Budget_Used": int(budget_used),
                "Budget_Total": int(budget_total),
                "Due": due_date.isoformat(),
                "Notes": notes.strip(),
            }
            if idx is not None:
                programs[idx] = entry
            else:
                programs.append(entry)
            save_data(programs)
            st.success(f"Saved program: {entry['Program']}")
            st.rerun()


elif view == "Import CSV":
    st.title("CSV Import")
    st.caption("Bulk-import programs with schema validation and controlled merge mode.")

    st.markdown("### 1) Download template")
    template_csv = (
        "Program,Owner,Status,Phase,Progress,Blockers,Budget_Used,Budget_Total,Due,Notes\n"
        "Cloud Migration,Alice Chen,Green,Execution,72,0,68000,500000,2025-09-30,On track. Migration wave 3 complete.\n"
        "ERP Upgrade,Bob Nguyen,Amber,Planning,35,2,120000,800000,2025-12-15,Vendor contract delayed. Legal review in progress.\n"
    )
    st.download_button(
        label="Download CSV template",
        data=template_csv,
        file_name="programs_template.csv",
        mime="text/csv",
    )

    st.markdown("### 2) Upload and validate")
    st.markdown(
        "- Status values: Green, Amber, Red  \n"
        "- Phase values: Planning, Execution, Closing  \n"
        "- Progress range: 0 to 100  \n"
        "- Due format: YYYY-MM-DD"
    )

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            csv_df = pd.read_csv(uploaded_file)
            is_valid, reason = validate_frame(csv_df)
            if not is_valid:
                st.error(reason)
            else:
                st.success(f"Validation passed. {len(csv_df)} rows detected.")
                st.dataframe(csv_df[REQUIRED_COLS], use_container_width=True)

                st.markdown("### 3) Choose import mode")
                mode = st.radio(
                    "Import mode",
                    ["Replace all existing programs", "Append to existing programs"],
                )

                if st.button("Import now", type="primary"):
                    records = csv_df[REQUIRED_COLS].fillna("").to_dict(orient="records")
                    incoming = normalize_data(records)
                    if mode == "Replace all existing programs":
                        save_data(incoming)
                        st.success(f"Replaced existing data with {len(incoming)} programs.")
                    else:
                        combined = normalize_data(load_data() + incoming)
                        save_data(combined)
                        st.success(f"Appended {len(incoming)} programs. New total: {len(combined)}.")
                    st.rerun()
        except Exception as exc:
            st.error(f"Could not process CSV file: {exc}")


st.markdown("---")
st.caption("Built for decisive portfolio reviews. Last render: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

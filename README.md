# 📊 IT Program Status Dashboard

A Streamlit dashboard for TPMs to track IT programs with RAG status, progress, budget utilization, and blocker visibility.

---

## 🚀 Quick Start

### 1. Prerequisites
Make sure you have Python 3.9+ installed.
```bash
python --version
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 📁 Project Structure

```
it_dashboard/
├── app.py            ← Main dashboard application
├── requirements.txt  ← Python dependencies
├── README.md         ← This file
└── programs.json     ← Auto-created when you save data (persists between runs)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **KPI Summary** | Total programs, Green / Amber / Red counts, total blockers |
| **RAG Status** | Color-coded Red / Amber / Green per program |
| **Progress Chart** | Horizontal bar chart per program |
| **Budget Utilization** | Stacked bar: used vs remaining |
| **Blocker Spotlight** | Expandable cards for any program with blockers |
| **Program List** | Filterable view with all program details |
| **Add / Edit** | Form to add new programs or update existing ones |
| **Persistent Storage** | Data saved to `programs.json` locally |

---

## 🔧 Customization Ideas (next steps)

- **Import from CSV**: Add a file uploader to bulk-load programs from a spreadsheet
- **Export to PDF**: Use `pdfkit` or `reportlab` to generate a weekly status report
- **Claude AI summaries**: Use the Anthropic API to auto-generate an executive summary
- **Email alerts**: Use `smtplib` to send alerts when a program turns Red
- **Deploy to the web**: Push to [Streamlit Community Cloud](https://streamlit.io/cloud) for free hosting

---

## 📦 Dependencies

- **Streamlit** — Python web app framework (no frontend code needed)
- **Pandas** — Data manipulation
- **Plotly** — Interactive charts

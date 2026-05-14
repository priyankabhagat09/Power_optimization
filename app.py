st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root {
    --bg: #dbe6f5;                 /* Light blue background */
    --panel: #ffffff;              /* White cards */
    --panel-2: #f5f8fd;            /* Secondary card background */
    --border: rgba(20, 60, 120, 0.08);

    --text: #143a72;               /* Deep blue text */
    --muted: #7d8fa8;              /* Gray-blue secondary text */

    --accent: #15468b;             /* Royal blue */
    --accent-soft: rgba(21, 70, 139, 0.08);

    --success: #15468b;
}

/* Global */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg);
    color: var(--text);
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #dbe6f5 0%, #edf3fb 100%);
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
    box-shadow: 4px 0 20px rgba(21, 70, 139, 0.04);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* Title */
h1 {
    font-size: 2rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    color: var(--accent);
    margin-bottom: 0.2rem;
}

/* Subtitle */
.dashboard-subtitle {
    color: var(--muted);
    font-size: 0.9rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid rgba(21, 70, 139, 0.08);
    margin: 1.2rem 0;
}

/* Metric Cards (Predicted State / SNR Value / Network Congestion) */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 22px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 8px 24px rgba(21, 70, 139, 0.06);
    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(21, 70, 139, 0.10);
    border-color: rgba(21, 70, 139, 0.18);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: var(--accent);
    font-size: 1.35rem;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: #ffffff;
    color: var(--accent);
    border: 1px solid rgba(21, 70, 139, 0.10);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(21, 70, 139, 0.05);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff;
    color: var(--text);
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 12px;
}

/* Sliders */
.stSlider > div[data-baseweb="slider"] > div {
    color: var(--accent);
}

/* Tabs */
button[data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border: none;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent);
    font-weight: 600;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(21, 70, 139, 0.05);
}

/* Info box */
[data-testid="stInfo"] {
    background: #ffffff;
    border: 1px solid rgba(21, 70, 139, 0.08);
    border-radius: 14px;
    color: var(--text);
}

/* Status badge */
.status-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    background: rgba(21, 70, 139, 0.08);
    border: 1px solid rgba(21, 70, 139, 0.10);
    color: var(--accent);
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
}

/* Section label */
.section-label {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* Charts and containers */
[data-testid="stVerticalBlock"] > div:has(canvas),
[data-testid="stPlotlyChart"],
[data-testid="stLineChart"] {
    background: #ffffff;
    border-radius: 18px;
    padding: 0.5rem;
}

/* Remove any dark backgrounds from generic containers */
div[data-testid="stContainer"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)
import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f7f4ee;
            --surface: #fffdf9;
            --surface-soft: #f4ede3;
            --border: #e7dccd;
            --text: #1f2937;
            --muted: #64748b;
            --primary: #a8612d;
            --primary-dark: #8b4f22;
            --primary-soft: #f4e2d2;
            --shadow: 0 10px 30px rgba(60, 41, 20, 0.08);
            --radius-lg: 22px;
            --radius-md: 16px;
            --radius-sm: 12px;
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], .main {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        header[data-testid="stHeader"] {
            background: rgba(247, 244, 238, 0.9) !important;
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fffdf9 0%, #f8f2e9 100%) !important;
            border-right: 1px solid var(--border);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text) !important;
            letter-spacing: -0.02em;
        }

        p, li {
            color: var(--muted) !important;
        }

        label {
            color: var(--muted) !important;
            font-weight: 700 !important;
        }

        ::selection {
            background: var(--primary) !important;
            color: white !important;
        }

        /* ---------- HERO ---------- */
        .hero-wrap {
            padding: 2rem 2rem 1.6rem 2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #8b5e34 0%, #c97a3d 55%, #e2a65e 100%);
            box-shadow: 0 18px 40px rgba(139, 94, 52, 0.18);
            margin-bottom: 1.5rem;
        }

        .hero-wrap * {
            color: white !important;
        }

        .hero-kicker {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.22);
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 0.85rem;
        }

        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 0.55rem;
            letter-spacing: -0.03em;
        }

        .hero-subtitle {
            font-size: 1.06rem;
            line-height: 1.65;
            max-width: 860px;
            color: rgba(255,255,255,0.96) !important;
        }

        .section-title {
            font-size: 1.6rem;
            font-weight: 800;
            margin: 1.2rem 0 1rem 0;
            color: var(--text) !important;
            letter-spacing: -0.02em;
        }

        /* ---------- CARDS ---------- */
        .project-card,
        .tech-list,
        .highlight-box,
        .footer-note,
        div[data-testid="metric-container"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow);
        }

        .project-card {
            padding: 1.2rem;
            min-height: 220px;
            margin-bottom: 1rem;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .project-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 16px 34px rgba(60, 41, 20, 0.10);
        }

        .project-title {
            font-size: 1.22rem;
            font-weight: 800;
            color: var(--text) !important;
            margin-bottom: 0.45rem;
        }

        .project-badge {
            display: inline-block;
            padding: 0.28rem 0.68rem;
            border-radius: 999px;
            background: var(--primary);
            color: white !important;
            font-size: 0.76rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .small-note {
            color: var(--muted) !important;
            font-size: 0.96rem;
            line-height: 1.6;
        }

        .tech-list,
        .highlight-box,
        .footer-note {
            padding: 1rem 1.1rem;
        }

        .highlight-box {
            border-left: 4px solid var(--primary) !important;
            background: #fdf2e8 !important;
        }

        .footer-note {
            background: #fff7ed !important;
            color: #9a3412 !important;
        }

        div[data-testid="metric-container"] {
            padding: 0.95rem !important;
        }

        div[data-testid="metric-container"] label {
            color: var(--muted) !important;
            font-weight: 700 !important;
        }

        /* ---------- SIDEBAR ---------- */
        .sidebar-brand {
            background: linear-gradient(135deg, #8b5e34 0%, #c97a3d 60%, #e2a65e 100%);
            border-radius: 22px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 14px 28px rgba(139, 94, 52, 0.16);
        }

        .sidebar-brand * {
            color: white !important;
        }

        .sidebar-brand-kicker {
            font-size: 0.76rem;
            font-weight: 700;
            opacity: 0.95;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .sidebar-brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }

        .sidebar-brand-subtitle {
            font-size: 0.88rem;
            line-height: 1.45;
            opacity: 0.96;
        }

        .sidebar-label {
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0.5rem 0 0.6rem 0;
        }

        .sidebar-footer {
            margin-top: 1.2rem;
            padding: 0.9rem;
            background: rgba(255,255,255,0.70);
            border: 1px solid var(--border);
            border-radius: 16px;
            color: var(--muted) !important;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        div[role="radiogroup"] > label {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            padding: 0.55rem 0.75rem !important;
            margin-bottom: 0.45rem !important;
            transition: all 0.18s ease;
        }

        div[role="radiogroup"] > label:hover {
            border-color: #d6b18b !important;
            background: #fbf3e8 !important;
        }

        div[role="radiogroup"] > label[data-checked="true"] {
            background: linear-gradient(135deg, #f5e7d7, #f3dbc0) !important;
            border-color: #c97a3d !important;
            box-shadow: 0 6px 16px rgba(139, 94, 52, 0.10);
        }

        div[role="radiogroup"] p {
            color: var(--text) !important;
            font-weight: 700 !important;
        }

        /* ---------- TABS ---------- */
        div[data-testid="stTabs"] {
            background: transparent !important;
        }

        button[data-baseweb="tab"] {
            position: relative !important;
            background: var(--surface) !important;
            color: var(--muted) !important;
            border: 1px solid var(--border) !important;
            border-radius: 999px !important;
            padding: 0.45rem 1rem !important;
            font-weight: 700 !important;
            margin-right: 0.45rem !important;
            box-shadow: 0 3px 10px rgba(60, 41, 20, 0.04);
        }

        button[data-baseweb="tab"]:hover {
            background: #f8eee1 !important;
            color: var(--primary) !important;
            border-color: #d6b18b !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #c97a3d, #8b5e34) !important;
            color: white !important;
            border-color: transparent !important;
            box-shadow: 0 6px 14px rgba(139, 94, 52, 0.18);
        }

        button[data-baseweb="tab"][aria-selected="true"] * {
            color: white !important;
        }

        /* remove Streamlit tab underline / separator */
        [data-testid="stTabs"] [role="tablist"] {
            gap: 0.15rem;
        }

        [data-testid="stTabs"] [role="tablist"]::before,
        [data-testid="stTabs"] [role="tablist"]::after,
        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            display: none !important;
            background: transparent !important;
            height: 0 !important;
        }

        /* ---------- FORMS ---------- */
        .stForm {
            background: rgba(255,253,249,0.82);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.15rem;
            box-shadow: var(--shadow);
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            background: white !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            box-shadow: 0 3px 10px rgba(60,41,20,0.04);
            color: var(--text) !important;
        }

        input, textarea {
            color: var(--text) !important;
            background: transparent !important;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] [aria-hidden="true"] {
            color: var(--text) !important;
            opacity: 1 !important;
            -webkit-text-fill-color: var(--text) !important;
        }

        /* ---------- BUTTONS ---------- */
        .stButton > button,
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #c97a3d, #8b5e34) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.62rem 1.25rem !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            line-height: 1.2 !important;
            box-shadow: 0 8px 18px rgba(139, 94, 52, 0.16);
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 24px rgba(139, 94, 52, 0.22);
            filter: brightness(1.02);
        }

        .stButton > button:active,
        .stFormSubmitButton > button:active {
            transform: translateY(0);
            box-shadow: 0 6px 14px rgba(139, 94, 52, 0.18);
        }

        .stButton > button:focus,
        .stFormSubmitButton > button:focus {
            outline: none !important;
            box-shadow: 0 0 0 0.18rem rgba(201, 122, 61, 0.20), 0 8px 18px rgba(139, 94, 52, 0.16) !important;
        }

        .stButton > button p,
        .stFormSubmitButton > button p,
        .stButton > button span,
        .stFormSubmitButton > button span {
            color: white !important;
        }

        /* ---------- DATA / CODE ---------- */
        div[data-testid="stDataFrame"] {
            background: white !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            overflow: hidden;
            box-shadow: var(--shadow);
        }

        code {
            background: #efe4d4 !important;
            color: var(--text) !important;
            padding: 0.15rem 0.4rem !important;
            border-radius: 8px !important;
            font-size: 0.92em !important;
            border: 1px solid #dcc8ae !important;
        }

        pre {
            background: #fffdf9 !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            box-shadow: 0 4px 12px rgba(60, 41, 20, 0.05);
        }

        pre code {
            background: transparent !important;
            color: var(--text) !important;
            border: none !important;
            padding: 0 !important;
        }

        div[data-baseweb="notification"] {
            border-radius: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f7f4ee;
            --surface: #fffdf9;
            --surface-soft: #f3ede4;
            --border: #e6ddd0;
            --text: #1f2937;
            --muted: #5f6b7a;
            --primary: #9a5b2e;
            --primary-hover: #7f4923;
            --secondary: #d6a36d;
            --shadow: 0 10px 28px rgba(60, 41, 20, 0.08);
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
            background: rgba(247, 244, 238, 0.88) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fffdf9 0%, #f7f1e8 100%) !important;
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

        ::-moz-selection {
            background: var(--primary) !important;
            color: white !important;
        }

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
            border: 1px solid rgba(255,255,255,0.20);
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

        .project-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: var(--shadow);
            min-height: 220px;
            margin-bottom: 1rem;
            transition: transform .18s ease, box-shadow .18s ease;
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
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow);
            padding: 1rem 1.1rem;
        }

        .highlight-box {
            border-left: 4px solid var(--primary);
            background: #fdf2e8;
        }

        .footer-note {
            background: #fff7ed;
            color: #9a3412 !important;
        }

        div[data-testid="metric-container"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            box-shadow: var(--shadow);
            padding: 0.95rem !important;
        }

        div[data-testid="metric-container"] label {
            color: var(--muted) !important;
            font-weight: 700 !important;
        }

        div[data-testid="stTabs"] {
            background: transparent !important;
        }

        button[data-baseweb="tab"] {
            background: var(--surface) !important;
            color: var(--muted) !important;
            border: 1px solid var(--border) !important;
            border-radius: 999px !important;
            padding: 0.45rem 1rem !important;
            font-weight: 700 !important;
            margin-right: 0.35rem !important;
            box-shadow: 0 3px 10px rgba(60, 41, 20, 0.04);
        }

        button[data-baseweb="tab"]:hover {
            background: #f8eee1 !important;
            color: var(--primary) !important;
            border-color: #d6b18b !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: var(--primary) !important;
            color: white !important;
            border-color: var(--primary) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] * {
            color: white !important;
        }

        .stForm {
            background: rgba(255,253,249,0.78);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
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

        /* Primary Button */
.stButton > button {
    background: linear-gradient(135deg, #c56a2d, #a3541f) !important;
    color: white !important;   /* 🔥 THIS FIXES YOUR ISSUE */
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease-in-out;
}

/* Hover */
.stButton > button:hover {
    background: linear-gradient(135deg, #d9773a, #b45f25) !important;
    transform: translateY(-1px);
}

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
        /* Fix selected text inside Streamlit selectboxes */
div[data-baseweb="select"] > div {
    color: var(--text) !important;
}

div[data-baseweb="select"] span {
    color: var(--text) !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] input {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

div[data-baseweb="select"] [aria-hidden="true"] {
    color: var(--text) !important;
    opacity: 1 !important;
}
        </style>
        """,
        unsafe_allow_html=True,
    )
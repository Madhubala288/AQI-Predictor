import streamlit as st
import textwrap


def load_professional_theme():

    css = """
    <style>

    /* =====================================================
       GLOBAL APP
    ===================================================== */

    .stApp {
        background: #080c12;
        color: #f8fafc;
    }

    .main {
        background: #080c12;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {
        background: #0d1420;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.8rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }


    /* =====================================================
       HEADINGS
    ===================================================== */

    h1 {
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #e2e8f0 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #cbd5e1 !important;
        font-weight: 650 !important;
    }


    /* =====================================================
       KPI CARDS
    ===================================================== */

    div[data-testid="metric-container"] {
        background: linear-gradient(
            145deg,
            #111827,
            #0f172a
        );

        border: 1px solid #263244;
        border-radius: 16px;

        padding: 20px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);

        transition: all 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }

    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-size: 0.82rem !important;
    }

    div[data-testid="metric-container"] div {
        color: #f8fafc;
    }


    /* =====================================================
       ALERTS
    ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #334155;
    }


    /* =====================================================
       DATAFRAME
    ===================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #1f2937;
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton > button,
    .stDownloadButton > button {

        border-radius: 10px;

        border: 1px solid #334155;

        background: #111827;

        color: #f8fafc;

        padding: 0.55rem 1.2rem;

        font-weight: 650;

        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {

        border-color: #3b82f6;

        background: #172033;

        color: white;
    }


    /* =====================================================
       SELECT BOX
    ===================================================== */

    div[data-baseweb="select"] > div {
        background: #111827;
        border-radius: 10px;
        border-color: #334155;
    }


    /* =====================================================
       RADIO BUTTONS
    ===================================================== */

    div[role="radiogroup"] label {
        color: #cbd5e1 !important;
    }


    /* =====================================================
       DIVIDERS
    ===================================================== */

    hr {
        border-color: #1f2937 !important;
    }


    /* =====================================================
       HERO CARD
    ===================================================== */

    .hero-card {

        position: relative;

        overflow: hidden;

        background:
            radial-gradient(
                circle at top right,
                rgba(59, 130, 246, 0.18),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #111827,
                #0f172a
            );

        border: 1px solid #263244;

        border-radius: 20px;

        padding: 32px;

        margin-bottom: 26px;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.30);
    }


    .hero-title {

        font-size: 2.35rem;

        font-weight: 850;

        color: #f8fafc;

        margin-bottom: 8px;

        letter-spacing: -0.8px;
    }


    .hero-subtitle {

        color: #94a3b8;

        font-size: 1rem;

        line-height: 1.6;

        margin-bottom: 18px;
    }


    /* =====================================================
       STATUS BADGE
    ===================================================== */

    .status-badge {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 0.78rem;

        font-weight: 700;

        background: rgba(22, 101, 52, 0.25);

        color: #86efac;

        border: 1px solid rgba(34, 197, 94, 0.35);
    }


    /* =====================================================
       LOCATION BADGE
    ===================================================== */

    .location-badge {

        display: inline-block;

        background: rgba(30, 64, 175, 0.18);

        color: #93c5fd;

        border: 1px solid rgba(59, 130, 246, 0.35);

        padding: 7px 14px;

        border-radius: 999px;

        font-size: 0.82rem;

        font-weight: 650;

        margin-bottom: 12px;
    }


    /* =====================================================
       SYSTEM STATUS
    ===================================================== */

    .system-status {

        display: flex;

        align-items: center;

        gap: 8px;

        color: #94a3b8;

        font-size: 0.82rem;

        margin-bottom: 20px;
    }


    .system-dot {

        width: 8px;

        height: 8px;

        border-radius: 50%;

        background: #22c55e;

        display: inline-block;

        box-shadow:
            0 0 8px rgba(34, 197, 94, 0.7);
    }


    /* =====================================================
       AQI STATUS CARD
    ===================================================== */

    .aqi-status-card {

        border-radius: 18px;

        padding: 28px;

        margin-top: 8px;

        margin-bottom: 28px;

        border: 1px solid #334155;

        background:
            linear-gradient(
                145deg,
                #111827,
                #0f172a
            );

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25);
    }


    .aqi-status-header {

        display: flex;

        justify-content: space-between;

        align-items: center;

        font-size: 0.95rem;

        color: #cbd5e1;

        margin-bottom: 15px;
    }


    .aqi-number {

        font-size: 4rem;

        font-weight: 850;

        line-height: 1;

        color: #f8fafc;

        margin-bottom: 6px;
    }


    .aqi-label {

        color: #94a3b8;

        font-size: 0.88rem;

        margin-bottom: 20px;
    }


    .aqi-advisory {

        color: #cbd5e1;

        font-size: 0.9rem;

        line-height: 1.6;

        border-top: 1px solid #334155;

        padding-top: 15px;
    }


    /* =====================================================
       AQI CATEGORY COLORS
    ===================================================== */

    .good {
        border-left: 5px solid #22c55e;
    }

    .fair {
        border-left: 5px solid #3b82f6;
    }

    .moderate {
        border-left: 5px solid #eab308;
    }

    .unhealthy {
        border-left: 5px solid #f97316;
    }

    .very-unhealthy {
        border-left: 5px solid #ef4444;
    }

    .hazardous {
        border-left: 5px solid #a855f7;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .professional-footer {

        text-align: center;

        color: #64748b;

        border-top: 1px solid #1f2937;

        padding-top: 25px;

        margin-top: 45px;

        font-size: 0.78rem;

        line-height: 1.7;
    }


    /* =====================================================
       SCROLLBAR
    ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0b0f14;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }


    </style>
    """

    st.markdown(
        textwrap.dedent(css),
        unsafe_allow_html=True
    )
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import math

from utils import get_aqi_category, get_health_advisory
from theme import load_professional_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AQI Forecasting System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD THEME
# ============================================================

load_professional_theme()


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_FILE = BASE_DIR / "predictions" / "predictions.csv"

REGISTRY_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "registry.json"
)

METRICS_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "metrics.json"
)

METADATA_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "metadata.json"
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN APP
    ============================== */

    .stApp {
        background-color: #0b1120;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }


    /* ==============================
       TEXT
    ============================== */

    h1 {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #cbd5e1 !important;
    }

    p {
        color: #94a3b8;
    }


    /* ==============================
       METRIC CARDS
    ============================== */

    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 750 !important;
    }


    /* ==============================
       BUTTONS
    ============================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }


    /* ==============================
       DATAFRAME
    ============================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #1e293b;
        border-radius: 14px;
        overflow: hidden;
    }


    /* ==============================
       ALERTS
    ============================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ==============================
       SELECTBOX
    ============================== */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }


    /* ==============================
       CARDS
    ============================== */

    .info-card {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
    }


    /* ==============================
       HERO
    ============================== */

    .hero-box {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172554 100%
        );

        border: 1px solid #263b63;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;

        box-shadow:
            0 15px 40px rgba(0,0,0,0.25);
    }


    /* ==============================
       STATUS
    ============================== */

    .status-online {
        background-color: #052e16;
        border: 1px solid #166534;
        color: #86efac;
        border-radius: 999px;
        padding: 7px 15px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }


    /* ==============================
       FOOTER
    ============================== */

    .footer-box {
        text-align: center;
        color: #64748b;
        border-top: 1px solid #1e293b;
        padding-top: 25px;
        margin-top: 50px;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_json_file(file_path):

    if not file_path.exists():
        return {}

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception:
        return {}


def section_title(title, subtitle=None):

    st.subheader(title)

    if subtitle:
        st.caption(subtitle)


def show_hero():

    st.markdown(
        """
        <div class="hero-box">
        """,
        unsafe_allow_html=True
    )

    st.title("🌍 AQI Forecasting System")

    st.write(
        "AI-powered 72-hour Air Quality Forecasting "
        "with Explainable Machine Learning"
    )

    st.markdown(
        '<span class="status-online">● Production Monitoring</span>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


def show_aqi_card(aqi, category, advisory):

    st.markdown("### 🎯 Current Air Quality")

    if category == "Good":
        st.success(
            f"🟢 **{category}**"
        )

    elif category == "Fair":
        st.info(
            f"🔵 **{category}**"
        )

    elif category == "Moderate":
        st.warning(
            f"🟡 **{category}**"
        )

    elif category == "Poor":
        st.warning(
            f"🟠 **{category}**"
        )

    else:
        st.error(
            f"🔴 **{category}**"
        )

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "Predicted AQI",
            f"{aqi:.2f}"
        )

    with col2:

        st.info(
            f"💡 **Health Advisory**\n\n{advisory}"
        )


# ============================================================
# LOAD PREDICTIONS
# ============================================================

if not PREDICTION_FILE.exists():

    st.error("❌ Prediction file not found.")

    st.info(
        "Please run the prediction pipeline first."
    )

    st.stop()


try:

    df = pd.read_csv(
        PREDICTION_FILE
    )

except Exception as e:

    st.error(
        f"❌ Unable to load prediction data: {e}"
    )

    st.stop()


# ============================================================
# VALIDATE DATA
# ============================================================

required_columns = [
    "Timestamp",
    "Predicted_AQI"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        f"❌ Missing columns: {missing_columns}"
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df["Predicted_AQI"] = pd.to_numeric(
    df["Predicted_AQI"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "Timestamp",
        "Predicted_AQI"
    ]
)

df = df.sort_values(
    "Timestamp"
).reset_index(
    drop=True
)


if df.empty:

    st.error(
        "❌ No valid prediction data available."
    )

    st.stop()


# ============================================================
# LOAD MODEL INFORMATION
# ============================================================

registry = load_json_file(
    REGISTRY_FILE
)

metrics = load_json_file(
    METRICS_FILE
)

metadata = load_json_file(
    METADATA_FILE
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🌍 AQI Predictor"
    )

    st.caption(
        "Air Quality Intelligence"
    )

    st.divider()

    st.subheader("🧭 Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "3-Day Forecast",
            "Prediction History",
            "Model Information"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("📍 Location")

    city = st.selectbox(
        "Select City",
        [
            "Karachi"
        ]
    )

    st.caption(
        "Currently available data: Karachi"
    )

    st.divider()

    st.subheader("⚙️ System")

    st.success(
        "System Online"
    )

    st.caption(
        "Prediction pipeline active"
    )


# ============================================================
# LATEST PREDICTION
# ============================================================

latest = df.iloc[-1]

latest_aqi = float(
    latest["Predicted_AQI"]
)

category = get_aqi_category(
    latest_aqi
)

advisory = get_health_advisory(
    category
)


# ============================================================
# DASHBOARD — PROFESSIONAL V2
# ============================================================

if page == "Dashboard":

    # ========================================================
    # HERO HEADER
    # ========================================================

    st.title("🌍 AQI Forecasting System")

    st.caption(
        "AI-powered Air Quality Intelligence • "
        "72-Hour Forecasting • Machine Learning"
    )

    st.success(
        f"🟢 System Online  |  📍 Forecast Location: {city}"
    )

    st.divider()


    # ========================================================
    # GET LATEST DATA
    # ========================================================

    latest = df.iloc[-1]

    latest_aqi = float(
        latest["Predicted_AQI"]
    )

    category = get_aqi_category(
        latest_aqi
    )

    advisory = get_health_advisory(
        category
    )

    latest_timestamp = latest[
        "Timestamp"
    ]


    # ========================================================
    # TOP KPI SECTION
    # ========================================================

    st.subheader("📊 Air Quality Overview")

    st.caption(
        "Latest prediction and forecasting system status"
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            label="Predicted AQI",
            value=f"{latest_aqi:.2f}"
        )


    with col2:

        st.metric(
            label="AQI Category",
            value=category
        )


    with col3:

        st.metric(
            label="Forecast Horizon",
            value=f"{len(df)} Hours"
        )


    with col4:

        forecast_days = math.ceil(
            len(df) / 24
        )

        st.metric(
            label="Forecast Days",
            value=forecast_days
        )


    st.divider()


    # ========================================================
    # CURRENT AIR QUALITY
    # ========================================================

    st.subheader("🎯 Current Air Quality")

    st.caption(
        "Latest machine-learning prediction"
    )


    aqi_col1, aqi_col2 = st.columns(
        [1, 2]
    )


    with aqi_col1:

        st.metric(
            label="Predicted AQI",
            value=f"{latest_aqi:.2f}"
        )

        if category == "Good":

            st.success(
                "🟢 Good Air Quality"
            )

        elif category == "Fair":

            st.info(
                "🔵 Fair Air Quality"
            )

        elif category == "Moderate":

            st.warning(
                "🟡 Moderate Air Quality"
            )

        elif category == "Poor":

            st.warning(
                "🟠 Poor Air Quality"
            )

        else:

            st.error(
                "🔴 Very Poor Air Quality"
            )


    with aqi_col2:

        st.info(
            f"💡 **Health Advisory**\n\n"
            f"{advisory}"
        )


    st.divider()


    # ========================================================
    # FORECAST TIMESTAMP
    # ========================================================

    st.subheader("🕒 Latest Forecast")

    forecast_time = latest_timestamp.strftime(
        "%d %B %Y, %I:%M %p"
    )

    st.info(
        f"Prediction generated at **{forecast_time}**"
    )


    st.divider()


    # ========================================================
    # 72-HOUR FORECAST
    # ========================================================

    st.subheader("📈 72-Hour AQI Forecast")

    st.caption(
        "Predicted AQI trend for the upcoming forecast period"
    )


    chart_data = (
        df
        .set_index("Timestamp")[
            ["Predicted_AQI"]
        ]
    )


    st.line_chart(
        chart_data,
        height=420
    )


    st.divider()


    # ========================================================
    # DAILY SUMMARY
    # ========================================================

    st.subheader("📅 Daily AQI Summary")

    st.caption(
        "Average, minimum and maximum predicted AQI"
    )


    temp_df = df.copy()

    temp_df["Date"] = (
        temp_df["Timestamp"]
        .dt.date
    )


    daily_summary = (
        temp_df
        .groupby("Date")[
            "Predicted_AQI"
        ]
        .agg(
            Average_AQI="mean",
            Minimum_AQI="min",
            Maximum_AQI="max"
        )
        .reset_index()
    )


    daily_summary[
        "Average_AQI"
    ] = daily_summary[
        "Average_AQI"
    ].round(2)


    daily_summary[
        "Minimum_AQI"
    ] = daily_summary[
        "Minimum_AQI"
    ].round(2)


    daily_summary[
        "Maximum_AQI"
    ] = daily_summary[
        "Maximum_AQI"
    ].round(2)


    st.dataframe(
        daily_summary,
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ========================================================
    # FORECAST INSIGHTS
    # ========================================================

    st.subheader("🔎 Forecast Insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)


    max_aqi = float(
        df["Predicted_AQI"].max()
    )

    min_aqi = float(
        df["Predicted_AQI"].min()
    )

    avg_aqi = float(
        df["Predicted_AQI"].mean()
    )


    with insight_col1:

        st.metric(
            "Maximum Forecast AQI",
            f"{max_aqi:.2f}"
        )


    with insight_col2:

        st.metric(
            "Minimum Forecast AQI",
            f"{min_aqi:.2f}"
        )


    with insight_col3:

        st.metric(
            "Average Forecast AQI",
            f"{avg_aqi:.2f}"
        )


    st.divider()


    # ========================================================
    # DOWNLOAD FORECAST
    # ========================================================

    st.subheader("⬇️ Download Forecast")

    st.caption(
        "Export the complete machine-learning prediction dataset"
    )


    csv_data = (
        df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
    label="⬇️ Download Predictions CSV",
    data=csv_data,
    file_name="aqi_predictions.csv",
    mime="text/csv",
    key="dashboard_predictions_download"
)

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    section_title(
        "📊 Air Quality Overview",
        "Latest prediction and forecasting system status"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Predicted AQI",
            f"{latest_aqi:.2f}"
        )

    with col2:

        st.metric(
            "AQI Category",
            category
        )

    with col3:

        st.metric(
            "Forecast Horizon",
            f"{len(df)} hours"
        )

    with col4:

        forecast_days = math.ceil(
            len(df) / 24
        )

        st.metric(
            "Forecast Days",
            forecast_days
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT AIR QUALITY
    # --------------------------------------------------------

    show_aqi_card(
        latest_aqi,
        category,
        advisory
    )

    st.divider()

    # --------------------------------------------------------
    # LATEST FORECAST
    # --------------------------------------------------------

    section_title(
        "🕒 Latest Forecast",
        "Most recent prediction generated by the ML system"
    )

    forecast_time = latest[
        "Timestamp"
    ].strftime(
        "%d %B %Y, %I:%M %p"
    )

    st.info(
        f"Latest prediction timestamp: **{forecast_time}**"
    )

    st.divider()

    # --------------------------------------------------------
    # FORECAST CHART
    # --------------------------------------------------------

    section_title(
        "📈 72-Hour AQI Forecast",
        "Predicted AQI trend for the upcoming forecast period"
    )

    chart_data = (
        df
        .set_index(
            "Timestamp"
        )[
            ["Predicted_AQI"]
        ]
    )

    st.line_chart(
        chart_data,
        height=400
    )

    st.divider()

    # --------------------------------------------------------
    # DAILY SUMMARY
    # --------------------------------------------------------

    section_title(
        "📅 Daily AQI Summary",
        "Average, minimum and maximum predicted AQI"
    )

    temp_df = df.copy()

    temp_df["Date"] = (
        temp_df["Timestamp"]
        .dt.date
    )

    daily_summary = (
        temp_df
        .groupby("Date")["Predicted_AQI"]
        .agg(
            Average_AQI="mean",
            Minimum_AQI="min",
            Maximum_AQI="max"
        )
        .reset_index()
    )

    for column in [
        "Average_AQI",
        "Minimum_AQI",
        "Maximum_AQI"
    ]:

        daily_summary[column] = (
            daily_summary[column]
            .round(2)
        )

    st.dataframe(
        daily_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    section_title(
        "⬇️ Download Forecast",
        "Download the complete prediction dataset"
    )

    csv_data = (
        df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Predictions CSV",
        data=csv_data,
        file_name="aqi_predictions.csv",
        mime="text/csv"
    )


# ============================================================
# 3-DAY FORECAST
# ============================================================

elif page == "3-Day Forecast":

    show_hero()

    st.info(
        f"📍 **{city} — 72 Hour Forecast**"
    )

    forecast_df = df.copy()

    forecast_df["Date"] = (
        forecast_df["Timestamp"]
        .dt.date
    )

    st.divider()

    # --------------------------------------------------------
    # DAILY SUMMARY
    # --------------------------------------------------------

    section_title(
        "📅 Daily Forecast Summary",
        "Predicted AQI statistics for each forecast day"
    )

    daily_summary = (
        forecast_df
        .groupby("Date")["Predicted_AQI"]
        .agg(
            Average_AQI="mean",
            Minimum_AQI="min",
            Maximum_AQI="max"
        )
        .reset_index()
    )

    for column in [
        "Average_AQI",
        "Minimum_AQI",
        "Maximum_AQI"
    ]:

        daily_summary[column] = (
            daily_summary[column]
            .round(2)
        )

    st.dataframe(
        daily_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # DAILY CHART
    # --------------------------------------------------------

    section_title(
        "📈 Daily AQI Trend"
    )

    daily_chart = (
        daily_summary
        .set_index("Date")[
            [
                "Average_AQI",
                "Minimum_AQI",
                "Maximum_AQI"
            ]
        ]
    )

    st.line_chart(
        daily_chart,
        height=400
    )

    st.divider()

    # --------------------------------------------------------
    # HOURLY FORECAST
    # --------------------------------------------------------

    section_title(
        "🕒 Hourly AQI Forecast",
        "Detailed predictions for every forecast hour"
    )

    hourly_display = forecast_df[
        [
            "Timestamp",
            "Predicted_AQI"
        ]
    ].copy()

    hourly_display["Predicted_AQI"] = (
        hourly_display["Predicted_AQI"]
        .round(3)
    )

    st.dataframe(
        hourly_display,
        width="stretch",
        hide_index=True
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

elif page == "Prediction History":

    show_hero()

    section_title(
        "📚 Prediction History",
        "Historical predictions generated by the forecasting system"
    )

    history = df.copy()

    history["Date"] = (
        history["Timestamp"]
        .dt.strftime("%d %B %Y")
    )

    history["Time"] = (
        history["Timestamp"]
        .dt.strftime("%I:%M %p")
    )

    history["Category"] = (
        history["Predicted_AQI"]
        .apply(get_aqi_category)
    )

    history["Predicted_AQI"] = (
        history["Predicted_AQI"]
        .round(3)
    )

    st.dataframe(
        history[
            [
                "Date",
                "Time",
                "Predicted_AQI",
                "Category"
            ]
        ],
        width="stretch",
        hide_index=True
    )

    st.divider()

    section_title(
        "📈 Prediction Trend"
    )

    history_chart = (
        df
        .set_index("Timestamp")[
            ["Predicted_AQI"]
        ]
    )

    st.line_chart(
        history_chart,
        height=400
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    show_hero()

    section_title(
        "🤖 Machine Learning Model",
        "Production model information and evaluation metrics"
    )

    # --------------------------------------------------------
    # MODEL DETAILS
    # --------------------------------------------------------

    model_name = registry.get(
        "current_best_model",
        "Unknown"
    )

    model_type = registry.get(
        "model_type",
        "Unknown"
    )

    model_version = registry.get(
        "model_version",
        "Unknown"
    )

    model_status = registry.get(
        "status",
        "Unknown"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Model",
            model_name
        )

    with col2:

        st.metric(
            "Version",
            model_version
        )

    with col3:

        st.metric(
            "Algorithm",
            model_type
        )

    with col4:

        st.metric(
            "Status",
            model_status
        )

    st.divider()

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    section_title(
        "📊 Model Performance",
        "Evaluation metrics from the registered production model"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        mae = metrics.get(
            "MAE",
            0
        )

        st.metric(
            "MAE",
            f"{float(mae):.4f}"
        )

    with col2:

        rmse = metrics.get(
            "RMSE",
            0
        )

        st.metric(
            "RMSE",
            f"{float(rmse):.4f}"
        )

    with col3:

        r2 = metrics.get(
            "R2",
            0
        )

        st.metric(
            "R² Score",
            f"{float(r2):.4f}"
        )

    st.divider()

    # --------------------------------------------------------
    # MODEL REGISTRY
    # --------------------------------------------------------

    section_title(
        "🗃️ Model Registry",
        "Registered model version and deployment status"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Version:** {model_version}"
        )

        st.write(
            f"**Status:** {model_status}"
        )

    with col2:

        st.write(
            "**Registry Location:**"
        )

        st.code(
            "model_registry/v1",
            language="text"
        )

    if str(model_status).lower() == "production":

        st.success(
            "✅ Production model is active."
        )

    else:

        st.warning(
            f"Model status: {model_status}"
        )

    st.divider()

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    section_title(
        "📋 Model Metadata",
        "Technical information stored with the registered model"
    )

    if metadata:

        with st.expander(
            "🔍 View Model Metadata"
        ):

            st.json(
                metadata
            )

    else:

        st.warning(
            "Metadata file was not found."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-box">
        <b>AQI Forecasting System</b><br>
        Machine Learning • Explainable AI • Automated Forecasting
        <br><br>
        Built for academic, research and portfolio use.
    </div>
    """,
    unsafe_allow_html=True
)
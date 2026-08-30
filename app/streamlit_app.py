import streamlit as st
import pandas as pd
import json
from pathlib import Path

from utils import get_aqi_category, get_health_advisory


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
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_FILE = (
    BASE_DIR
    / "predictions"
    / "predictions.csv"
)

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
# LOAD JSON FILE
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


# ============================================================
# LOAD PREDICTION DATA
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
# VALIDATE REQUIRED COLUMNS
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

df = (
    df
    .sort_values("Timestamp")
    .reset_index(drop=True)
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

    st.title("🌍 AQI Predictor")

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
# COMMON DATA
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

forecast_hours = len(df)

forecast_days = (
    df["Timestamp"]
    .dt.date
    .nunique()
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🌍 AQI Forecasting System"
)

st.caption(
    "AI-powered Air Quality Intelligence | "
    "72-Hour Forecasting | Machine Learning"
)

st.success(
    f"🟢 System Online | 📍 Forecast Location: {city}"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header(
        "📊 Air Quality Overview"
    )

    st.caption(
        "Latest prediction and forecasting system status"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

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
            f"{forecast_hours} Hours"
        )

    with col4:

        st.metric(
            "Forecast Days",
            forecast_days
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT AIR QUALITY
    # --------------------------------------------------------

    st.header(
        "🎯 Current Air Quality"
    )

    aqi_col1, aqi_col2 = st.columns(
        [1, 2]
    )

    with aqi_col1:

        st.metric(
            "Predicted AQI",
            f"{latest_aqi:.2f}"
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

        elif category == "Unhealthy":

            st.warning(
                "🟠 Unhealthy Air Quality"
            )

        elif category == "Very Unhealthy":

            st.error(
                "🔴 Very Unhealthy Air Quality"
            )

        else:

            st.error(
                "🟣 Hazardous Air Quality"
            )

    with aqi_col2:

        st.info(
            f"💡 Health Advisory\n\n"
            f"{advisory}"
        )

    st.divider()

    # --------------------------------------------------------
    # LATEST FORECAST
    # --------------------------------------------------------

    st.header(
        "🕒 Latest Forecast"
    )

    forecast_time = (
        latest["Timestamp"]
        .strftime(
            "%d %B %Y, %I:%M %p"
        )
    )

    st.info(
        f"Prediction generated at "
        f"**{forecast_time}**"
    )

    st.divider()

    # --------------------------------------------------------
    # 72-HOUR FORECAST
    # --------------------------------------------------------

    st.header(
        "📈 72-Hour AQI Forecast"
    )

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
        width="stretch",
        height=400
    )

    st.divider()

    # --------------------------------------------------------
    # DAILY SUMMARY
    # --------------------------------------------------------

    st.header(
        "📅 Daily AQI Summary"
    )

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
    # FORECAST INSIGHTS
    # --------------------------------------------------------

    st.header(
        "🔎 Forecast Insights"
    )

    max_aqi = float(
        df["Predicted_AQI"].max()
    )

    min_aqi = float(
        df["Predicted_AQI"].min()
    )

    avg_aqi = float(
        df["Predicted_AQI"].mean()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Maximum Forecast AQI",
            f"{max_aqi:.2f}"
        )

    with col2:

        st.metric(
            "Minimum Forecast AQI",
            f"{min_aqi:.2f}"
        )

    with col3:

        st.metric(
            "Average Forecast AQI",
            f"{avg_aqi:.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.header(
        "⬇️ Download Forecast"
    )

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
        key="dashboard_download"
    )


# ============================================================
# 3-DAY FORECAST
# ============================================================

elif page == "3-Day Forecast":

    st.header(
        "📅 3-Day AQI Forecast"
    )

    st.info(
        f"📍 {city} | 72-Hour Forecast"
    )

    forecast_df = df.copy()

    forecast_df["Date"] = (
        forecast_df["Timestamp"]
        .dt.date
    )

    # --------------------------------------------------------
    # DAILY SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "📊 Daily Forecast Summary"
    )

    daily_summary = (
        forecast_df
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

    st.subheader(
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
        width="stretch",
        height=400
    )

    st.divider()

    # --------------------------------------------------------
    # HOURLY FORECAST
    # --------------------------------------------------------

    st.subheader(
        "🕒 Hourly AQI Forecast"
    )

    st.caption(
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

    st.header(
        "📚 Prediction History"
    )

    st.caption(
        "Historical predictions generated by the forecasting system"
    )

    history = df.copy()

    history["Date"] = (
        history["Timestamp"]
        .dt.strftime(
            "%d %B %Y"
        )
    )

    history["Time"] = (
        history["Timestamp"]
        .dt.strftime(
            "%I:%M %p"
        )
    )

    history["Category"] = (
        history["Predicted_AQI"]
        .apply(
            get_aqi_category
        )
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

    st.subheader(
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
        width="stretch",
        height=400
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    st.header(
        "🤖 Machine Learning Model"
    )

    st.caption(
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
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    st.subheader(
        "📊 Model Performance"
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

    st.subheader(
        "🗃️ Model Registry"
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
            "**Registry Path:**"
        )

        st.code(
            "model_registry/v1"
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

    st.subheader(
        "📋 Model Metadata"
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

st.divider()

st.caption(
    "AQI Forecasting System | "
    "Machine Learning | Explainable AI | "
    "Automated Forecasting"
)

st.caption(
    "Built for academic, research and portfolio use."
)
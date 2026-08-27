import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

from utils import get_aqi_category, get_health_advisory


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AQI Forecasting System",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_FILE = (
    BASE_DIR / "predictions" / "predictions.csv"
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
# HELPER FUNCTION
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
# LOAD PREDICTIONS
# ============================================================

if not PREDICTION_FILE.exists():

    st.error(
        "Prediction file not found."
    )

    st.info(
        "Please run Phase 11B first."
    )

    st.stop()


try:

    df = pd.read_csv(
        PREDICTION_FILE
    )

except Exception as e:

    st.error(
        f"Unable to load prediction data: {e}"
    )

    st.stop()


# ============================================================
# VALIDATE COLUMNS
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
        f"Missing columns: {missing_columns}"
    )

    st.stop()


# ============================================================
# DATA CLEANING
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
).reset_index(drop=True)


if df.empty:

    st.error(
        "No valid prediction data available."
    )

    st.stop()


# ============================================================
# LOAD MODEL REGISTRY INFORMATION
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
# HEADER
# ============================================================

st.title(
    "🌍 AQI Forecasting System"
)

st.write(
    "An end-to-end machine learning system "
    "for 72-hour air quality forecasting."
)

st.caption(
    "Dashboard updated: "
    + datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🧭 Navigation"
)

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "3-Day Forecast",
        "Prediction History",
        "Model Information"
    ]
)


# ============================================================
# CITY SELECTION
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📍 Select City"
)

city = st.sidebar.selectbox(
    "City",
    [
        "Karachi"
    ]
)

st.sidebar.caption(
    "Currently available data: Karachi"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header(
        "📊 AQI Dashboard"
    )

    st.info(
        f"Forecast location: **{city}**"
    )


    # ========================================================
    # LATEST PREDICTION
    # ========================================================

    # IMPORTANT:
    # iloc[-1] gives the latest chronological record.

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


    # ========================================================
    # TOP METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Latest Predicted AQI",
            f"{latest_aqi:.2f}"
        )


    with col2:

        st.metric(
            "AQI Category",
            category
        )


    with col3:

        st.metric(
            "Forecast Hours",
            len(df)
        )


    with col4:

        st.metric(
            "Forecast Days",
            df["Timestamp"].dt.date.nunique()
        )


    st.divider()


    # ========================================================
    # LATEST PREDICTION TIME
    # ========================================================

    st.subheader(
        "🕐 Latest Forecast"
    )

    st.write(
        latest["Timestamp"].strftime(
            "%d %B %Y, %I:%M %p"
        )
    )


    st.divider()


    # ========================================================
    # HEALTH ADVISORY
    # ========================================================

    st.subheader(
        "🩺 Health Advisory"
    )


    if category == "Good":

        st.success(
            advisory
        )

    elif category == "Fair":

        st.info(
            advisory
        )

    elif category == "Moderate":

        st.warning(
            advisory
        )

    else:

        st.error(
            advisory
        )


    st.divider()


    # ========================================================
    # AQI FORECAST CHART
    # ========================================================

    st.subheader(
        "📈 72-Hour AQI Forecast"
    )

    chart_data = (
        df
        .set_index("Timestamp")[
            ["Predicted_AQI"]
        ]
    )

    st.line_chart(
        chart_data
    )


    st.divider()


    # ========================================================
    # DAILY SUMMARY
    # ========================================================

    st.subheader(
        "📅 Daily AQI Summary"
    )

    temp_df = df.copy()

    temp_df["Date"] = (
        temp_df["Timestamp"].dt.date
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
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.subheader(
        "📥 Download Predictions"
    )

    csv_data = (
        df.to_csv(
            index=False
        )
        .encode("utf-8")
    )

    st.download_button(
        label="Download Predictions CSV",
        data=csv_data,
        file_name="aqi_predictions.csv",
        mime="text/csv"
    )


# ============================================================
# 3-DAY FORECAST
# ============================================================

elif page == "3-Day Forecast":

    st.header(
        "📅 72-Hour AQI Forecast"
    )

    st.info(
        f"Forecast location: **{city}**"
    )


    # ========================================================
    # DAILY SUMMARY
    # ========================================================

    forecast_df = df.copy()

    forecast_df["Date"] = (
        forecast_df[
            "Timestamp"
        ].dt.date
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


    st.subheader(
        "📊 Daily Forecast Summary"
    )

    st.dataframe(
        daily_summary,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ========================================================
    # DAILY CHART
    # ========================================================

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
        daily_chart
    )


    st.divider()


    # ========================================================
    # HOURLY FORECAST
    # ========================================================

    st.subheader(
        "🕐 Hourly Forecast"
    )

    hourly_display = forecast_df.copy()

    hourly_display[
        "Predicted_AQI"
    ] = (
        hourly_display[
            "Predicted_AQI"
        ].round(3)
    )


    st.dataframe(
        hourly_display[
            [
                "Timestamp",
                "Predicted_AQI"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

elif page == "Prediction History":

    st.header(
        "📚 Prediction History"
    )

    st.write(
        "Historical prediction records "
        "generated by the forecasting system."
    )


    history = df.copy()

    history["Date"] = (
        history[
            "Timestamp"
        ].dt.strftime(
            "%d %B %Y"
        )
    )

    history["Time"] = (
        history[
            "Timestamp"
        ].dt.strftime(
            "%I:%M %p"
        )
    )

    history["Category"] = (
        history[
            "Predicted_AQI"
        ].apply(
            get_aqi_category
        )
    )

    history["Predicted_AQI"] = (
        history[
            "Predicted_AQI"
        ].round(3)
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
        use_container_width=True,
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
        history_chart
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    st.header(
        "🤖 Model Information"
    )

    st.write(
        "The dashboard uses the production-ready "
        "model registered in Phase 10."
    )


    # ========================================================
    # MODEL DETAILS
    # ========================================================

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
            "Type",
            model_type
        )


    with col4:

        st.metric(
            "Status",
            model_status
        )


    st.divider()


    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    st.subheader(
        "📊 Model Performance"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "MAE",
            f"{metrics.get('MAE', 0):.4f}"
        )


    with col2:

        st.metric(
            "RMSE",
            f"{metrics.get('RMSE', 0):.4f}"
        )


    with col3:

        st.metric(
            "R² Score",
            f"{metrics.get('R2', 0):.4f}"
        )


    st.divider()


    # ========================================================
    # REGISTRY
    # ========================================================

    st.subheader(
        "🗂️ Model Registry"
    )

    st.write(
        f"**Version:** {model_version}"
    )

    st.write(
        f"**Status:** {model_status}"
    )

    st.write(
        "**Registry Path:** model_registry/v1"
    )


    if model_status == "Production":

        st.success(
            "Production model is active."
        )

    else:

        st.warning(
            f"Model status: {model_status}"
        )


    st.divider()


    # ========================================================
    # METADATA
    # ========================================================

    st.subheader(
        "📋 Model Metadata"
    )

    if metadata:

        st.json(
            metadata
        )

    else:

        st.warning(
            "Metadata file was not found."
        )
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


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

PREDICTION_FILE = BASE_DIR / "predictions" / "predictions.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_aqi_category(aqi):
    """
    OpenWeather AQI scale:
    1 = Good
    2 = Fair
    3 = Moderate
    4 = Poor
    5 = Very Poor
    """

    if aqi < 1.5:
        return "Good"

    elif aqi < 2.5:
        return "Fair"

    elif aqi < 3.5:
        return "Moderate"

    elif aqi < 4.5:
        return "Poor"

    else:
        return "Very Poor"


def get_health_advisory(category):

    advisories = {
        "Good":
            "Air quality is good. Outdoor activities are generally safe.",

        "Fair":
            "Air quality is acceptable for most people.",

        "Moderate":
            "Sensitive individuals should consider reducing prolonged outdoor exposure.",

        "Poor":
            "Consider limiting prolonged outdoor activities.",

        "Very Poor":
            "Avoid prolonged outdoor exposure and take appropriate precautions."
    }

    return advisories.get(
        category,
        "No health advisory available."
    )


# ============================================================
# HEADER
# ============================================================

st.title("🌍 AQI Forecasting System")

st.write(
    "An end-to-end machine learning system "
    "for 72-hour air quality forecasting."
)

st.caption(
    f"Dashboard updated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "3-Day Forecast",
        "Model Information"
    ]
)


# ============================================================
# LOAD PREDICTIONS
# ============================================================

if not PREDICTION_FILE.exists():

    st.error(
        "Prediction file not found. "
        "Please run Phase 11B first."
    )

    st.stop()


try:

    df = pd.read_csv(PREDICTION_FILE)

except Exception as e:

    st.error(
        f"Unable to load prediction data: {e}"
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
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Missing required columns: {missing_columns}"
    )

    st.stop()


df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df["Predicted_AQI"] = pd.to_numeric(
    df["Predicted_AQI"],
    errors="coerce"
)

df = df.dropna(
    subset=["Timestamp", "Predicted_AQI"]
)

df = df.sort_values("Timestamp")


if df.empty:

    st.error("No valid prediction data available.")

    st.stop()


# ============================================================
# DASHBOARD PAGE
# ============================================================

if page == "Dashboard":

    st.header("📊 AQI Dashboard")

    latest = df.iloc[0]

    latest_aqi = float(latest["Predicted_AQI"])

    category = get_aqi_category(latest_aqi)

    advisory = get_health_advisory(category)


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

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


    st.divider()


    # --------------------------------------------------------
    # HEALTH ADVISORY
    # --------------------------------------------------------

    st.subheader("🩺 Health Advisory")

    if category == "Good":

        st.success(advisory)

    elif category == "Fair":

        st.info(advisory)

    elif category == "Moderate":

        st.warning(advisory)

    else:

        st.error(advisory)


    st.divider()


    # --------------------------------------------------------
    # AQI FORECAST CHART
    # --------------------------------------------------------

    st.subheader("📈 AQI Forecast")

    chart_data = df.set_index("Timestamp")[
        ["Predicted_AQI"]
    ]

    st.line_chart(chart_data)


    st.divider()


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.subheader("📥 Download Forecast")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Predictions CSV",
        data=csv_data,
        file_name="aqi_predictions.csv",
        mime="text/csv"
    )


# ============================================================
# 3-DAY FORECAST PAGE
# ============================================================

elif page == "3-Day Forecast":

    st.header("📅 72-Hour AQI Forecast")


    # --------------------------------------------------------
    # DAILY SUMMARY
    # --------------------------------------------------------

    forecast_df = df.copy()

    forecast_df["Date"] = (
        forecast_df["Timestamp"]
        .dt.date
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


    st.subheader("Daily Forecast Summary")


    display_summary = daily_summary.copy()

    display_summary[
        "Average_AQI"
    ] = display_summary[
        "Average_AQI"
    ].round(2)

    display_summary[
        "Minimum_AQI"
    ] = display_summary[
        "Minimum_AQI"
    ].round(2)

    display_summary[
        "Maximum_AQI"
    ] = display_summary[
        "Maximum_AQI"
    ].round(2)


    st.dataframe(
        display_summary,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # --------------------------------------------------------
    # FULL HOURLY FORECAST
    # --------------------------------------------------------

    st.subheader("Hourly Forecast")

    hourly_display = forecast_df.copy()

    hourly_display[
        "Predicted_AQI"
    ] = hourly_display[
        "Predicted_AQI"
    ].round(3)


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
# MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    st.header("🤖 Model Information")

    st.write(
        "The dashboard uses the production-ready "
        "machine learning model registered in Phase 10."
    )


    st.info(
        "Production Model: Tuned Random Forest"
    )

    st.write(
        "**Model Type:** RandomForestRegressor"
    )

    st.write(
        "**Model Version:** v1"
    )

    st.write(
        "**Forecast Horizon:** 72 hours"
    )

    st.write(
        "**Evaluation R²:** 0.9932"
    )

    st.write(
        "**Evaluation RMSE:** 0.1069"
    )

    st.write(
        "**Evaluation MAE:** 0.0422"
    )


    st.success(
        "Model Registry v1 is being used "
        "for the current forecasting system."
    )
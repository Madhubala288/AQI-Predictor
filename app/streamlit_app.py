import streamlit as st
import pandas as pd
from pathlib import Path

from utils import get_aqi_category, get_health_advisory

try:
    from theme import load_professional_theme
    load_professional_theme()
except Exception:
    pass


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Karachi AQI Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_FILE = (
    BASE_DIR / "predictions" / "predictions.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

if not PREDICTION_FILE.exists():

    st.error("❌ Prediction data not found.")

    st.info(
        "Please run the prediction pipeline first."
    )

    st.stop()


try:

    df = pd.read_csv(PREDICTION_FILE)

except Exception as e:

    st.error(
        f"❌ Unable to load prediction data: {e}"
    )

    st.stop()


# ============================================================
# VALIDATION
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
# LATEST DATA
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
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">
            🌍 Karachi AQI — What to expect next
        </div>
        <div class="hero-subtitle">
            Machine Learning powered air-quality forecasting
            with Explainable AI.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AQI LEGEND
# ============================================================

st.markdown("### AQI Health Categories")

legend_col1, legend_col2, legend_col3, legend_col4, legend_col5 = st.columns(5)

with legend_col1:
    st.success("🟢 Good")

with legend_col2:
    st.info("🔵 Fair")

with legend_col3:
    st.warning("🟡 Moderate")

with legend_col4:
    st.warning("🟠 Poor")

with legend_col5:
    st.error("🔴 Very Poor")


st.divider()


# ============================================================
# CURRENT AIR QUALITY
# ============================================================

st.subheader("🌍 Current Air Quality")

col1, col2 = st.columns(
    [1, 2]
)

with col1:

    st.metric(
        "Predicted AQI",
        f"{latest_aqi:.2f}"
    )

    if category == "Good":

        st.success("🟢 Good Air Quality")

    elif category == "Fair":

        st.info("🔵 Fair Air Quality")

    elif category == "Moderate":

        st.warning("🟡 Moderate Air Quality")

    elif category == "Poor":

        st.warning("🟠 Poor Air Quality")

    else:

        st.error("🔴 Very Poor Air Quality")


with col2:

    st.markdown(
        f"""
        <div class="info-card">
            <h4>💡 What this means</h4>
            <p>{advisory}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# OVERVIEW CARDS
# ============================================================

st.subheader("📊 Forecast Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Current AQI",
        f"{latest_aqi:.2f}"
    )

with c2:

    st.metric(
        "Category",
        category
    )

with c3:

    st.metric(
        "Forecast Hours",
        forecast_hours
    )

with c4:

    st.metric(
        "Forecast Days",
        forecast_days
    )


st.divider()


# ============================================================
# LATEST FORECAST
# ============================================================

st.subheader("🕒 Latest Forecast")

forecast_time = (
    latest["Timestamp"]
    .strftime(
        "%d %B %Y, %I:%M %p"
    )
)

st.info(
    f"Forecast generated for **{forecast_time}**"
)


st.divider()


# ============================================================
# FORECAST TREND
# ============================================================

st.subheader("📈 AQI Forecast Trend")

st.caption(
    "Predicted AQI values across the available forecast period."
)

chart_data = (
    df
    .set_index("Timestamp")[
        ["Predicted_AQI"]
    ]
)

st.line_chart(
    chart_data,
    height=400
)


st.divider()


# ============================================================
# DAILY SUMMARY
# ============================================================

st.subheader("📅 Daily AQI Summary")

summary_df = df.copy()

summary_df["Date"] = (
    summary_df["Timestamp"]
    .dt.date
)

daily_summary = (
    summary_df
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


# ============================================================
# FORECAST INSIGHTS
# ============================================================

st.subheader("🔎 Forecast Insights")

max_aqi = float(
    df["Predicted_AQI"].max()
)

min_aqi = float(
    df["Predicted_AQI"].min()
)

avg_aqi = float(
    df["Predicted_AQI"].mean()
)

i1, i2, i3 = st.columns(3)

with i1:

    st.metric(
        "Maximum AQI",
        f"{max_aqi:.2f}"
    )

with i2:

    st.metric(
        "Minimum AQI",
        f"{min_aqi:.2f}"
    )

with i3:

    st.metric(
        "Average AQI",
        f"{avg_aqi:.2f}"
    )


st.divider()


# ============================================================
# DOWNLOAD
# ============================================================

st.subheader("⬇️ Download Forecast")

csv_data = (
    df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="⬇️ Download Predictions CSV",
    data=csv_data,
    file_name="karachi_aqi_predictions.csv",
    mime="text/csv",
    key="home_download"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-box">
        <b>🌍 Karachi AQI Forecasting System</b><br>
        Machine Learning • Explainable AI • Automated Forecasting
        <br><br>
        Built for academic, research and portfolio use.
    </div>
    """,
    unsafe_allow_html=True
)
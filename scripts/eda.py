"""
Exploratory Data Analysis (EDA) Pipeline
Pearls AQI Predictor

Input:
    data/processed/cleaned_data.csv

Outputs:
    reports/charts/
    reports/EDA_Report.md
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/cleaned_data.csv"
CHARTS_FOLDER = "reports/charts"
REPORT_FILE = "reports/EDA_Report.md"

os.makedirs(CHARTS_FOLDER, exist_ok=True)
os.makedirs("reports", exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\n============================================")
print("PEARLS AQI PREDICTOR - EDA")
print("============================================")

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")


# ============================================================
# 3. BASIC DATA PREPARATION
# ============================================================

# Convert Timestamp to datetime
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce",
        utc=True
    )

# Sort chronologically
if "Timestamp" in df.columns:
    df = df.sort_values("Timestamp").reset_index(drop=True)


# ============================================================
# 4. DATASET OVERVIEW
# ============================================================

print("\n========== DATASET OVERVIEW ==========")

print("Shape:", df.shape)

print("\nColumns:")
print(list(df.columns))

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Records:")
print(df.head())


# ============================================================
# 5. MISSING VALUES
# ============================================================

print("\n========== MISSING VALUES ==========")

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

print("\nTotal Missing Values:", total_missing)


# ============================================================
# 6. SUMMARY STATISTICS
# ============================================================

print("\n========== SUMMARY STATISTICS ==========")

numeric_df = df.select_dtypes(include="number")

summary_statistics = numeric_df.describe()

print(summary_statistics)


# ============================================================
# 7. AQI DISTRIBUTION
# ============================================================

if "AQI" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df["AQI"],
        bins=5,
        kde=False
    )

    plt.title("AQI Distribution")
    plt.xlabel("OpenWeather AQI Index")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHARTS_FOLDER,
            "aqi_distribution.png"
        ),
        dpi=150
    )

    plt.close()

    print("\nAQI distribution chart saved.")


# ============================================================
# 8. TEMPERATURE DISTRIBUTION
# ============================================================

if "Temperature" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df["Temperature"],
        bins=30,
        kde=True
    )

    plt.title("Temperature Distribution")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHARTS_FOLDER,
            "temperature_distribution.png"
        ),
        dpi=150
    )

    plt.close()

    print("Temperature distribution chart saved.")


# ============================================================
# 9. HUMIDITY DISTRIBUTION
# ============================================================

if "Humidity" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df["Humidity"],
        bins=30,
        kde=True
    )

    plt.title("Humidity Distribution")
    plt.xlabel("Humidity (%)")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHARTS_FOLDER,
            "humidity_distribution.png"
        ),
        dpi=150
    )

    plt.close()

    print("Humidity distribution chart saved.")


# ============================================================
# 10. CORRELATION HEATMAP
# ============================================================

if len(numeric_df.columns) > 1:

    correlation = numeric_df.corr()

    plt.figure(figsize=(12, 9))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )

    plt.title("Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHARTS_FOLDER,
            "correlation_heatmap.png"
        ),
        dpi=150
    )

    plt.close()

    print("Correlation heatmap saved.")


# ============================================================
# 11. TIME SERIES ANALYSIS
# ============================================================

if "Timestamp" in df.columns and "AQI" in df.columns:

    plt.figure(figsize=(14, 6))

    plt.plot(
        df["Timestamp"],
        df["AQI"],
        linewidth=1
    )

    plt.title("AQI Time Series - Karachi")
    plt.xlabel("Timestamp")
    plt.ylabel("OpenWeather AQI Index")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHARTS_FOLDER,
            "time_series_plot.png"
        ),
        dpi=150
    )

    plt.close()

    print("Time-series chart saved.")


# ============================================================
# 12. AQI CHANGE ANALYSIS
# ============================================================

if "AQI" in df.columns:

    df["AQI_Change"] = df["AQI"].diff()

    df["AQI_Change_Rate"] = (
        df["AQI"].pct_change() * 100
    )

    print("\n========== AQI CHANGE ANALYSIS ==========")

    print(
        "Average AQI change:",
        round(df["AQI_Change"].mean(), 3)
    )

    print(
        "Maximum AQI:",
        df["AQI"].max()
    )

    print(
        "Minimum AQI:",
        df["AQI"].min()
    )


# ============================================================
# 13. TIMESTAMP GAP ANALYSIS
# ============================================================

timestamp_gaps = None

if "Timestamp" in df.columns:

    timestamp_diff = df["Timestamp"].diff()

    expected_interval = pd.Timedelta(hours=1)

    gaps = timestamp_diff[
        timestamp_diff > expected_interval
    ]

    timestamp_gaps = len(gaps)

    print("\n========== TIMESTAMP ANALYSIS ==========")

    print(
        "Expected interval:",
        expected_interval
    )

    print(
        "Number of timestamp gaps:",
        timestamp_gaps
    )


# ============================================================
# 14. GENERATE AUTOMATIC INSIGHTS
# ============================================================

print("\n========== KEY INSIGHTS ==========")

insights = []


# AQI insight
if "AQI" in df.columns:

    aqi_counts = df["AQI"].value_counts()

    most_common_aqi = aqi_counts.idxmax()
    most_common_count = aqi_counts.max()

    insights.append(
        f"- The most frequently observed OpenWeather AQI index "
        f"was **{most_common_aqi}**, occurring {most_common_count} times."
    )

    insights.append(
        f"- The observed OpenWeather AQI index ranged from "
        f"**{df['AQI'].min()} to {df['AQI'].max()}**."
    )


# Temperature insight
if "Temperature" in df.columns:

    insights.append(
        f"- Temperature ranged from "
        f"**{df['Temperature'].min():.1f}°C to "
        f"{df['Temperature'].max():.1f}°C**."
    )


# Humidity insight
if "Humidity" in df.columns:

    insights.append(
        f"- Humidity ranged from "
        f"**{df['Humidity'].min():.1f}% to "
        f"{df['Humidity'].max():.1f}%**."
    )


# PM2.5 insight
if "PM2.5" in df.columns:

    insights.append(
        f"- PM2.5 ranged from "
        f"**{df['PM2.5'].min():.2f} to "
        f"{df['PM2.5'].max():.2f}**."
    )


# Correlation insight
if "AQI" in numeric_df.columns:

    aqi_corr = numeric_df.corr()["AQI"].drop("AQI")

    strongest_feature = aqi_corr.abs().idxmax()
    strongest_value = aqi_corr[strongest_feature]

    insights.append(
        f"- The feature with the strongest linear correlation "
        f"with OpenWeather AQI was **{strongest_feature}** "
        f"with a correlation of **{strongest_value:.2f}**."
    )


# Timestamp gap insight
if timestamp_gaps is not None:

    if timestamp_gaps > 0:

        insights.append(
            f"- The dataset contains **{timestamp_gaps} timestamp gap(s)** "
            f"where the expected hourly sequence is interrupted."
        )

    else:

        insights.append(
            "- No major timestamp gaps were detected in the dataset."
        )


for insight in insights:
    print(insight)


# ============================================================
# 15. SAVE EDA REPORT
# ============================================================

print("\nGenerating EDA Report...")


date_start = (
    df["Timestamp"].min()
    if "Timestamp" in df.columns
    else "N/A"
)

date_end = (
    df["Timestamp"].max()
    if "Timestamp" in df.columns
    else "N/A"
)


# AQI distribution text
aqi_distribution_text = ""

if "AQI" in df.columns:

    counts = df["AQI"].value_counts().sort_index()

    for value, count in counts.items():

        percentage = (count / len(df)) * 100

        aqi_distribution_text += (
            f"| {value} | {count} | {percentage:.2f}% |\n"
        )


# Summary table
summary_table = ""

for column in numeric_df.columns:

    summary_table += (
        f"| {column} | "
        f"{numeric_df[column].mean():.2f} | "
        f"{numeric_df[column].min():.2f} | "
        f"{numeric_df[column].max():.2f} |\n"
    )


report_content = f"""# Pearls AQI Predictor — Exploratory Data Analysis Report

## 1. Dataset Overview

The dataset used for this EDA is the cleaned historical dataset generated
during the historical data and preprocessing phases of the **Pearls AQI Predictor** project.

### Dataset Information

- **City:** Karachi
- **Number of records:** {len(df)}
- **Number of columns:** {len(df.columns)}
- **Start timestamp:** {date_start}
- **End timestamp:** {date_end}
- **Data frequency:** Approximately hourly
- **Target variable:** AQI
- **Data source:** Weather and air-pollution historical data

### Main Features

The dataset contains:

- Timestamp
- City
- Temperature
- Humidity
- Pressure
- Wind Speed
- AQI
- PM2.5
- PM10
- CO
- NO2
- SO2
- O3
- NH3

---

## 2. Dataset Quality

### Missing Values

Total missing values:

**{total_missing}**

The preprocessing pipeline handled missing values before this EDA stage.

### Duplicate Records

Duplicate records were removed during preprocessing.

### Timestamp

The timestamp column was converted into datetime format and the dataset
was sorted chronologically.

Detected timestamp gaps:

**{timestamp_gaps if timestamp_gaps is not None else "N/A"}**

---

## 3. Summary Statistics

| Feature | Mean | Minimum | Maximum |
|---|---:|---:|---:|
{summary_table}

The summary statistics provide an overview of the central tendency and
range of the numerical variables.

---

## 4. AQI Distribution

![AQI Distribution](charts/aqi_distribution.png)

The AQI distribution shows how frequently each OpenWeather AQI index
was observed in the historical Karachi dataset.

### AQI Frequency

| AQI Index | Records | Percentage |
|---:|---:|---:|
{aqi_distribution_text}

### Observation

The dataset contains OpenWeather's **1–5 AQI index** rather than a
0–500 standardized AQI value. Therefore, these values should not be
interpreted directly as conventional AQI scores.

---

## 5. Temperature Distribution

![Temperature Distribution](charts/temperature_distribution.png)

The temperature distribution shows the range and frequency of recorded
temperatures in Karachi during the historical period.

Temperature range:

**{df["Temperature"].min():.1f}°C – {df["Temperature"].max():.1f}°C**

---

## 6. Humidity Distribution

![Humidity Distribution](charts/humidity_distribution.png)

The humidity distribution shows the spread of humidity observations
throughout the historical period.

Humidity range:

**{df["Humidity"].min():.1f}% – {df["Humidity"].max():.1f}%**

---

## 7. Correlation Analysis

![Correlation Heatmap](charts/correlation_heatmap.png)

Correlation analysis was performed on the numerical variables.

The correlation matrix helps identify relationships between pollutants,
weather conditions and the OpenWeather AQI index.

"""

if "AQI" in numeric_df.columns:

    aqi_corr = (
        numeric_df.corr()["AQI"]
        .drop("AQI")
        .sort_values(
            key=lambda x: x.abs(),
            ascending=False
        )
    )

    report_content += "### Correlation with AQI\n\n"
    report_content += "| Feature | Correlation with AQI |\n"
    report_content += "|---|---:|\n"

    for feature, value in aqi_corr.items():

        report_content += (
            f"| {feature} | {value:.2f} |\n"
        )


report_content += f"""

---

## 8. Time-Series Analysis

![AQI Time Series](charts/time_series_plot.png)

The time-series plot shows how the OpenWeather AQI index changes over
time in the historical Karachi dataset.

Time-series analysis is important for the AQI forecasting system because
the final project aims to predict future air-quality conditions.

The chronological ordering of the observations also helps prepare the
dataset for future time-based feature engineering and forecasting models.

---

## 9. AQI Change Analysis

The AQI change rate was calculated to support future feature engineering.

### Formula

AQI Change:

`Current AQI - Previous AQI`

AQI Change Rate:

`((Current AQI - Previous AQI) / Previous AQI) × 100`

The average AQI change observed in the dataset was:

**{df["AQI_Change"].mean():.3f}**

These features can later be used as inputs during the feature-engineering
phase, provided they are calculated without using future information.

---

## 10. Key Insights

"""

for insight in insights:

    report_content += insight + "\n"


report_content += """

---

## 11. EDA Conclusion

The EDA confirms that the historical dataset contains weather and
pollutant observations suitable for further feature engineering and
machine-learning experiments.

Important observations include:

1. AQI values show variation throughout the historical period.
2. Pollutant concentrations vary considerably over time.
3. Weather variables such as temperature, humidity, pressure and wind
   speed provide additional contextual information.
4. Correlation analysis helps identify potentially useful predictive
   features.
5. Time-series analysis confirms that chronological ordering is important
   for the forecasting problem.
6. Timestamp gaps should be considered during future feature engineering
   and model training.

The next phase will transform these raw variables into model-ready
time-based and derived features for AQI forecasting.
"""


with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(report_content)


# ============================================================
# 16. FINAL MESSAGE
# ============================================================

print("\n============================================")
print("EDA COMPLETED SUCCESSFULLY!")
print("============================================")
print("Charts saved in:", CHARTS_FOLDER)
print("EDA Report saved at:", REPORT_FILE)
print("============================================")
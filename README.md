# 🌍 AQI Forecasting System

An end-to-end Machine Learning system for forecasting Air Quality Index (AQI) using historical air-quality data, weather information, feature engineering, machine learning, Explainable AI, automated pipelines, and an interactive Streamlit dashboard.

The project is designed as an academic, research, and portfolio-level Machine Learning application.

---

## 🚀 Live Demo

### Streamlit Dashboard

https://aqi-predictor-kdhjvpanp5jz3xvwnlqvde.streamlit.app/

The live dashboard provides:

- AQI overview
- 72-hour AQI forecast
- Daily AQI summary
- Prediction history
- Model information
- Health advisory
- Forecast visualization
- CSV prediction download

---


## 🏗️ System Architecture

                   ┌─────────────────────┐
                │ Weather / AQI Data  │
                │       Sources       │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   Data Collection   │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Historical Dataset  │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Data Preprocessing   │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Feature Engineering │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │    Feature Store    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   Model Training    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │  Model Evaluation   │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   Model Registry    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   AQI Prediction    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   72-Hour Forecast  │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   SHAP Explainable  │
                │         AI          │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Streamlit Dashboard │
                └─────────────────────┘

📁 Project Structure

AQI-Predictor/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── feature_pipeline.yml
│       └── training_pipeline.yml
│
├── api/
│   ├── app.py
│   └── app_backup.py
│
├── app/
│   ├── streamlit_app.py
│   ├── theme.py
│   ├── app_backup.py
│   └── assets/
│
├── data/
│   ├── historical/
│   └── processed/
│
├── feature_store/
│   ├── features_v1.csv
│   └── metadata.json
│
├── models/
│   └── trained model files
│
├── model_registry/
│   └── v1/
│       ├── registry.json
│       ├── metrics.json
│       └── metadata.json
│
├── predictions/
│   └── predictions.csv
│
├── reports/
│   ├── evaluation_report.md
│   └── evaluation_charts/
│
├── scripts/
│   ├── backfill_aqi.py
│   ├── backfill_weather.py
│   ├── eda.py
│   ├── evaluate_model.py
│   ├── explain_model.py
│   ├── feature_engineering.py
│   ├── fetch_weather.py
│   ├── forecast_3days.py
│   ├── merge_aqi.py
│   ├── merge_historical.py
│   ├── merge_karachi_data.py
│   ├── predict.py
│   ├── preprocess_data.py
│   ├── register_model.py
│   ├── store_features.py
│   ├── train_model.py
│   └── validation scripts
│
├── tests/
│   └── test_preprocessing.py
│
├── requirements.txt
└── README.md

🎯 Project Goal

The goal of this project is to build a complete Machine Learning solution for AQI forecasting, from data processing and model development to automated prediction, Explainable AI, API integration, and an interactive web dashboard.

👩‍💻 Author

Madhubala

Machine Learning & AI Project
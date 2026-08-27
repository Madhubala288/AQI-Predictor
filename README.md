# 🌍 AQI Forecasting System

An end-to-end Machine Learning system for forecasting
Air Quality Index (AQI) using historical air-quality data,
weather information, feature engineering, machine learning,
Explainable AI, and a Streamlit dashboard.

## 🚀 Live Demo

Streamlit Dashboard:

https://aqi-predictor-kdhjvpanp5jz3xvwnlqvde.streamlit.app/

## 📌 Project Overview

The AQI Forecasting System is designed to predict future
air quality conditions using historical pollution data,
weather features, and engineered time-series features.

The system follows a complete Machine Learning pipeline:

Data Collection → Data Preprocessing → Feature Engineering
→ Feature Store → Model Training → Model Evaluation
→ Model Registry → AQI Forecasting → Explainable AI
→ Streamlit Dashboard

## ✨ Key Features

- Historical AQI data processing
- Weather data integration
- Automated data preprocessing
- Feature engineering
- Feature Store
- Machine Learning model training
- Random Forest AQI prediction
- Model evaluation
- Model Registry
- 72-hour AQI forecasting
- SHAP-based Explainable AI
- AQI health advisory
- Interactive Streamlit dashboard
- Prediction visualization
- Prediction CSV download
- Automated testing
- GitHub Actions CI/CD

## 🛠️ Technology Stack

### Programming Language
- Python

### Data Processing
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- Random Forest Regressor
- Ridge Regression

### Explainable AI
- SHAP

### Visualization
- Matplotlib
- Streamlit

### APIs
- OpenWeather API

### Version Control
- Git
- GitHub

### Automation
- GitHub Actions

## 🏗️ System Architecture

```text
Weather / Air Pollution APIs
            │
            ▼
     Data Collection
            │
            ▼
     Historical Data
            │
            ▼
      Preprocessing
            │
            ▼
    Feature Engineering
            │
            ▼
      Feature Store
            │
            ▼
     Model Training
            │
            ▼
    Model Evaluation
            │
            ▼
      Model Registry
            │
            ▼
    72-Hour Forecast
            │
            ▼
   Streamlit Dashboard
            │
            ▼
    Explainable AI
         (SHAP)
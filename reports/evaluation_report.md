# Phase 9 — Model Evaluation Report

## 1. Model Information

- Model: `RandomForestRegressor`
- Dataset: `features_v1.csv`
- Total Samples: 694
- Training Samples: 555
- Testing Samples: 139

## 2. Evaluation Metrics

| Metric | Value |
|---|---:|
| MAE | 0.0422 |
| RMSE | 0.1069 |
| R² | 0.9932 |

## 3. Error Analysis

- Mean Absolute Error: **0.0422**
- Maximum Error: **0.7950**
- 95th Percentile Error: **0.2200**
- High-error observations: **8**

## 4. Test Period

- Start: `2024-01-25 06:00:00+00:00`
- End: `2024-01-31 00:00:00+00:00`

## 5. Feature Importance

- **PM2.5**: 0.9805
- **PM10**: 0.0088
- **Temperature**: 0.0023
- **Wind_Speed**: 0.0020
- **Pressure**: 0.0018


## 6. Generated Charts

- `evaluation_charts/actual_vs_predicted.png`
- `evaluation_charts/residual_plot.png`
- `evaluation_charts/feature_importance.png`

## 7. Conclusion

The trained model was evaluated on the final 20% of the chronological dataset.

The evaluation uses MAE, RMSE and R² to measure prediction performance.

Because this project uses time-series data, the evaluation was performed without random shuffling.

The model's performance should be interpreted in the context of the OpenWeather AQI index used in the dataset.

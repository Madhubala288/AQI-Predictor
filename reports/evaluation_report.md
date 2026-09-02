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

The model achieved a very low average prediction error. The MAE of 0.0422 indicates that the predicted AQI values differ from the actual values by approximately 0.04 AQI units on average.

The RMSE of 0.1069 indicates that larger prediction errors were also relatively low. The R² score of 0.9932 means that the model explains approximately 99.32% of the variance in the target AQI values.

## 4. Test Period

- Start: `2024-01-25 06:00:00+00:00`
- End: `2024-01-31 00:00:00+00:00`

## 5. Feature Importance

- **PM2.5**: 0.9805
- **PM10**: 0.0088
- **Temperature**: 0.0023
- **Wind_Speed**: 0.0020
- **Pressure**: 0.0018

PM2.5 was the most influential feature in the Random Forest model, contributing approximately 98.05% of the model's feature importance.

## 6. Generated Charts

- `evaluation_charts/actual_vs_predicted.png`
- `evaluation_charts/residual_plot.png`
- `evaluation_charts/feature_importance.png`

## 7. Conclusion

The trained Random Forest model was evaluated on the final 20% of the chronological dataset, using 555 samples for training and 139 samples for testing.

The model achieved an MAE of 0.0422, an RMSE of 0.1069, and an R² score of 0.9932. These results indicate strong predictive performance on the test dataset, with approximately 99.32% of the variance in AQI values explained by the model.

Because this project uses time-series data, the evaluation was performed without random shuffling to preserve the chronological order of observations.

The model's performance should be interpreted in the context of the OpenWeather AQI index used in the dataset. The reported R² score represents explained variance and should not be interpreted as classification accuracy.
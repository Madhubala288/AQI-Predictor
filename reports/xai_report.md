# Explainable AI Report

## Model Information

- **Model:** RandomForestRegressor
- **Model Version:** v1
- **Explanation Method:** SHAP TreeExplainer
- **Model Type:** Tree-based Random Forest
- **Number of Features:** 18
- **Explanation Dataset Size:** 694 rows

## Explainability Methods

### SHAP Summary Plot

The SHAP summary plot shows the global importance and impact of features across the dataset.

### SHAP Waterfall Plot

The SHAP waterfall plot explains how individual features contributed to one specific AQI prediction.

### Random Forest Feature Importance

The feature importance chart shows the relative importance of each feature used by the Random Forest model.

## Top Features

- **PM2.5**: 0.980521
- **PM10**: 0.008837
- **Temperature**: 0.002269
- **Wind_Speed**: 0.001973
- **Pressure**: 0.001763
- **AQI_Lag_1**: 0.000963
- **Humidity**: 0.000927
- **NO2**: 0.000703
- **Hour**: 0.000628
- **O3**: 0.000450

## Generated Files

- `explainability/shap_summary.png`
- `explainability/shap_waterfall.png`
- `explainability/feature_importance.png`

## Conclusion

The Explainable AI analysis provides both global and local explanations of the AQI forecasting model. SHAP identifies how individual features influence predictions, while Random Forest feature importance provides an overall ranking of feature influence.

The explanations are generated directly from the registered production model (v1), ensuring that the XAI results correspond to the model used by the forecasting system.
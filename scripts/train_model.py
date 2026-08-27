"""
Phase 8B - Corrected Machine Learning Pipeline

Purpose:
- Prevent target leakage
- Train multiple regression models
- Tune Random Forest and Ridge
- Compare models
- Save the best model
- Verify saved model
"""

import json
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "feature_store/features_v1.csv"

MODEL_DIR = "models"

BEST_MODEL_FILE = os.path.join(
    MODEL_DIR,
    "best_model.pkl"
)

METADATA_FILE = os.path.join(
    MODEL_DIR,
    "model_metadata.json"
)

RANDOM_STATE = 42


# ============================================================
# FEATURE SELECTION
# ============================================================

# Features that are safe for forecasting
FEATURE_COLUMNS = [
    "Temperature",
    "Humidity",
    "Pressure",
    "Wind_Speed",
    "PM2.5",
    "PM10",
    "CO",
    "NO2",
    "SO2",
    "O3",
    "NH3",
    "Hour",
    "Day",
    "Month",
    "Weekday",
    "AQI_Lag_1",
    "AQI_Lag_2",
    "AQI_Lag_3"
]

TARGET_COLUMN = "AQI"


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading feature dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Dataset Shape: {df.shape}")


# ============================================================
# SORT DATA CHRONOLOGICALLY
# ============================================================

if "Timestamp" in df.columns:

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.sort_values(
        "Timestamp"
    ).reset_index(drop=True)

    print("Dataset sorted chronologically.")


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

print("\n========== COLUMN VALIDATION ==========")

required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("All required columns are available.")


# ============================================================
# CHECK DATA LEAKAGE
# ============================================================

print("\n========== DATA LEAKAGE CHECK ==========")

forbidden_features = [
    "AQI",
    "AQI_Change",
    "AQI_Moving_Average_3H"
]

used_forbidden = [
    col
    for col in FEATURE_COLUMNS
    if col in forbidden_features
]

if used_forbidden:

    raise ValueError(
        f"Target leakage detected: {used_forbidden}"
    )

print("No current-AQI leakage detected.")
print("AQI_Change and AQI_Moving_Average_3H are excluded.")


# ============================================================
# SELECT X AND y
# ============================================================

X = df[FEATURE_COLUMNS].copy()

y = df[TARGET_COLUMN].copy()

print("\n========== FEATURES AND TARGET ==========")

print(f"Features Shape: {X.shape}")
print(f"Target Shape  : {y.shape}")

print("\nFeatures used:")

for feature in FEATURE_COLUMNS:
    print(f"- {feature}")

print(f"\nTarget: {TARGET_COLUMN}")


# ============================================================
# REMOVE MISSING VALUES
# ============================================================

print("\n========== MISSING VALUES ==========")

training_data = pd.concat(
    [X, y],
    axis=1
)

print(
    f"Rows before removing missing values: "
    f"{len(training_data)}"
)

training_data = training_data.dropna()

print(
    f"Rows after removing missing values : "
    f"{len(training_data)}"
)

X = training_data[FEATURE_COLUMNS]

y = training_data[TARGET_COLUMN]


# ============================================================
# CHRONOLOGICAL TRAIN / TEST SPLIT
# ============================================================

print("\n========== CHRONOLOGICAL TRAIN TEST SPLIT ==========")

split_index = int(len(X) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

print("\nImportant:")
print("The first 80% is used for training.")
print("The final 20% is used for testing.")
print("No random shuffling is used because this is time-series data.")


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    return mae, rmse, r2


# ============================================================
# MODEL RESULTS
# ============================================================

results = []


# ============================================================
# 1. LINEAR REGRESSION
# ============================================================

print("\n========== LINEAR REGRESSION ==========")

linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train
)

linear_mae, linear_rmse, linear_r2 = evaluate_model(
    linear_model,
    X_test,
    y_test
)

print(f"MAE : {linear_mae:.4f}")
print(f"RMSE: {linear_rmse:.4f}")
print(f"R2  : {linear_r2:.4f}")

results.append({
    "Model": "Linear Regression",
    "MAE": linear_mae,
    "RMSE": linear_rmse,
    "R2": linear_r2,
    "model_object": linear_model
})


# ============================================================
# 2. RANDOM FOREST
# ============================================================

print("\n========== RANDOM FOREST ==========")

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=RANDOM_STATE,
    n_jobs=-1
)

rf_model.fit(
    X_train,
    y_train
)

rf_mae, rf_rmse, rf_r2 = evaluate_model(
    rf_model,
    X_test,
    y_test
)

print(f"MAE : {rf_mae:.4f}")
print(f"RMSE: {rf_rmse:.4f}")
print(f"R2  : {rf_r2:.4f}")

results.append({
    "Model": "Random Forest",
    "MAE": rf_mae,
    "RMSE": rf_rmse,
    "R2": rf_r2,
    "model_object": rf_model
})


# ============================================================
# 3. RIDGE REGRESSION
# ============================================================

print("\n========== RIDGE REGRESSION ==========")

ridge_pipeline = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            Ridge()
        )
    ]
)

ridge_pipeline.fit(
    X_train,
    y_train
)

ridge_mae, ridge_rmse, ridge_r2 = evaluate_model(
    ridge_pipeline,
    X_test,
    y_test
)

print(f"MAE : {ridge_mae:.4f}")
print(f"RMSE: {ridge_rmse:.4f}")
print(f"R2  : {ridge_r2:.4f}")

results.append({
    "Model": "Ridge Regression",
    "MAE": ridge_mae,
    "RMSE": ridge_rmse,
    "R2": ridge_r2,
    "model_object": ridge_pipeline
})


# ============================================================
# 4. RANDOM FOREST HYPERPARAMETER TUNING
# ============================================================

print("\n========== RANDOM FOREST TUNING ==========")

rf_parameter_grid = {

    "n_estimators": [
        100,
        200
    ],

    "max_depth": [
        None,
        10,
        20
    ],

    "min_samples_split": [
        2,
        5
    ],

    "min_samples_leaf": [
        1,
        2
    ]
}


rf_grid = GridSearchCV(
    estimator=RandomForestRegressor(
        random_state=RANDOM_STATE,
        n_jobs=-1
    ),

    param_grid=rf_parameter_grid,

    scoring="neg_mean_absolute_error",

    cv=3,

    n_jobs=-1
)

rf_grid.fit(
    X_train,
    y_train
)

tuned_rf = rf_grid.best_estimator_

tuned_rf_mae, tuned_rf_rmse, tuned_rf_r2 = evaluate_model(
    tuned_rf,
    X_test,
    y_test
)

print("Best Random Forest Parameters:")
print(rf_grid.best_params_)

print(f"MAE : {tuned_rf_mae:.4f}")
print(f"RMSE: {tuned_rf_rmse:.4f}")
print(f"R2  : {tuned_rf_r2:.4f}")

results.append({
    "Model": "Tuned Random Forest",
    "MAE": tuned_rf_mae,
    "RMSE": tuned_rf_rmse,
    "R2": tuned_rf_r2,
    "model_object": tuned_rf
})


# ============================================================
# 5. RIDGE HYPERPARAMETER TUNING
# ============================================================

print("\n========== RIDGE TUNING ==========")

ridge_parameter_grid = {

    "model__alpha": [
        0.01,
        0.1,
        1.0,
        10.0,
        100.0
    ]
}


ridge_grid = GridSearchCV(
    estimator=Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                Ridge()
            )
        ]
    ),

    param_grid=ridge_parameter_grid,

    scoring="neg_mean_absolute_error",

    cv=3,

    n_jobs=-1
)

ridge_grid.fit(
    X_train,
    y_train
)

tuned_ridge = ridge_grid.best_estimator_

tuned_ridge_mae, tuned_ridge_rmse, tuned_ridge_r2 = evaluate_model(
    tuned_ridge,
    X_test,
    y_test
)

print("Best Ridge Parameters:")
print(ridge_grid.best_params_)

print(f"MAE : {tuned_ridge_mae:.4f}")
print(f"RMSE: {tuned_ridge_rmse:.4f}")
print(f"R2  : {tuned_ridge_r2:.4f}")

results.append({
    "Model": "Tuned Ridge Regression",
    "MAE": tuned_ridge_mae,
    "RMSE": tuned_ridge_rmse,
    "R2": tuned_ridge_r2,
    "model_object": tuned_ridge
})


# ============================================================
# MODEL COMPARISON
# ============================================================

print("\n==============================================")
print("              MODEL COMPARISON")
print("==============================================")

comparison_data = []

for result in results:

    comparison_data.append({
        "Model": result["Model"],
        "MAE": result["MAE"],
        "RMSE": result["RMSE"],
        "R2": result["R2"]
    })

comparison_df = pd.DataFrame(
    comparison_data
)

print(
    comparison_df.to_string(
        index=False
    )
)


# ============================================================
# SELECT BEST MODEL
# ============================================================

# Primary metric: lowest MAE
# Secondary metric: lowest RMSE
# Tertiary metric: highest R2

best_result = sorted(
    results,
    key=lambda x: (
        x["MAE"],
        x["RMSE"],
        -x["R2"]
    )
)[0]

best_model = best_result["model_object"]

best_model_name = best_result["Model"]

best_mae = best_result["MAE"]
best_rmse = best_result["RMSE"]
best_r2 = best_result["R2"]


# ============================================================
# BEST MODEL INFORMATION
# ============================================================

print("\n==============================================")
print("                 BEST MODEL")
print("==============================================")

print(
    f"Selected Model: {best_model_name}"
)

print(
    f"MAE : {best_mae:.4f}"
)

print(
    f"RMSE: {best_rmse:.4f}"
)

print(
    f"R2  : {best_r2:.4f}"
)


# ============================================================
# SAVE BEST MODEL
# ============================================================

joblib.dump(
    best_model,
    BEST_MODEL_FILE
)

print(
    f"\nBest model saved to:\n"
    f"{BEST_MODEL_FILE}"
)


# ============================================================
# SAVE MODEL METADATA
# ============================================================

metadata = {

    "phase": "Phase 8B",

    "model_name": best_model_name,

    "dataset": INPUT_FILE,

    "dataset_rows": int(len(df)),

    "training_samples": int(len(X_train)),

    "testing_samples": int(len(X_test)),

    "target": TARGET_COLUMN,

    "features": FEATURE_COLUMNS,

    "excluded_features": [
        "AQI_Change",
        "AQI_Moving_Average_3H"
    ],

    "data_leakage_check": "passed",

    "metrics": {

        "MAE": float(best_mae),

        "RMSE": float(best_rmse),

        "R2": float(best_r2)
    },

    "train_test_split": "80/20 chronological",

    "random_state": RANDOM_STATE
}


with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print(
    f"Metadata saved to:\n"
    f"{METADATA_FILE}"
)


# ============================================================
# MODEL VERIFICATION
# ============================================================

print("\n========== MODEL VERIFICATION ==========")

loaded_model = joblib.load(
    BEST_MODEL_FILE
)

print("Model loaded successfully.")


sample_X = X_test.head(5)

sample_predictions = loaded_model.predict(
    sample_X
)

print("\nSample predictions:")

for i, prediction in enumerate(
    sample_predictions,
    start=1
):

    print(
        f"Sample {i}: {prediction:.4f}"
    )


# ============================================================
# FINAL CHECK
# ============================================================

print("\n=======================================================")
print("PHASE 8B COMPLETED SUCCESSFULLY!")
print("=======================================================")

print("\nGenerated files:")

print(
    f"1. {BEST_MODEL_FILE}"
)

print(
    f"2. {METADATA_FILE}"
)

print("\nMachine Learning pipeline is ready for Phase 9.")
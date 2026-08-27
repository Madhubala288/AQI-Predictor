"""
Phase 10 - Model Registry

Registers the best-performing model with:
- Model version
- Evaluation metrics
- Metadata
- Registry information
- Model verification
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import joblib
import sklearn


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"
REGISTRY_DIR = BASE_DIR / "model_registry"
VERSION = "v1"
VERSION_DIR = REGISTRY_DIR / VERSION

BEST_MODEL = MODEL_DIR / "best_model.pkl"
MODEL_METADATA = MODEL_DIR / "model_metadata.json"

METRICS_FILE = VERSION_DIR / "metrics.json"
METADATA_FILE = VERSION_DIR / "metadata.json"
REGISTRY_FILE = VERSION_DIR / "registry.json"
REGISTERED_MODEL = VERSION_DIR / "best_model.pkl"


# ============================================================
# 2. CREATE REGISTRY FOLDER
# ============================================================

VERSION_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. CHECK BEST MODEL
# ============================================================

print("========== MODEL REGISTRATION ==========")

if not BEST_MODEL.exists():
    print("ERROR: best_model.pkl not found.")
    sys.exit(1)

print("Best model found.")


# ============================================================
# 4. COPY BEST MODEL
# ============================================================

shutil.copy2(BEST_MODEL, REGISTERED_MODEL)

print(f"Model copied to:")
print(REGISTERED_MODEL)


# ============================================================
# 5. LOAD EXISTING MODEL METADATA
# ============================================================

if MODEL_METADATA.exists():

    with open(MODEL_METADATA, "r") as file:
        original_metadata = json.load(file)

else:
    original_metadata = {}


# ============================================================
# 6. SAVE EVALUATION METRICS
# ============================================================

# Metrics obtained from Phase 9
metrics = {
    "MAE": 0.0422,
    "RMSE": 0.1069,
    "R2": 0.9932
}

with open(METRICS_FILE, "w") as file:
    json.dump(metrics, file, indent=4)

print("Metrics saved successfully.")


# ============================================================
# 7. CREATE MODEL METADATA
# ============================================================

metadata = {
    "model_version": VERSION,
    "model_name": "Tuned Random Forest",
    "model_type": "RandomForestRegressor",
    "training_date": datetime.now().strftime("%Y-%m-%d"),
    "dataset_version": "features_v1.csv",
    "framework": "scikit-learn",
    "sklearn_version": sklearn.__version__,
    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    "target": "AQI",
    "scaler_required": False,
    "source_metadata": original_metadata
}

with open(METADATA_FILE, "w") as file:
    json.dump(metadata, file, indent=4, default=str)

print("Metadata saved successfully.")


# ============================================================
# 8. CREATE REGISTRY FILE
# ============================================================

registry = {
    "model_version": VERSION,
    "status": "Production",
    "registered_on": datetime.now().strftime("%Y-%m-%d"),
    "current_best_model": "Tuned Random Forest",
    "model_type": "RandomForestRegressor",
    "model_path": str(REGISTERED_MODEL.relative_to(BASE_DIR)),
    "metrics_path": str(METRICS_FILE.relative_to(BASE_DIR)),
    "metadata_path": str(METADATA_FILE.relative_to(BASE_DIR))
}

with open(REGISTRY_FILE, "w") as file:
    json.dump(registry, file, indent=4)

print("Registry information saved successfully.")


# ============================================================
# 9. VERIFY MODEL
# ============================================================

print("\n========== REGISTRY VERIFICATION ==========")

try:

    loaded_model = joblib.load(REGISTERED_MODEL)

    print("Registered model loaded successfully.")
    print(f"Model type: {type(loaded_model).__name__}")

except Exception as error:

    print(f"Model verification failed: {error}")
    sys.exit(1)


# ============================================================
# 10. VERIFY ALL FILES
# ============================================================

required_files = [
    REGISTERED_MODEL,
    METRICS_FILE,
    METADATA_FILE,
    REGISTRY_FILE
]

all_files_exist = True

for file_path in required_files:

    if file_path.exists():
        print(f"✓ {file_path.name}")
    else:
        print(f"✗ {file_path.name}")
        all_files_exist = False


# ============================================================
# 11. FINAL RESULT
# ============================================================

if not all_files_exist:

    print("\nModel Registry verification FAILED.")
    sys.exit(1)

print("\n=======================================================")
print("PHASE 10 COMPLETED SUCCESSFULLY!")
print("=======================================================")

print("\nRegistered Model:")
print(f"Version : {VERSION}")
print("Model   : Tuned Random Forest")
print("Status  : Production")

print("\nRegistry location:")
print(VERSION_DIR)
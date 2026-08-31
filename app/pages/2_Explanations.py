import streamlit as st
import json
from pathlib import Path


st.set_page_config(
    page_title="AQI Explanations",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

XAI_DIR = (
    BASE_DIR
    / "reports"
    / "explainability"
)

REGISTRY_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "registry.json"
)


# ============================================================
# LOAD REGISTRY
# ============================================================

def load_json(path):

    if not path.exists():
        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


registry = load_json(
    REGISTRY_FILE
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🧠 Explainable AI"
)

st.caption(
    "Understand which features influence the AQI prediction."
)


st.info(
    "SHAP explanations are generated from the registered "
    "production model."
)


# ============================================================
# MODEL INFORMATION
# ============================================================

st.subheader(
    "🤖 Model Information"
)

model_name = registry.get(
    "current_best_model",
    "Random Forest"
)

model_type = registry.get(
    "model_type",
    "Random Forest Regressor"
)

model_version = registry.get(
    "model_version",
    "v1"
)

model_status = registry.get(
    "status",
    "Production"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Model",
        model_name
    )

with c2:
    st.metric(
        "Algorithm",
        model_type
    )

with c3:
    st.metric(
        "Version",
        model_version
    )

with c4:
    st.metric(
        "Status",
        model_status
    )


st.divider()


# ============================================================
# SHAP SUMMARY
# ============================================================

summary_file = (
    XAI_DIR
    / "shap_summary.png"
)

st.subheader(
    "📊 SHAP Feature Importance"
)

st.caption(
    "Global explanation showing how features influence "
    "AQI predictions."
)

if summary_file.exists():

    st.image(
        str(summary_file),
        width="stretch"
    )

else:

    st.warning(
        "SHAP summary image not found."
    )


st.divider()


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance_file = (
    XAI_DIR
    / "feature_importance.png"
)

st.subheader(
    "🎯 Random Forest Feature Importance"
)

if importance_file.exists():

    st.image(
        str(importance_file),
        width="stretch"
    )

else:

    st.warning(
        "Feature importance image not found."
    )


st.divider()


# ============================================================
# WATERFALL
# ============================================================

waterfall_file = (
    XAI_DIR
    / "shap_waterfall.png"
)

st.subheader(
    "💧 Individual Prediction Explanation"
)

st.caption(
    "SHAP waterfall plot explaining one individual "
    "AQI prediction."
)

if waterfall_file.exists():

    st.image(
        str(waterfall_file),
        width="stretch"
    )

else:

    st.warning(
        "SHAP waterfall image not found."
    )


st.divider()


# ============================================================
# EXPLANATION
# ============================================================

st.subheader(
    "ℹ️ How to interpret SHAP"
)

st.write(
    """
    SHAP explains the contribution of individual features
    to a machine-learning prediction.

    A feature with a larger absolute SHAP value has a
    stronger influence on the prediction.

    The summary plot provides a global view of feature
    influence, while the waterfall plot explains one
    individual prediction.
    """
)
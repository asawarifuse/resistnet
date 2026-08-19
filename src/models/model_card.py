"""
ResistNet - Model Card
Scientific documentation of models, data, and limitations.
"""

MODEL_CARD = {
    "name": "ResistNet AMR Early Warning & Response System",
    "version": "2.0",
    "intended_use": "District-level AMR risk forecasting and public-health decision support prototype",
    "not_intended_for": [
        "Individual patient diagnosis",
        "Autonomous prescribing",
        "Clinical decisions without human oversight"
    ],
    "data": {
        "amr_resistance": {
            "source": "Synthetic prototype modeled on publicly reported AMR surveillance characteristics",
            "real_or_synthetic": "Synthetic",
            "records": 54720,
            "period": "2021-2023",
            "pathogens": 5,
            "antibiotics": 14
        },
        "pharma_sales": {
            "source": "Synthetic prototype modeled on antibiotic consumption patterns",
            "real_or_synthetic": "Synthetic",
            "records": 229824,
            "period": "2021-2023",
            "channels": 4
        }
    },
    "models": ["Prophet", "Random Forest", "XGBoost", "LSTM", "Ensemble"],
    "evaluation": {
        "backtest_period": "2023",
        "mae": "0.71%",
        "rmse": "1.04%",
        "r2": 0.998,
        "leakage_free": True,
        "lead_time_median_quarters": 6,
        "detection_rate": "100%",
        "ablation_improvement": "21.1%"
    },
    "limitations": [
        "Synthetic prototype data - not validated clinical surveillance data",
        "No prospective clinical validation",
        "Geographic bias (114 districts, not all 766)",
        "Reporting bias in underlying patterns",
        "Data availability limitations",
        "Potential model drift over time",
        "Requires real-world surveillance data for production",
        "Not for autonomous clinical decisions"
    ],
    "disclaimer": "Prototype for demonstration. Not for clinical use without validation."
}

def get_model_card():
    return MODEL_CARD

if __name__ == "__main__":
    import json
    print(json.dumps(MODEL_CARD, indent=2))
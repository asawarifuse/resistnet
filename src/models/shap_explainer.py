"""
ResistNet - SHAP Explainability Module
Explains resistance predictions using SHAP values.
Identifies which factors drive high-risk alerts.
"""

import pandas as pd
import numpy as np
import os
import shap
import pickle
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

os.makedirs(REPORTS_DIR, exist_ok=True)

def train_explainable_model():
    """Train a Random Forest on engineered features for SHAP analysis"""
    
    print("📥 Loading feature matrix...")
    X = pd.read_csv(f"{PROCESSED_DATA_DIR}/features_X.csv")
    y = pd.read_csv(f"{PROCESSED_DATA_DIR}/features_y_reg.csv").values.ravel()
    metadata = pd.read_csv(f"{PROCESSED_DATA_DIR}/features_metadata.csv")
    
    print(f"   Features: {X.shape}")
    print(f"   Target: {len(y):,} records")
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Sample for faster training (50K is a lot for SHAP)
    sample_size = min(10000, len(X))
    rng = np.random.RandomState(42)
    indices = rng.choice(len(X), sample_size, replace=False)
    X_sample = X.iloc[indices]
    y_sample = y[indices]
    
    print(f"\n🎯 Training Random Forest on {sample_size:,} samples...")
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_sample, y_sample)
    
    # Evaluate
    train_score = model.score(X_sample, y_sample)
    print(f"   Training R²: {train_score:.3f}")
    
    return model, X_sample, y_sample, X.columns.tolist()

def generate_shap_explanations(model, X_sample, feature_names):
    """Generate SHAP explanations"""
    
    print("\n🔍 Computing SHAP values...")
    
    # Use TreeExplainer (fast for Random Forest)
    explainer = shap.TreeExplainer(model)
    
    # Compute SHAP on a smaller subset for speed
    X_shap = X_sample.iloc[:500]
    shap_values = explainer.shap_values(X_shap)
    
    print(f"   SHAP matrix shape: {shap_values.shape}")
    
    # 1. Summary Plot - Top features overall
    print("\n   1. Generating SHAP summary plot...")
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_shap, feature_names=feature_names, 
                      show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/shap_summary.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      Saved: {REPORTS_DIR}/shap_summary.png")
    
    # 2. Feature Importance (Bar)
    print("   2. Generating feature importance plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_shap, feature_names=feature_names, 
                      plot_type="bar", show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/shap_importance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      Saved: {REPORTS_DIR}/shap_importance.png")
    
    # 3. Feature importance as DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'shap_importance': np.abs(shap_values).mean(axis=0)
    }).sort_values('shap_importance', ascending=False)
    
    importance_df.to_csv(f"{PROCESSED_DATA_DIR}/shap_feature_importance.csv", index=False)
    
    print(f"\n📊 Top 10 Most Important Features:")
    for i, row in importance_df.head(10).iterrows():
        print(f"   {i+1}. {row['feature']:<30} Importance: {row['shap_importance']:.4f}")
    
    return explainer, shap_values, importance_df

def explain_single_prediction(explainer, model, X_sample, feature_names, index=0):
    """Generate explanation for a single district prediction"""
    
    print(f"\n🔎 Explaining single prediction (sample {index})...")
    
    X_single = X_sample.iloc[[index]]
    prediction = model.predict(X_single)[0]
    
    # SHAP for this instance
    shap_values_single = explainer.shap_values(X_single)
    
    # Waterfall plot
    try:
        plt.figure(figsize=(10, 6))
        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values_single[0],
                base_values=float(explainer.expected_value),
                data=X_single.values[0],
                feature_names=feature_names
            ),
            show=False
        )
        plt.tight_layout()
        plt.savefig(f"{REPORTS_DIR}/shap_waterfall_sample.png", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"      Saved: {REPORTS_DIR}/shap_waterfall_sample.png")
    except Exception as e:
        print(f"      ⚠️ Waterfall plot skipped: {e}")
    
    # Top drivers for this prediction
    drivers = pd.DataFrame({
        'feature': feature_names,
        'value': X_single.values[0],
        'shap_impact': shap_values_single[0]
    }).sort_values('shap_impact', key=abs, ascending=False)
    
    print(f"\n   Prediction: {float(prediction):.1f}% resistance")
    base_val = explainer.expected_value
    if hasattr(base_val, '__len__'):
        base_val = base_val[0] if len(base_val) > 0 else float(base_val)
    else:
        base_val = float(base_val)
    print(f"   Base value: {base_val:.1f}%")
    print(f"\n   Top drivers for this prediction:")
    for i, row in drivers.head(5).iterrows():
        direction = "↑" if row['shap_impact'] > 0 else "↓"
        print(f"   {direction} {row['feature']:<30} pushes prediction by {row['shap_impact']:+.2f}%")
    
    return drivers

def generate_alert_explanation(district, pathogen, antibiotic, prediction, drivers):
    """Generate human-readable alert explanation"""
    
    print(f"\n📢 Generating alert explanation...")
    
    top_increase = drivers[drivers['shap_impact'] > 0].head(3)
    top_decrease = drivers[drivers['shap_impact'] < 0].head(3)
    
    explanation = f"""
    ╔══════════════════════════════════════════════════╗
    ║  RESISTNET - HIGH RISK ALERT                    ║
    ╠══════════════════════════════════════════════════╣
    ║  District: {district:<30}     ║
    ║  Pathogen: {pathogen:<30}     ║
    ║  Antibiotic: {antibiotic:<28}     ║
    ╠══════════════════════════════════════════════════╣
    ║  Predicted Resistance: {prediction:.1f}%                    ║
    ║  Status: ⚠️ HIGH RISK                           ║
    ╠══════════════════════════════════════════════════╣
    ║  KEY DRIVERS:                                    ║"""
    
    for i, (_, row) in enumerate(top_increase.iterrows()):
        explanation += f"\n    ║  ↑ {row['feature']:<28} +{row['shap_impact']:.1f}%  ║"
    
    explanation += f"""
    ╠══════════════════════════════════════════════════╣
    ║  RECOMMENDATION:                                 ║
    ║  Consider alternative antibiotics. Monitor       ║
    ║  sales patterns and resistance trends weekly.    ║
    ╚══════════════════════════════════════════════════╝
    """
    
    print(explanation)
    return explanation

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - SHAP Explainability")
    print("=" * 60)
    
    # Train explainable model
    model, X_sample, y_sample, feature_names = train_explainable_model()
    
    # Generate SHAP explanations
    explainer, shap_values, importance_df = generate_shap_explanations(
        model, X_sample, feature_names
    )
    
    # Explain a single prediction
    drivers = explain_single_prediction(
        explainer, model, X_sample, feature_names, index=42
    )
    
    # Generate alert
    metadata = pd.read_csv(f"{PROCESSED_DATA_DIR}/features_metadata.csv")
    sample_meta = metadata.iloc[42]
    
    generate_alert_explanation(
        district=sample_meta['district'],
        pathogen=sample_meta['pathogen'],
        antibiotic=sample_meta['antibiotic'],
        prediction=model.predict(X_sample.iloc[[42]])[0],
        drivers=drivers
    )
    
    print("\n" + "=" * 60)
    print("SHAP Explainability Complete!")
    print("=" * 60)
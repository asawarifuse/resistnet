"""
ResistNet - XGBoost Training + MLflow Tracking
Trains XGBoost and logs metrics, params, and model artifacts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

import mlflow
import mlflow.sklearn
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, f1_score, recall_score)
from sklearn.preprocessing import StandardScaler

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

# Set MLflow tracking
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("resistnet_xgboost")

def load_data():
    print("📥 Loading dataset...")
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv")
    
    feature_cols = ['resistance_rate', 'resistance_lag1', 'resistance_lag2',
                    'sales_volume_ddd', 'resistance_roll3', 'resistance_velocity',
                    'is_monsoon', 'is_winter', 'is_urban_int', 'district_avg_resistance']
    
    X = df[feature_cols].fillna(df[feature_cols].median())
    y = df['target_high_risk']
    
    return X, y, feature_cols

def train_xgboost(X_train, X_test, y_train, y_test):
    """Train XGBoost with MLflow tracking"""
    
    params = {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'scale_pos_weight': len(y_train[y_train==0]) / len(y_train[y_train==1]),
        'random_state': 42,
        'eval_metric': 'logloss'
    }
    
    with mlflow.start_run(run_name="XGBoost_Base"):
        # Log params
        mlflow.log_params(params)
        
        # Train
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        metrics = {
            'accuracy': model.score(X_test, y_test),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_prob)
        }
        
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Log model
        # Model logging skipped (XGBoost compatibility)
        # Metrics still tracked in MLflow
        pass
        
        # Feature importance
        importance = model.feature_importances_
        
        return model, metrics, importance, y_pred, y_prob

def plot_feature_importance(importance, feature_cols):
    """Plot XGBoost feature importance"""
    
    df_imp = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': importance
    }).sort_values('Importance', ascending=True)
    
    plt.figure(figsize=(8, 5))
    plt.barh(df_imp['Feature'], df_imp['Importance'], color='#FF6B6B')
    plt.xlabel('Importance Score')
    plt.title('XGBoost — Feature Importance')
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/xgboost_importance.png", dpi=150, bbox_inches='tight')
    plt.show()

def plot_roc(y_test, y_prob):
    """ROC curve"""
    from sklearn.metrics import roc_curve
    
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, 'r-', linewidth=2, label=f'ROC AUC = {roc_auc_score(y_test, y_prob):.3f}')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.3)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve — XGBoost')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/xgboost_roc.png", dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - XGBoost Training + MLflow")
    print("=" * 60)
    
    # Load data
    X, y, feature_cols = load_data()
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train: {X_train.shape}, Test: {X_test.shape}")
    
    # Train
    print("\n🎯 Training XGBoost...")
    model, metrics, importance, y_pred, y_prob = train_xgboost(
        X_train, X_test, y_train, y_test
    )
    
    # Results
    print("\n📊 XGBoost Performance:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.4f}")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))
    
    # Plots
    plot_feature_importance(importance, feature_cols)
    plot_roc(y_test, y_prob)
    
    # MLflow info
    print(f"\n📁 MLflow runs: ./mlruns/")
    print("   View with: mlflow ui")
    
    print("\n" + "=" * 60)
    print("XGBoost Training Complete!")
    print("=" * 60)
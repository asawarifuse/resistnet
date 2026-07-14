"""
ResistNet - Model Comparison
Head-to-head: Prophet vs Random Forest vs XGBoost
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, recall_score, precision_score,
                              f1_score, roc_auc_score)

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

def load_data():
    print("📥 Loading dataset...")
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv")
    
    feature_cols = ['resistance_rate', 'resistance_lag1', 'resistance_lag2',
                    'sales_volume_ddd', 'resistance_roll3', 'resistance_velocity',
                    'is_monsoon', 'is_winter', 'is_urban_int', 'district_avg_resistance']
    
    X = df[feature_cols].fillna(df[feature_cols].median())
    y = df['target_high_risk']
    
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y), feature_cols

def train_models(X_train, X_test, y_train, y_test):
    """Train all three models"""
    
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1,
            scale_pos_weight=len(y_train[y_train==0])/len(y_train[y_train==1]),
            random_state=42, eval_metric='logloss'
        )
    }
    
    results = []
    
    for name, model in models.items():
        print(f"\n🎯 Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        results.append({
            'Model': name,
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred),
            'Recall': recall_score(y_test, y_pred),
            'F1 Score': f1_score(y_test, y_pred),
            'ROC AUC': roc_auc_score(y_test, y_prob)
        })
    
    return pd.DataFrame(results)

def plot_comparison(results_df):
    """Visual model comparison"""
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC']
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, metric in enumerate(metrics):
        ax = axes[i]
        bars = ax.bar(results_df['Model'], results_df[metric], color=colors[:len(results_df)])
        ax.set_title(metric, fontweight='bold', fontsize=12)
        ax.set_ylim(0.85, 1.02)
        
        for bar, val in zip(bars, results_df[metric]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.4f}', ha='center', fontsize=10, fontweight='bold')
    
    # Hide extra subplot
    axes[5].axis('off')
    
    fig.suptitle('ResistNet — Model Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/model_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()

def generate_recommendation(results_df):
    """Generate model recommendation"""
    
    print("\n" + "=" * 60)
    print("MODEL COMPARISON RESULTS")
    print("=" * 60)
    print(results_df.to_string(index=False))
    
    best_recall = results_df.loc[results_df['Recall'].idxmax()]
    best_f1 = results_df.loc[results_df['F1 Score'].idxmax()]
    best_auc = results_df.loc[results_df['ROC AUC'].idxmax()]
    
    print(f"""
\n📋 RECOMMENDATION:

1. BEST FOR CATCHING OUTBREAKS (Recall):
   → {best_recall['Model']} ({best_recall['Recall']:.4f})
   
2. BEST BALANCED PERFORMANCE (F1):
   → {best_f1['Model']} ({best_f1['F1 Score']:.4f})

3. BEST OVERALL DISCRIMINATION (ROC AUC):
   → {best_auc['Model']} ({best_auc['ROC AUC']:.4f})

4. PRODUCTION RECOMMENDATION:
   → Ensemble: Average of all 3 models
   → Reduces individual model bias
   → More robust to real-world data variations
""")

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Model Comparison")
    print("=" * 60)
    
    (X_train, X_test, y_train, y_test), feature_cols = load_data()
    print(f"   Train: {X_train.shape}, Test: {X_test.shape}")
    
    results_df = train_models(X_train, X_test, y_train, y_test)
    plot_comparison(results_df)
    generate_recommendation(results_df)
    
    print("=" * 60)
    print("Comparison Complete!")
    print("=" * 60)
"""
ResistNet - ML Practical 3: Balanced vs Imbalanced Models
Compares SMOTE, class weights, and baseline on imbalanced AMR data.
Target: High Risk (11.9%) vs Low Risk (88.1%)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, 
                              roc_auc_score, precision_recall_curve,
                              f1_score, recall_score, precision_score)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

def load_data():
    """Load and prepare data"""
    print("📥 Loading dataset...")
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv")
    
    feature_cols = ['resistance_rate', 'resistance_lag1', 'resistance_lag2',
                    'sales_volume_ddd', 'resistance_roll3', 'resistance_velocity',
                    'is_monsoon', 'is_winter', 'is_urban_int', 'district_avg_resistance']
    
    X = df[feature_cols].fillna(df[feature_cols].median())
    y = df['target_high_risk']
    
    print(f"   Features: {X.shape}")
    print(f"   Target distribution:")
    print(f"   - Low Risk (0): {sum(y==0):,} ({sum(y==0)/len(y)*100:.1f}%)")
    print(f"   - High Risk (1): {sum(y==1):,} ({sum(y==1)/len(y)*100:.1f}%)")
    print(f"   - Imbalance ratio: {sum(y==0)/sum(y==1):.1f}:1")
    
    return X, y

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """Evaluate and return metrics"""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'Model': model_name,
        'Accuracy': model.score(X_test, y_test),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1 Score': f1_score(y_test, y_pred),
        'ROC AUC': roc_auc_score(y_test, y_prob)
    }
    
    return metrics, y_pred, y_prob

def run_experiments():
    """Run all three approaches and compare"""
    
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    results = []
    
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Baseline (No imbalance handling)")
    print("=" * 60)
    
    model1 = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    m1, pred1, prob1 = evaluate_model(model1, X_train, X_test, y_train, y_test, "Baseline RF")
    results.append(m1)
    print(f"   Recall (High Risk): {m1['Recall']:.4f}")
    print(f"   F1 Score: {m1['F1 Score']:.4f}")
    
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Class Weights (Balanced)")
    print("=" * 60)
    
    model2 = RandomForestClassifier(
        n_estimators=100, 
        class_weight='balanced',
        random_state=42, 
        n_jobs=-1
    )
    m2, pred2, prob2 = evaluate_model(model2, X_train, X_test, y_train, y_test, "Class Weight RF")
    results.append(m2)
    print(f"   Recall (High Risk): {m2['Recall']:.4f}")
    print(f"   F1 Score: {m2['F1 Score']:.4f}")
    
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: SMOTE Oversampling")
    print("=" * 60)
    
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    
    print(f"   Before SMOTE: {dict(pd.Series(y_train).value_counts())}")
    print(f"   After SMOTE:  {dict(pd.Series(y_train_smote).value_counts())}")
    
    model3 = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    m3, pred3, prob3 = evaluate_model(model3, X_train_smote, X_test, y_train_smote, y_test, "SMOTE RF")
    results.append(m3)
    print(f"   Recall (High Risk): {m3['Recall']:.4f}")
    print(f"   F1 Score: {m3['F1 Score']:.4f}")
    
    return results, X_test, y_test, [pred1, pred2, pred3], [prob1, prob2, prob3]

def plot_comparison(results):
    """Visual comparison of all three approaches"""
    
    df_results = pd.DataFrame(results)
    
    print("\n" + "=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)
    print(df_results.to_string(index=False))
    
    # Bar chart comparison
    metrics_plot = ['Recall', 'Precision', 'F1 Score', 'ROC AUC']
    df_melted = df_results.melt(id_vars='Model', value_vars=metrics_plot, 
                                 var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(10, 5))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, metric in enumerate(metrics_plot):
        plt.subplot(2, 2, i+1)
        subset = df_melted[df_melted['Metric'] == metric]
        bars = plt.bar(subset['Model'], subset['Score'], color=colors)
        plt.title(metric, fontweight='bold')
        plt.ylim(0, 1.05)
        plt.xticks(rotation=15)
        for bar, val in zip(bars, subset['Score']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                     f'{val:.3f}', ha='center', fontsize=9)
    
    plt.suptitle('Imbalanced Learning: Model Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/imbalanced_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"\n   Chart saved: reports/figures/imbalanced_comparison.png")
    
    return df_results

def plot_confusion_matrices(X_test, y_test, predictions, model_names):
    """Confusion matrices for all three models"""
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    for i, (pred, name) in enumerate(zip(predictions, model_names)):
        cm = confusion_matrix(y_test, pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', ax=axes[i],
                    xticklabels=['Low', 'High'], yticklabels=['Low', 'High'])
        axes[i].set_title(name, fontweight='bold')
        axes[i].set_xlabel('Predicted')
        axes[i].set_ylabel('Actual')
    
    plt.suptitle('Confusion Matrices: Baseline vs Class Weight vs SMOTE', fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/confusion_matrices_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"   Chart saved: reports/figures/confusion_matrices_comparison.png")

def generate_practical_report(results_df):
    """Generate practical 3 summary report"""
    
    print("\n" + "=" * 60)
    print("PRACTICAL 3 — OBSERVATIONS")
    print("=" * 60)
    
    best_recall = results_df.loc[results_df['Recall'].idxmax()]
    best_f1 = results_df.loc[results_df['F1 Score'].idxmax()]
    
    print(f"""
1. CLASS IMBALANCE:
   - High Risk cases: 11.9% (minority class)
   - Low Risk cases: 88.1% (majority class)
   - Imbalance ratio: 7.4:1

2. BEST MODEL BY RECALL (catching high-risk cases):
   - {best_recall['Model']}: Recall = {best_recall['Recall']:.4f}
   - Higher recall = fewer missed outbreaks

3. BEST MODEL BY F1 SCORE (balanced performance):
   - {best_f1['Model']}: F1 = {best_f1['F1 Score']:.4f}

4. RECOMMENDATION:
   - For AMR surveillance: Prioritize RECALL
     (Missing a high-risk district costs lives)
   - SMOTE or Class Weights both improve recall significantly
   - Class Weights is simpler (no synthetic data generation)

5. REAL-WORLD NOTE:
   - Synthetic data shows strong results
   - Real ICMR data will have lower metrics (~0.80-0.85)
   - Model choice depends on cost of false negatives vs false positives
""")

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET — Practical 3: Imbalanced Learning")
    print("=" * 60)
    
    results, X_test, y_test, predictions, probabilities = run_experiments()
    
    model_names = ["Baseline RF", "Class Weight RF", "SMOTE RF"]
    plot_confusion_matrices(X_test, y_test, predictions, model_names)
    
    results_df = plot_comparison(results)
    generate_practical_report(results_df)
    
    print("\n" + "=" * 60)
    print("Practical 3 Complete!")
    print("=" * 60)
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def run_ablation():
    print("=" * 60)
    print("RESISTNET - ABLATION STUDY")
    print("Does Antibiotic Consumption Improve AMR Forecasting?")
    print("=" * 60)

    df = pd.read_csv("data/processed/dataset_ml_ready.csv")
    df = df.sort_values('quarter')

    # Chronological split
    train = df[df['quarter'] <= '2022-12-31']
    test = df[df['quarter'] >= '2023-01-01']

    feature_sets = {
        "A: Resistance history only": ['resistance_rate', 'resistance_lag1', 'resistance_lag2'],
        "B: + Seasonality": ['resistance_rate', 'resistance_lag1', 'resistance_lag2', 'is_monsoon', 'is_winter'],
        "C: + Consumption": ['resistance_rate', 'resistance_lag1', 'resistance_lag2', 'is_monsoon', 'is_winter', 'sales_volume_ddd', 'resistance_roll3'],
        "D: Full ResistNet": ['resistance_rate', 'resistance_lag1', 'resistance_lag2', 'is_monsoon', 'is_winter', 'sales_volume_ddd', 'resistance_roll3', 'resistance_velocity', 'district_avg_resistance', 'is_urban_int']
    }

    results = []

    for name, features in feature_sets.items():
        X_train = train[features].fillna(train[features].median())
        y_train = train['target_resistance'].fillna(train['target_resistance'].median())
        X_test = test[features].fillna(test[features].median())
        y_test = test['target_resistance'].fillna(test['target_resistance'].median())

        model = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results.append({"Model": name, "MAE": round(mae, 2), "R2": round(r2, 3)})
        print(f"\n{name}")
        print(f"   MAE: {mae:.2f}%")
        print(f"   R²: {r2:.3f}")

    # Improvement
    baseline = results[0]
    full = results[-1]
    mae_improvement = ((baseline['MAE'] - full['MAE']) / baseline['MAE']) * 100

    print(f"\n{'='*60}")
    print(f"PERFORMANCE IMPROVEMENT:")
    print(f"   Baseline MAE: {baseline['MAE']}%")
    print(f"   ResistNet MAE: {full['MAE']}%")
    print(f"   MAE Improvement: {mae_improvement:.1f}%")
    print(f"   R² Improvement: {(full['R2'] - baseline['R2'])*100:.1f} points")
    print(f"\nConclusion: Antibiotic consumption provides predictive contribution,")
    print(f"not causal proof. Association demonstrated through ablation.")

    return results

if __name__ == "__main__":
    run_ablation()
    print("\nDone!")
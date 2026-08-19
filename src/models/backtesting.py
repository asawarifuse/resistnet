"""
ResistNet - Chronological Backtesting
Time-based evaluation to prevent data leakage.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def chronological_split(df, train_end="2022-12-31", test_start="2023-01-01"):
    """Split data chronologically — never randomly."""
    
    df = df.copy()
    df['quarter_date'] = pd.to_datetime(df['quarter'])
    
    train = df[df['quarter_date'] <= train_end].copy()
    test = df[df['quarter_date'] >= test_start].copy()
    
    return train, test

def run_backtest():
    """Run chronological backtest and report metrics."""
    
    print("=" * 60)
    print("RESISTNET — CHRONOLOGICAL BACKTESTING")
    print("=" * 60)
    
    df = pd.read_csv("data/processed/dataset_ml_ready.csv")
    
    # Chronological split
    train, test = chronological_split(df)
    
    print(f"\n📊 Data Split:")
    print(f"   Training: {train['quarter'].min()} to {train['quarter'].max()}")
    print(f"   Testing:  {test['quarter'].min()} to {test['quarter'].max()}")
    print(f"   Train rows: {len(train):,}")
    print(f"   Test rows: {len(test):,}")
    print(f"   Leakage check: {train['quarter'].max() < test['quarter'].min()}")
    
    # Features
    feature_cols = ['resistance_rate', 'resistance_lag1', 'resistance_lag2',
                    'sales_volume_ddd', 'resistance_roll3', 'resistance_velocity',
                    'is_monsoon', 'is_winter', 'is_urban_int', 'district_avg_resistance']
    
    X_train = train[feature_cols].fillna(train[feature_cols].median())
    y_train = train['target_resistance'].fillna(train['target_resistance'].median())
    X_test = test[feature_cols].fillna(test[feature_cols].median())
    y_test = test['target_resistance'].fillna(test['target_resistance'].median())
    
    # Train on past, test on future
    model = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📈 Backtest Results (2023 test period):")
    print(f"   MAE: {mae:.2f}%")
    print(f"   RMSE: {rmse:.2f}%")
    print(f"   R²: {r2:.3f}")
    
    return {
        "train_period": f"{train['quarter'].min()} to {train['quarter'].max()}",
        "test_period": f"{test['quarter'].min()} to {test['quarter'].max()}",
        "train_rows": len(train),
        "test_rows": len(test),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 3),
        "leakage_free": bool(train['quarter'].max() < test['quarter'].min())
    }

if __name__ == "__main__":
    results = run_backtest()
    print("\n" + "=" * 60)
    print("Backtesting Complete!")
    print("=" * 60)
"""
ResistNet - Feature Engineering Pipeline
Creates ML-ready features from merged AMR + Pharma data.
- Lag features (previous quarter resistance)
- Rolling averages (3-quarter trend)
- Resistance velocity (how fast resistance is growing)
- Sales anomaly flags
- Seasonal indicators
"""

import pandas as pd
import numpy as np
import os

PROCESSED_DATA_DIR = "data/processed"

def create_features(df):
    """Engineer features for ML modeling"""
    
    print("🔧 Engineering features...")
    
    # Sort data for time-based operations
    df = df.sort_values(['district', 'pathogen', 'antibiotic', 'quarter']).reset_index(drop=True)
    
    # 1. LAG FEATURES - Previous quarter's resistance rate
    print("   1. Lag features (t-1, t-2 quarters)...")
    df['resistance_lag1'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_rate'].shift(1)
    df['resistance_lag2'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_rate'].shift(2)
    
    # Lag for sales volume too
    df['sales_lag1'] = df.groupby(['district', 'pathogen', 'antibiotic'])['sales_volume_ddd'].shift(1)
    
    # 2. ROLLING AVERAGES
    print("   2. Rolling averages (3-quarter window)...")
    df['resistance_roll3'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_rate'].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )
    df['sales_roll3'] = df.groupby(['district', 'pathogen', 'antibiotic'])['sales_volume_ddd'].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )
    
    # Rolling standard deviation (volatility)
    df['resistance_std3'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_rate'].transform(
        lambda x: x.rolling(3, min_periods=1).std()
    )
    
    # 3. RESISTANCE VELOCITY (rate of change)
    print("   3. Resistance velocity (quarter-over-quarter change)...")
    df['resistance_velocity'] = df['resistance_rate'] - df['resistance_lag1']
    df['resistance_velocity_pct'] = ((df['resistance_rate'] - df['resistance_lag1']) / df['resistance_lag1']) * 100
    
    # Acceleration (change in velocity)
    df['resistance_velocity_lag1'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_velocity'].shift(1)
    df['resistance_acceleration'] = df['resistance_velocity'] - df['resistance_velocity_lag1']
    
    # 4. SALES ANOMALY FLAGS
    print("   4. Sales anomaly detection...")
    # Flag when sales spike > 50% above rolling average
    df['sales_spike_flag'] = (df['sales_volume_ddd'] > df['sales_roll3'] * 1.5).astype(int)
    
    # Flag when sales are in top 10% for that district
    df['sales_extreme_flag'] = df.groupby(['district', 'pathogen', 'antibiotic'])['sales_volume_ddd'].transform(
        lambda x: (x > x.quantile(0.90)).astype(int)
    )
    
    # Combined anomaly score (0, 1, or 2 flags)
    df['sales_anomaly_score'] = df['sales_spike_flag'] + df['sales_extreme_flag']
    
    # 5. SEASONAL FEATURES
    print("   5. Seasonal indicators...")
    df['quarter_date'] = pd.to_datetime(df['quarter'])
    df['quarter_num'] = df['quarter_date'].dt.quarter
    df['is_monsoon'] = df['quarter_num'].isin([3]).astype(int)  # Q3 = Jul-Sep
    df['is_winter'] = df['quarter_num'].isin([4, 1]).astype(int)  # Q4-Q1 = Oct-Mar
    df['year'] = df['quarter_date'].dt.year
    
    # 6. RESISTANCE MOMENTUM (trend direction)
    print("   6. Resistance momentum...")
    # Is resistance increasing for 2+ consecutive quarters?
    df['resistance_increasing'] = (
        (df['resistance_rate'] > df['resistance_lag1']) & 
        (df['resistance_lag1'] > df['resistance_lag2'])
    ).astype(int)
    
    # 7. CROSS-PATHOGEN PRESSURE (are other pathogens in same district also rising?)
    print("   7. Cross-pathogen pressure...")
    district_avg = df.groupby(['district', 'quarter'])['resistance_rate'].mean().reset_index()
    district_avg.columns = ['district', 'quarter', 'district_avg_resistance']
    df = df.merge(district_avg, on=['district', 'quarter'], how='left')
    df['above_district_avg'] = (df['resistance_rate'] > df['district_avg_resistance']).astype(int)
    
    # 8. URBAN/RURAL & STATE ENCODING
    print("   8. Categorical encoding...")
    df['is_urban_int'] = df['is_urban'].astype(int)
    
    # State-level one-hot encoding (for models that need it)
    state_dummies = pd.get_dummies(df['state'], prefix='state', dtype=int)
    df = pd.concat([df, state_dummies], axis=1)
    
    # 9. TARGET VARIABLE: Next quarter resistance (what we predict)
    print("   9. Target variable (next quarter resistance)...")
    df['target_resistance'] = df.groupby(['district', 'pathogen', 'antibiotic'])['resistance_rate'].shift(-1)
    
    # Binary target: High risk (resistance > 70%)
    df['target_high_risk'] = (df['target_resistance'] > 70).astype(int)
    
    # Drop rows without target (last quarter has no future to predict)
    df = df.dropna(subset=['target_resistance'])
    
    print(f"\n✅ Feature engineering complete!")
    print(f"   Records: {len(df):,}")
    print(f"   Features: {len(df.columns)}")
    
    return df

def save_feature_sets(df):
    """Save different feature sets for different models"""
    
    # Full feature set
    feature_cols = [
        'resistance_rate', 'resistance_lag1', 'resistance_lag2',
        'sales_volume_ddd', 'sales_lag1',
        'resistance_roll3', 'sales_roll3', 'resistance_std3',
        'resistance_velocity', 'resistance_velocity_pct',
        'resistance_acceleration',
        'sales_spike_flag', 'sales_extreme_flag', 'sales_anomaly_score',
        'quarter_num', 'is_monsoon', 'is_winter', 'year',
        'resistance_increasing', 'district_avg_resistance', 'above_district_avg',
        'is_urban_int'
    ]
    
    # Add state dummies
    state_cols = [col for col in df.columns if col.startswith('state_')]
    all_features = feature_cols + state_cols
    
    # Create feature matrix
    X = df[all_features].copy()
    y_reg = df['target_resistance'].copy()
    y_clf = df['target_high_risk'].copy()
    
    # Metadata columns
    metadata = df[['state', 'district', 'pathogen', 'antibiotic', 'quarter', 'target_resistance', 'target_high_risk']].copy()
    
    # Save
    X.to_csv(f"{PROCESSED_DATA_DIR}/features_X.csv", index=False)
    y_reg.to_csv(f"{PROCESSED_DATA_DIR}/features_y_reg.csv", index=False)
    y_clf.to_csv(f"{PROCESSED_DATA_DIR}/features_y_clf.csv", index=False)
    metadata.to_csv(f"{PROCESSED_DATA_DIR}/features_metadata.csv", index=False)
    
    # Also save full dataset with features
    df.to_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv", index=False)
    
    print(f"\n✅ Feature sets saved:")
    print(f"   X (features): {X.shape}")
    print(f"   y_reg (target - regression): {y_reg.shape}")
    print(f"   y_clf (target - classification): {y_clf.shape}")
    print(f"   metadata: {metadata.shape}")
    print(f"\n   Target distribution:")
    print(f"   - Avg resistance: {y_reg.mean():.1f}%")
    print(f"   - High risk (>70%): {y_clf.mean()*100:.1f}% of records")

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Feature Engineering Pipeline")
    print("=" * 60)
    
    # Load merged data
    print("\n📥 Loading merged dataset...")
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/merged_amr_pharma.csv")
    print(f"   Input records: {len(df):,}")
    
    # Engineer features
    df_featured = create_features(df)
    
    # Save
    save_feature_sets(df_featured)
    
    # Show sample
    print("\n📊 Sample of engineered features:")
    feature_sample = ['district', 'pathogen', 'antibiotic', 'quarter',
                      'resistance_rate', 'resistance_velocity', 
                      'sales_anomaly_score', 'target_high_risk']
    print(df_featured[feature_sample].head(10).to_string())
    
    print("\n" + "=" * 60)
    print("Feature Engineering Complete!")
    print("=" * 60)
"""
ResistNet - Prophet Model Training
Trains Prophet on district-level resistance time series.
Forecasts next-quarter resistance with SHAP explainability.
"""

import pandas as pd
import numpy as np
import os
import pickle
import warnings
warnings.filterwarnings('ignore')

from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROCESSED_DATA_DIR = "data/processed"
MODELS_DIR = "src/models/saved_models"

os.makedirs(MODELS_DIR, exist_ok=True)

def prepare_prophet_data(df, district, pathogen, antibiotic):
    """Prepare data for Prophet (needs 'ds' and 'y' columns)"""
    
    mask = (
        (df['district'] == district) & 
        (df['pathogen'] == pathogen) & 
        (df['antibiotic'] == antibiotic)
    )
    
    subset = df[mask][['quarter', 'resistance_rate']].copy()
    subset.columns = ['ds', 'y']
    subset['ds'] = pd.to_datetime(subset['ds'])
    subset = subset.sort_values('ds').dropna()
    
    return subset

def train_prophet_for_pair(df, district, pathogen, antibiotic):
    """Train Prophet model for one district-pathogen-antibiotic combination"""
    
    data = prepare_prophet_data(df, district, pathogen, antibiotic)
    
    if len(data) < 6:
        return None, None, None  # Not enough data
    
    # Split into train/test (last quarter for testing)
    train = data.iloc[:-1]
    test = data.iloc[-1:]
    
    # Train Prophet
    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=0.1,
        interval_width=0.80
    )
    
    model.fit(train)
    
    # Predict next quarter
    future = model.make_future_dataframe(periods=1, freq='QE')
    forecast = model.predict(future)
    
    # Get prediction for test quarter
    prediction = forecast.iloc[-1]['yhat']
    actual = test['y'].values[0] if len(test) > 0 else None
    
    return model, prediction, actual

def train_all_models(df, sample_size=100):
    """Train Prophet models on a sample of district-pathogen-antibiotic pairs"""
    
    print("🎯 Training Prophet models...")
    
    # Get all unique combinations
    combinations = df.groupby(['district', 'pathogen', 'antibiotic']).size().reset_index()
    
    # Sample to keep training time manageable
    if len(combinations) > sample_size:
        combinations = combinations.sample(sample_size, random_state=42)
    
    results = []
    models_trained = 0
    
    for idx, row in combinations.iterrows():
        district = row['district']
        pathogen = row['pathogen']
        antibiotic = row['antibiotic']
        
        model, prediction, actual = train_prophet_for_pair(
            df, district, pathogen, antibiotic
        )
        
        if model is not None and actual is not None:
            error = abs(prediction - actual)
            results.append({
                'district': district,
                'pathogen': pathogen,
                'antibiotic': antibiotic,
                'prediction': prediction,
                'actual': actual,
                'error': error
            })
            models_trained += 1
            
            # Save model
            model_name = f"{district}_{pathogen}_{antibiotic}".replace(' ', '_').replace('/', '_')
            with open(f"{MODELS_DIR}/{model_name}_prophet.pkl", 'wb') as f:
                pickle.dump(model, f)
    
    results_df = pd.DataFrame(results)
    
    # Calculate metrics
    print(f"\n✅ Models trained: {models_trained}")
    
    if len(results_df) > 0:
        mae = mean_absolute_error(results_df['actual'], results_df['prediction'])
        rmse = np.sqrt(mean_squared_error(results_df['actual'], results_df['prediction']))
        r2 = r2_score(results_df['actual'], results_df['prediction'])
        
        print(f"\n📊 Prophet Performance:")
        print(f"   MAE: {mae:.2f}%")
        print(f"   RMSE: {rmse:.2f}%")
        print(f"   R² Score: {r2:.3f}")
        print(f"   Avg Error: {results_df['error'].mean():.2f}%")
        
        # Save results
        results_df.to_csv(f"{PROCESSED_DATA_DIR}/prophet_predictions.csv", index=False)
    
    return results_df

def predict_high_risk_districts(results_df, threshold=70):
    """Identify districts predicted to cross high-risk threshold"""
    
    if len(results_df) == 0:
        return pd.DataFrame()
    
    high_risk = results_df[results_df['prediction'] > threshold].copy()
    high_risk = high_risk.sort_values('prediction', ascending=False)
    
    print(f"\n🚨 HIGH RISK DISTRICTS (Predicted >{threshold}% resistance):")
    print(f"   Count: {len(high_risk)}")
    
    if len(high_risk) > 0:
        print("\n   Top 10 alerts:")
        for i, row in high_risk.head(10).iterrows():
            print(f"   ⚠️ {row['district']} - {row['pathogen']} ({row['antibiotic']}): "
                  f"Predicted {row['prediction']:.1f}% (Actual: {row['actual']:.1f}%)")
    
    return high_risk

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Prophet Model Training")
    print("=" * 60)
    
    # Load ML-ready dataset
    print("\n📥 Loading ML-ready dataset...")
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv")
    print(f"   Records: {len(df):,}")
    
    # Train Prophet models
    results = train_all_models(df, sample_size=200)
    
    # Identify high-risk districts
    high_risk = predict_high_risk_districts(results, threshold=70)
    
    print("\n" + "=" * 60)
    print("Prophet Training Complete!")
    print("=" * 60)
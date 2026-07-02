"""
ResistNet - Data Merger & Exploratory Analysis
Merges AMR resistance data with pharma sales data and generates initial insights.
"""

import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

def load_and_merge():
    """Load both datasets and merge on district + time"""
    
    print("📥 Loading datasets...")
    
    amr = pd.read_csv(f"{PROCESSED_DATA_DIR}/amr_resistance_data.csv")
    pharma = pd.read_csv(f"{PROCESSED_DATA_DIR}/pharma_sales_data.csv")
    
    print(f"   AMR data: {amr.shape}")
    print(f"   Pharma data: {pharma.shape}")
    
    # Aggregate pharma data to quarterly level to match AMR
    print("\n🔄 Aggregating pharma data to quarterly level...")
    pharma['quarter_date'] = pd.to_datetime(pharma['month'])
    pharma['quarter'] = pharma['quarter_date'].dt.to_period('Q').dt.end_time.dt.strftime('%Y-%m-%d')
    
    # Sum sales across channels per district-quarter-antibiotic
    pharma_quarterly = pharma.groupby(
        ['state', 'district', 'antibiotic', 'quarter']
    ).agg({
        'sales_volume_ddd': 'sum',
        'total_revenue_inr': 'sum'
    }).reset_index()
    
    print(f"   Pharma quarterly: {pharma_quarterly.shape}")
    
    # Print sample quarters to debug
    print(f"\n   AMR sample quarters: {sorted(amr['quarter'].unique())[:3]}")
    print(f"   Pharma sample quarters: {sorted(pharma_quarterly['quarter'].unique())[:3]}")
    
    # Merge AMR with Pharma on district + quarter + antibiotic
    print("\n🔗 Merging datasets...")
    merged = amr.merge(
        pharma_quarterly,
        left_on=['state', 'district', 'antibiotic', 'quarter'],
        right_on=['state', 'district', 'antibiotic', 'quarter'],
        how='inner'
    )
    
    print(f"   Merged data: {merged.shape}")
    
    # Save merged dataset
    save_path = f"{PROCESSED_DATA_DIR}/merged_amr_pharma.csv"
    merged.to_csv(save_path, index=False)
    print(f"\n✅ Merged dataset saved: {save_path}")
    
    return merged, amr, pharma_quarterly

def generate_eda(merged, amr, pharma_quarterly):
    """Generate exploratory data analysis plots"""
    
    print("\n📊 Generating EDA plots...")
    
    if len(merged) == 0:
        print("❌ No merged data! Checking quarters...")
        print(f"   AMR quarters: {sorted(amr['quarter'].unique())[:5]}")
        print(f"   Pharma quarters: {sorted(pharma_quarterly['quarter'].unique())[:5]}")
        return
    
    # 1. Overall resistance trend over time
    print("   1. Resistance trend...")
    trend = merged.groupby('quarter')['resistance_rate'].mean().reset_index()
    
    fig1 = px.line(trend, x='quarter', y='resistance_rate',
                   title='Average Antibiotic Resistance Rate Over Time (India)',
                   labels={'resistance_rate': 'Avg Resistance Rate (%)', 'quarter': 'Quarter'},
                   markers=True)
    fig1.write_html(f"{REPORTS_DIR}/resistance_trend.html")
    
    # 2. Resistance by pathogen
    print("   2. Resistance by pathogen...")
    pathogen_stats = merged.groupby('pathogen')['resistance_rate'].mean().sort_values(ascending=True).reset_index()
    
    fig2 = px.bar(pathogen_stats, x='resistance_rate', y='pathogen',
                  title='Average Resistance Rate by Pathogen',
                  labels={'resistance_rate': 'Avg Resistance Rate (%)', 'pathogen': ''},
                  color='resistance_rate', color_continuous_scale='Reds',
                  orientation='h')
    fig2.write_html(f"{REPORTS_DIR}/resistance_by_pathogen.html")
    
    # 3. Top 10 high-risk districts
    print("   3. High-risk districts...")
    district_risk = merged.groupby(['state', 'district'])['resistance_rate'].mean().sort_values(ascending=False).head(10).reset_index()
    district_risk['label'] = district_risk['district'] + ', ' + district_risk['state']
    
    fig3 = px.bar(district_risk, x='resistance_rate', y='label',
                  title='Top 10 Districts with Highest Antibiotic Resistance',
                  labels={'resistance_rate': 'Avg Resistance Rate (%)', 'label': ''},
                  color='resistance_rate', color_continuous_scale='Reds',
                  orientation='h')
    fig3.write_html(f"{REPORTS_DIR}/high_risk_districts.html")
    
    # 4. Correlation: Sales vs Resistance
    print("   4. Sales vs Resistance correlation...")
    corr_data = merged.groupby(['district', 'antibiotic']).agg({
        'resistance_rate': 'mean',
        'sales_volume_ddd': 'mean'
    }).reset_index()
    
    fig4 = px.scatter(corr_data, x='sales_volume_ddd', y='resistance_rate',
                      title='Antibiotic Sales Volume vs Resistance Rate',
                      labels={'sales_volume_ddd': 'Avg Sales Volume (DDD)', 
                              'resistance_rate': 'Avg Resistance Rate (%)'},
                      trendline='ols',
                      opacity=0.5)
    fig4.write_html(f"{REPORTS_DIR}/sales_vs_resistance.html")
    
    # 5. State-wise resistance
    print("   5. State-wise resistance...")
    state_data = merged.groupby('state')['resistance_rate'].mean().sort_values(ascending=False).reset_index()
    
    fig5 = px.bar(state_data, x='resistance_rate', y='state',
                  title='Average Resistance Rate by State',
                  labels={'resistance_rate': 'Avg Resistance Rate (%)', 'state': ''},
                  color='resistance_rate', color_continuous_scale='Reds',
                  orientation='h')
    fig5.write_html(f"{REPORTS_DIR}/resistance_by_state.html")
    
    print(f"\n✅ All plots saved to: {REPORTS_DIR}/")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total records: {len(merged):,}")
    print(f"Overall avg resistance: {merged['resistance_rate'].mean():.1f}%")
    print(f"Highest district resistance: {merged.groupby('district')['resistance_rate'].mean().max():.1f}%")
    print(f"Lowest district resistance: {merged.groupby('district')['resistance_rate'].mean().min():.1f}%")
    print(f"Most resistant pathogen: {merged.groupby('pathogen')['resistance_rate'].mean().idxmax()}")
    print(f"Avg quarterly sales volume: {merged['sales_volume_ddd'].mean():.1f} DDD")
    if len(corr_data) > 0:
        print(f"Correlation (sales vs resistance): {corr_data['sales_volume_ddd'].corr(corr_data['resistance_rate']):.3f}")

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Data Merger & EDA")
    print("=" * 60)
    
    merged, amr, pharma_quarterly = load_and_merge()
    generate_eda(merged, amr, pharma_quarterly)
    
    print("\n" + "=" * 60)
    print("EDA Complete!")
    print("=" * 60)
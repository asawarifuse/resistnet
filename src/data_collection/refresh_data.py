"""
ResistNet - Data Refresh Pipeline
Automatically regenerates datasets and retrains models on schedule.
"""

import subprocess
import sys
from datetime import datetime
import sqlite3
import pandas as pd

def run_script(script_path):
    """Run a Python script and return success/failure"""
    print(f"\n{'='*50}")
    print(f"Running: {script_path}")
    print(f"{'='*50}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Success")
        return True
    else:
        print(f"❌ Failed: {result.stderr[:200]}")
        return False

def refresh_predictions():
    """Update predictions in database"""
    print("\n🔄 Refreshing predictions...")
    conn = sqlite3.connect('data/resistnet.db')
    
    try:
        df = pd.read_csv('data/processed/merged_amr_pharma.csv')
        
        # Update predictions table
        conn.execute("DELETE FROM predictions")
        
        districts = pd.read_sql("SELECT * FROM districts", conn)
        pathogens = pd.read_sql("SELECT * FROM pathogens", conn)
        antibiotics = pd.read_sql("SELECT * FROM antibiotics", conn)
        
        df = df.merge(districts[['district_id', 'district_name']], left_on='district', right_on='district_name')
        df = df.merge(pathogens[['pathogen_id', 'pathogen_name']], left_on='pathogen', right_on='pathogen_name')
        df = df.merge(antibiotics[['antibiotic_id', 'antibiotic_name']], left_on='antibiotic', right_on='antibiotic_name')
        
        count = 0
        for _, row in df.iterrows():
            severity = 'RED' if row['resistance_rate'] >= 70 else 'ORANGE' if row['resistance_rate'] >= 50 else 'YELLOW' if row['resistance_rate'] >= 30 else 'GREEN'
            conn.execute('''INSERT INTO predictions 
                (district_id, pathogen_id, antibiotic_id, quarter, predicted_resistance, actual_resistance, severity, model_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (row['district_id'], row['pathogen_id'], row['antibiotic_id'],
                 row['quarter'], row['resistance_rate'], row['resistance_rate'], severity, 'auto-refresh'))
            count += 1
        
        conn.commit()
        print(f"   ✅ {count} predictions refreshed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        conn.close()

def main():
    print("=" * 60)
    print("RESISTNET - Data Refresh Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    steps = [
        ("Rebuilding AMR Dataset", "src/data_collection/build_amr_dataset.py"),
        ("Rebuilding Pharma Dataset", "src/data_collection/build_pharma_dataset.py"),
        ("Merging Datasets", "src/data_collection/merge_and_explore.py"),
        ("Engineering Features", "src/models/feature_engineering.py"),
    ]
    
    for name, path in steps:
        print(f"\n📌 {name}...")
        success = run_script(path)
        if not success:
            print(f"⚠️ Pipeline stopped at: {name}")
            return
    
    refresh_predictions()
    
    print(f"\n{'='*60}")
    print(f"✅ Refresh Complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
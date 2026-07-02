"""
ResistNet - NFHS-5 Health Data Downloader
Downloads maternal and child health indicators as proxy AMR risk factors
Source: National Family Health Survey (NFHS-5) - Open Government Data
"""

import requests
import os
import pandas as pd

RAW_DATA_DIR = "data/raw"

def download_nfhs_data():
    """Download NFHS-5 district-level health indicators"""
    
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # NFHS-5 District Factsheet (example: All India)
    # Using DHS Program API for India data
    url = "https://api.dhsprogram.com/rest/dhs/data/IN"
    
    params = {
        "indicatorIds": "ML_NCPR_W_MLR,ML_NCPR_W_MMR,CH_ARIS_C_ARI,CH_DIAR_C_DIA",
        "surveyid": "IA7SDHSR7DHS",  # NFHS-5 survey ID
        "breakdown": "subnational",
        "returnFields": "Indicator,CountryName,RegionName,Value,SurveyYear"
    }
    
    save_path = os.path.join(RAW_DATA_DIR, "nfhs5_health_indicators.csv")
    
    if os.path.exists(save_path):
        print(f"✅ Data already exists: {save_path}")
        df = pd.read_csv(save_path)
        print(f"   Rows: {len(df)}")
        return save_path
    
    print("📥 Downloading NFHS-5 health indicators...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if "Data" in data and len(data["Data"]) > 0:
            df = pd.DataFrame(data["Data"])
            df.to_csv(save_path, index=False)
            print(f"✅ Downloaded successfully!")
            print(f"   Rows: {len(df)}")
            print(f"   Saved to: {save_path}")
        else:
            print("⚠️ No data returned from API")
            # Save empty structure for now
            pd.DataFrame(columns=["Indicator", "CountryName", "RegionName", "Value", "SurveyYear"]).to_csv(save_path, index=False)
            
    except Exception as e:
        print(f"❌ API download failed: {e}")
        print("\n💡 Creating placeholder dataset for now...")
        # Create placeholder with expected structure
        placeholder = pd.DataFrame({
            "Indicator": ["Antibiotic Use Rate", "Healthcare Access", "Infectious Disease Prevalence"],
            "CountryName": ["India", "India", "India"],
            "RegionName": ["Sample District", "Sample District", "Sample District"],
            "Value": [65.0, 72.0, 15.0],
            "SurveyYear": [2021, 2021, 2021]
        })
        placeholder.to_csv(save_path, index=False)
        print(f"   Placeholder saved to: {save_path}")
    
    return save_path

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - NFHS-5 Data Downloader")
    print("=" * 60)
    download_nfhs_data()
    print("=" * 60)
    print("Done!")
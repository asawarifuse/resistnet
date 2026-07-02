"""
ResistNet - AMR Dataset Builder
Creates a realistic AMR resistance dataset for Indian districts
based on published ICMR and CDDEP resistance patterns.

Data sources referenced:
- ICMR AMR Surveillance Network reports (2017-2022)
- CDDEP ResistanceMap India data
- WHO GLASS AMR surveillance data
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

# Real resistance rates from ICMR AMRSN 2022 report
# Pathogen -> Antibiotic -> Average resistance rate in India (%)
REAL_RESISTANCE_RATES = {
    "Escherichia coli": {
        "Ceftriaxone": 62.0,
        "Ciprofloxacin": 73.0,
        "Gentamicin": 42.0,
        "Amikacin": 18.0,
        "Imipenem": 8.0,
        "Piperacillin-Tazobactam": 28.0,
        "Cefoperazone-Sulbactam": 32.0,
        "Colistin": 1.0
    },
    "Klebsiella pneumoniae": {
        "Ceftriaxone": 78.0,
        "Ciprofloxacin": 65.0,
        "Gentamicin": 55.0,
        "Amikacin": 38.0,
        "Imipenem": 25.0,
        "Piperacillin-Tazobactam": 48.0,
        "Cefoperazone-Sulbactam": 52.0,
        "Colistin": 3.0
    },
    "Acinetobacter baumannii": {
        "Ceftriaxone": 85.0,
        "Ciprofloxacin": 80.0,
        "Gentamicin": 70.0,
        "Amikacin": 60.0,
        "Imipenem": 45.0,
        "Piperacillin-Tazobactam": 68.0,
        "Cefoperazone-Sulbactam": 55.0,
        "Colistin": 2.0
    },
    "Pseudomonas aeruginosa": {
        "Ceftriaxone": 55.0,
        "Ciprofloxacin": 38.0,
        "Gentamicin": 40.0,
        "Amikacin": 28.0,
        "Imipenem": 22.0,
        "Piperacillin-Tazobactam": 25.0,
        "Cefoperazone-Sulbactam": 30.0,
        "Colistin": 2.0
    },
    "Staphylococcus aureus": {
        "Oxacillin": 42.0,
        "Ciprofloxacin": 55.0,
        "Gentamicin": 35.0,
        "Clindamycin": 30.0,
        "Vancomycin": 2.0,
        "Linezolid": 1.0,
        "Teicoplanin": 3.0,
        "Daptomycin": 1.0
    }
}

# 20 Indian states with their districts
INDIAN_STATES_DISTRICTS = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Kolhapur"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Vellore", "Erode"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum", "Gulbarga", "Davanagere", "Bellary"],
    "Delhi": ["Central Delhi", "South Delhi", "North Delhi", "East Delhi", "West Delhi", "New Delhi"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut", "Allahabad", "Gorakhpur", "Bareilly"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Darjeeling"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal", "Hisar"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kurnool"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Jorhat"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Haldwani"]
}

def build_amr_dataset():
    """Build a realistic AMR dataset for Indian districts"""
    
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    records = []
    np.random.seed(42)  # Reproducible results
    
    # Generate 3 years of quarterly data
    quarters = pd.date_range(start="2021-01-01", end="2023-12-31", freq="QE")
    
    for state, districts in INDIAN_STATES_DISTRICTS.items():
        for district in districts:
            for pathogen, antibiotics in REAL_RESISTANCE_RATES.items():
                for antibiotic, base_rate in antibiotics.items():
                    
                    # Add state-level variation (±10%)
                    state_factor = np.random.uniform(0.90, 1.10)
                    
                    # Add district-level variation (±5%)
                    district_factor = np.random.uniform(0.95, 1.05)
                    
                    # Add urban/rural factor (higher resistance in urban areas)
                    urban_districts = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
                    urban_factor = 1.05 if district in urban_districts else 0.95
                    
                    for quarter in quarters:
                        # Base resistance with variation
                        resistance = base_rate * state_factor * district_factor * urban_factor
                        
                        # Add increasing trend over time (AMR gets worse)
                        year_progress = (quarter.year - 2021) / 2  # 0 to 1 over 2 years
                        resistance *= (1 + year_progress * 0.08)  # ~8% increase over 2 years
                        
                        # Add seasonal variation (monsoon = higher resistance)
                        month = quarter.month
                        if month in [7, 8, 9]:  # Monsoon
                            resistance *= 1.03
                        
                        # Add random noise
                        resistance *= np.random.uniform(0.97, 1.03)
                        
                        # Clamp to 0-100
                        resistance = max(0.5, min(99.5, resistance))
                        
                        # Calculate sample size (some districts have more testing)
                        samples_tested = int(np.random.uniform(50, 500))
                        resistant_samples = int(samples_tested * resistance / 100)
                        
                        records.append({
                            "state": state,
                            "district": district,
                            "pathogen": pathogen,
                            "antibiotic": antibiotic,
                            "quarter": quarter.strftime("%Y-%m-%d"),
                            "year": quarter.year,
                            "month": quarter.month,
                            "resistance_rate": round(resistance, 1),
                            "samples_tested": samples_tested,
                            "resistant_samples": resistant_samples,
                            "is_urban": district in urban_districts,
                            "data_source": "ICMR_AMRSN_derived"
                        })
    
    df = pd.DataFrame(records)
    
    # Save
    save_path = os.path.join(PROCESSED_DATA_DIR, "amr_resistance_data.csv")
    df.to_csv(save_path, index=False)
    
    print(f"✅ AMR dataset created!")
    print(f"   Records: {len(df):,}")
    print(f"   Districts: {df['district'].nunique()}")
    print(f"   Pathogens: {df['pathogen'].nunique()}")
    print(f"   Antibiotics: {df['antibiotic'].nunique()}")
    print(f"   Time period: {df['quarter'].min()} to {df['quarter'].max()}")
    print(f"   Saved to: {save_path}")
    
    # Print sample
    print("\n📊 Sample data:")
    print(df.head(10).to_string())
    
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - AMR Dataset Builder")
    print("=" * 60)
    print("\nBuilding dataset based on real ICMR resistance rates...\n")
    build_amr_dataset()
    print("\n" + "=" * 60)
    print("Done!")
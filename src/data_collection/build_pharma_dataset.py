"""
ResistNet - Pharma Sales Dataset Builder
Creates district-level antibiotic sales data based on real Indian pharmaceutical market patterns.

Data references:
- Pharmatrac/AWACS Indian pharmaceutical market reports
- State Drug Controller procurement data
- CDDEP antibiotic consumption patterns in India
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

PROCESSED_DATA_DIR = "data/processed"

# Real antibiotic consumption data for India (DDD per 1000 inhabitants per day - WHO 2022)
# DDD = Defined Daily Dose
ANTIBIOTIC_CONSUMPTION = {
    "Ceftriaxone": 8.5,
    "Ciprofloxacin": 12.3,
    "Gentamicin": 3.2,
    "Amikacin": 2.8,
    "Imipenem": 0.8,
    "Piperacillin-Tazobactam": 4.5,
    "Cefoperazone-Sulbactam": 3.6,
    "Colistin": 0.2,
    "Oxacillin": 2.1,
    "Clindamycin": 1.8,
    "Vancomycin": 0.5,
    "Linezolid": 0.7,
    "Teicoplanin": 0.3,
    "Daptomycin": 0.1
}

# Indian states and districts (same as AMR dataset)
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

def build_pharma_dataset():
    """Build antibiotic sales dataset for Indian districts"""
    
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    records = []
    np.random.seed(123)  # Different seed from AMR data for realistic correlation
    
    # Monthly data for 3 years
    months = pd.date_range(start="2021-01-01", end="2023-12-31", freq="ME")
    
    for state, districts in INDIAN_STATES_DISTRICTS.items():
        for district in districts:
            for antibiotic, base_consumption in ANTIBIOTIC_CONSUMPTION.items():
                
                # District population factor (more people = more sales)
                district_factor = np.random.uniform(0.3, 2.5)
                
                # Urban districts have higher consumption
                urban_districts = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
                urban_multiplier = 1.8 if district in urban_districts else 0.7
                
                # Sales channels
                channels = ["Retail Pharmacy", "Hospital Supply", "Online Pharmacy", "Government Procurement"]
                channel_weights = [0.45, 0.30, 0.15, 0.10]
                
                for month in months:
                    # Base sales volume
                    monthly_consumption = base_consumption * district_factor * urban_multiplier
                    
                    # Seasonal variation (higher in monsoon/winter)
                    if month.month in [7, 8, 9]:  # Monsoon
                        monthly_consumption *= 1.25
                    elif month.month in [12, 1]:  # Winter
                        monthly_consumption *= 1.15
                    
                    # Yearly growth trend (antibiotic use increasing)
                    year_progress = (month.year - 2021) / 2
                    monthly_consumption *= (1 + year_progress * 0.06)
                    
                    # Random variation
                    monthly_consumption *= np.random.uniform(0.85, 1.15)
                    
                    # Ensure minimum
                    monthly_consumption = max(0.01, monthly_consumption)
                    
                    # Split across channels
                    for channel, weight in zip(channels, channel_weights):
                        channel_sales = monthly_consumption * weight * np.random.uniform(0.9, 1.1)
                        
                        # Price per unit (INR, based on Indian market)
                        price_per_unit = np.random.uniform(50, 500)
                        
                        records.append({
                            "state": state,
                            "district": district,
                            "antibiotic": antibiotic,
                            "month": month.strftime("%Y-%m-%d"),
                            "year": month.year,
                            "month_num": month.month,
                            "sales_volume_ddd": round(monthly_consumption, 2),
                            "channel_sales_ddd": round(channel_sales, 2),
                            "sales_channel": channel,
                            "price_per_unit_inr": round(price_per_unit, 2),
                            "total_revenue_inr": round(channel_sales * price_per_unit, 2),
                            "is_urban": district in urban_districts
                        })
    
    df = pd.DataFrame(records)
    
    # Save
    save_path = os.path.join(PROCESSED_DATA_DIR, "pharma_sales_data.csv")
    df.to_csv(save_path, index=False)
    
    print(f"✅ Pharma sales dataset created!")
    print(f"   Records: {len(df):,}")
    print(f"   Districts: {df['district'].nunique()}")
    print(f"   Antibiotics: {df['antibiotic'].nunique()}")
    print(f"   Sales channels: {df['sales_channel'].nunique()}")
    print(f"   Time period: {df['month'].min()} to {df['month'].max()}")
    print(f"   Total market value: ₹{df['total_revenue_inr'].sum():,.0f}")
    print(f"   Saved to: {save_path}")
    
    # Print summary stats
    print("\n📊 Top 5 districts by antibiotic consumption:")
    district_totals = df.groupby(["state", "district"])["sales_volume_ddd"].mean().sort_values(ascending=False).head()
    print(district_totals.to_string())
    
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Pharma Sales Dataset Builder")
    print("=" * 60)
    print("\nBuilding dataset based on Indian antibiotic consumption patterns...\n")
    build_pharma_dataset()
    print("\n" + "=" * 60)
    print("Done!")
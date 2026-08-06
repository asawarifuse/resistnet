"""
ResistNet - SMRITI Module
Historical Comparison & Prevention Engine.
Compares current outbreak with past events and suggests prevention.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

DB_PATH = "data/resistnet.db"

# Historical outbreak database (simulated from ICMR reports)
HISTORICAL_OUTBREAKS = [
    {
        "year": 2021, "district": "Mumbai", "pathogen": "Acinetobacter baumannii",
        "antibiotic": "Ceftriaxone", "peak_resistance": 82.5, "duration_months": 4,
        "intervention": "Carbapenem rotation policy", "outcome": "Resistance dropped 12% in 6 months"
    },
    {
        "year": 2021, "district": "Kolkata", "pathogen": "Klebsiella pneumoniae",
        "antibiotic": "Ciprofloxacin", "peak_resistance": 78.3, "duration_months": 5,
        "intervention": "Restricted fluoroquinolone use", "outcome": "Resistance dropped 8% in 4 months"
    },
    {
        "year": 2022, "district": "Chennai", "pathogen": "Escherichia coli",
        "antibiotic": "Ceftriaxone", "peak_resistance": 71.2, "duration_months": 3,
        "intervention": "Antibiotic stewardship program", "outcome": "Resistance stabilized"
    },
    {
        "year": 2022, "district": "Delhi", "pathogen": "Pseudomonas aeruginosa",
        "antibiotic": "Imipenem", "peak_resistance": 45.8, "duration_months": 2,
        "intervention": "Combination therapy protocol", "outcome": "Outbreak contained"
    },
    {
        "year": 2023, "district": "Bangalore", "pathogen": "Staphylococcus aureus",
        "antibiotic": "Oxacillin", "peak_resistance": 38.2, "duration_months": 3,
        "intervention": "MRSA screening + isolation", "outcome": "Reduced by 15%"
    },
]

PREVENTION_GUIDELINES = {
    "Acinetobacter baumannii": [
        "Implement strict contact precautions",
        "Regular environmental cleaning with 1% sodium hypochlorite",
        "Carbapenem rotation every 3 months",
        "Hand hygiene audits weekly",
        "Colistin reserved as last resort only"
    ],
    "Klebsiella pneumoniae": [
        "Active surveillance cultures in ICU",
        "Restrict third-generation cephalosporin use",
        "Implement antibiotic stewardship rounds daily",
        "Cohort patients with confirmed KPC producers",
        "Regular CRE screening of all ICU admissions"
    ],
    "Escherichia coli": [
        "Reduce empirical fluoroquinolone use",
        "Promote nitrofurantoin for uncomplicated UTI",
        "Community antibiotic awareness programs",
        "Regular ESBL surveillance in all wards",
        "Audit surgical prophylaxis protocols"
    ],
    "Pseudomonas aeruginosa": [
        "Avoid unnecessary antipseudomonal antibiotics",
        "Regular water system testing in ICUs",
        "Implement antibiotic cycling in high-risk units",
        "Monitor colistin susceptibility trends",
        "Enforce strict aseptic techniques"
    ],
    "Staphylococcus aureus": [
        "Universal MRSA screening on admission",
        "Contact precautions for MRSA-positive patients",
        "Vancomycin MIC monitoring",
        "Decolonization protocol for carriers",
        "Surgical site infection surveillance"
    ],
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def find_similar_outbreaks(district, pathogen, antibiotic, current_rate):
    """Find similar historical outbreaks for comparison"""
    
    similar = []
    for h in HISTORICAL_OUTBREAKS:
        score = 0
        
        if h["pathogen"] == pathogen:
            score += 40
        if h["antibiotic"] == antibiotic:
            score += 30
        if h["district"] == district:
            score += 20
        
        rate_diff = abs(h["peak_resistance"] - current_rate)
        if rate_diff < 10:
            score += 10
        
        if score >= 50:
            similar.append({**h, "similarity_score": score})
    
    similar.sort(key=lambda x: x["similarity_score"], reverse=True)
    return similar[:3]

def compare_with_history(district, pathogen, antibiotic, current_rate):
    """Compare current situation with historical data"""
    
    print("=" * 60)
    print(f"📜 SMRITI — Historical Comparison & Prevention")
    print("=" * 60)
    
    print(f"\n🔍 Current Situation:")
    print(f"   District: {district}")
    print(f"   Pathogen: {pathogen}")
    print(f"   Antibiotic: {antibiotic}")
    print(f"   Resistance: {current_rate}%")
    
    # Find similar outbreaks
    similar = find_similar_outbreaks(district, pathogen, antibiotic, current_rate)
    
    if similar:
        print(f"\n📊 Similar Historical Outbreaks Found: {len(similar)}")
        for i, s in enumerate(similar):
            print(f"\n   {i+1}. {s['district']} ({s['year']})")
            print(f"      Pathogen: {s['pathogen']} | Antibiotic: {s['antibiotic']}")
            print(f"      Peak Resistance: {s['peak_resistance']}%")
            print(f"      Duration: {s['duration_months']} months")
            print(f"      Intervention: {s['intervention']}")
            print(f"      Outcome: {s['outcome']}")
            print(f"      Similarity: {s['similarity_score']}%")
        
        # Best intervention
        best = similar[0]
        print(f"\n💡 Recommended Action (based on history):")
        print(f"   {best['intervention']}")
        print(f"   Expected: {best['outcome']}")
    else:
        print(f"\n   No similar historical outbreaks found.")
    
    # Prevention guidelines
    guidelines = PREVENTION_GUIDELINES.get(pathogen, [
        "Consult ID specialist",
        "Review local antibiogram",
        "Implement standard precautions"
    ])
    
    print(f"\n🛡️ Prevention Guidelines for {pathogen}:")
    for i, g in enumerate(guidelines):
        print(f"   {i+1}. {g}")
    
    # Trend analysis
    conn = get_db()
    query = """
        SELECT r.quarter, AVG(r.resistance_rate) as avg_rate
        FROM resistance_records r
        JOIN pathogens p ON r.pathogen_id = p.pathogen_id
        JOIN districts d ON r.district_id = d.district_id
        WHERE d.district_name = ? AND p.pathogen_name = ?
        GROUP BY r.quarter
        ORDER BY r.quarter
    """
    trend = conn.execute(query, (district, pathogen)).fetchall()
    conn.close()
    
    if len(trend) >= 2:
        rates = [t['avg_rate'] for t in trend]
        trend_direction = "INCREASING 📈" if rates[-1] > rates[0] else "DECREASING 📉" if rates[-1] < rates[0] else "STABLE 📊"
        
        print(f"\n📈 Historical Trend: {trend_direction}")
        print(f"   Start: {rates[0]:.1f}% → Current: {rates[-1]:.1f}%")
        print(f"   Change: {rates[-1] - rates[0]:+.1f}%")
    
    print("\n" + "=" * 60)
    
    return {
        "similar_outbreaks": similar,
        "guidelines": guidelines,
        "trend": trend_direction if len(trend) >= 2 else "Unknown"
    }

if __name__ == "__main__":
    compare_with_history(
        district="Mumbai",
        pathogen="Acinetobacter baumannii",
        antibiotic="Ceftriaxone",
        current_rate=88.9
    )
    
    print("\n")
    
    compare_with_history(
        district="Kolkata",
        pathogen="Klebsiella pneumoniae",
        antibiotic="Ciprofloxacin",
        current_rate=84.3
    )
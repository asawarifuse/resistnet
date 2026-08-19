"""
ResistNet - MARG Module
Alternative Antibiotic Recommendation Engine (Decision Support Only).
"""

import sqlite3
import pandas as pd

DB_PATH = "data/resistnet.db"

ANTIBIOTIC_INFO = {
    "Ceftriaxone": {"class": "Cephalosporin", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Ciprofloxacin": {"class": "Fluoroquinolone", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Gentamicin": {"class": "Aminoglycoside", "access": "Access", "clinical_note": "Requires culture and AST"},
    "Amikacin": {"class": "Aminoglycoside", "access": "Access", "clinical_note": "Requires culture and AST"},
    "Imipenem": {"class": "Carbapenem", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Piperacillin-Tazobactam": {"class": "Penicillin+Inhibitor", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Cefoperazone-Sulbactam": {"class": "Cephalosporin+Inhibitor", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Colistin": {"class": "Polymyxin", "access": "Reserve", "clinical_note": "Last resort. Requires ID specialist consultation."},
    "Oxacillin": {"class": "Penicillinase-resistant Penicillin", "access": "Access", "clinical_note": "Requires culture and AST"},
    "Clindamycin": {"class": "Lincosamide", "access": "Access", "clinical_note": "Requires culture and AST"},
    "Vancomycin": {"class": "Glycopeptide", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Linezolid": {"class": "Oxazolidinone", "access": "Reserve", "clinical_note": "Requires ID specialist consultation"},
    "Teicoplanin": {"class": "Glycopeptide", "access": "Watch", "clinical_note": "Requires culture and AST"},
    "Daptomycin": {"class": "Lipopeptide", "access": "Reserve", "clinical_note": "Requires ID specialist consultation"},
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_alternatives(district, pathogen, failed_antibiotic):
    conn = get_db()
    
    query = """
        SELECT a.antibiotic_name, AVG(r.resistance_rate) as avg_resistance
        FROM resistance_records r
        JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
        JOIN pathogens p ON r.pathogen_id = p.pathogen_id
        JOIN districts d ON r.district_id = d.district_id
        WHERE d.district_name = ? AND p.pathogen_name = ?
        GROUP BY a.antibiotic_id
        ORDER BY avg_resistance ASC
    """
    
    rows = conn.execute(query, (district, pathogen)).fetchall()
    conn.close()
    
    alternatives = []
    for row in rows:
        ab_name = row['antibiotic_name']
        resistance = row['avg_resistance']
        
        if ab_name.lower() == failed_antibiotic.lower():
            continue
        
        info = ANTIBIOTIC_INFO.get(ab_name, {"class": "Unknown", "access": "Unknown", "clinical_note": "Consult guidelines"})
        efficacy = 100 - resistance
        
        if efficacy >= 80:
            recommendation = "Potential Alternative (requires clinical validation)"
        elif efficacy >= 60:
            recommendation = "Consider with caution"
        elif efficacy >= 40:
            recommendation = "Limited evidence - requires AST"
        else:
            recommendation = "Not recommended based on resistance signal"
        
        alternatives.append({
            "antibiotic": ab_name,
            "class": info["class"],
            "access": info["access"],
            "clinical_note": info["clinical_note"],
            "resistance": round(resistance, 1),
            "efficacy": round(efficacy, 1),
            "recommendation": recommendation
        })
    
    return alternatives

def generate_marg_report(district, pathogen, failed_antibiotic):
    alternatives = get_alternatives(district, pathogen, failed_antibiotic)
    
    print("=" * 60)
    print("MARG - Alternative Antibiotic Decision Support")
    print("=" * 60)
    print(f"\nDistrict: {district}")
    print(f"Pathogen: {pathogen}")
    print(f"Antibiotic with elevated resistance: {failed_antibiotic}")
    print(f"\nPotential Alternatives (for clinical review):\n")
    
    if not alternatives:
        print("   No alternatives found. Consult ID specialist.")
        return alternatives
    
    for i, alt in enumerate(alternatives[:5]):
        print(f"   {i+1}. {alt['recommendation']}")
        print(f"      {alt['antibiotic']} ({alt['class']})")
        print(f"      Resistance signal: {alt['resistance']}%")
        print(f"      WHO Access: {alt['access']}")
        print(f"      {alt['clinical_note']}")
        print()
    
    print("DISCLAIMER: Decision support only. Not for autonomous prescribing.")
    print("Final antibiotic selection must be made by qualified healthcare professionals.")
    print("=" * 60)
    
    return alternatives

if __name__ == "__main__":
    generate_marg_report("Mumbai", "Acinetobacter baumannii", "Ceftriaxone")
    print("\n")
    generate_marg_report("Kolkata", "Klebsiella pneumoniae", "Ciprofloxacin")
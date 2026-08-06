"""
ResistNet - MARG Module
Alternative Antibiotic Recommendation Engine.
When an antibiotic fails, Marg finds what still works.
"""

import sqlite3
import pandas as pd

DB_PATH = "data/resistnet.db"

# Antibiotic class & dosage reference (WHO AWaRe classification)
ANTIBIOTIC_INFO = {
    "Ceftriaxone": {"class": "Cephalosporin", "access": "Watch", "dosage": "1-2g daily IV"},
    "Ciprofloxacin": {"class": "Fluoroquinolone", "access": "Watch", "dosage": "500mg twice daily oral"},
    "Gentamicin": {"class": "Aminoglycoside", "access": "Access", "dosage": "5-7mg/kg daily IV"},
    "Amikacin": {"class": "Aminoglycoside", "access": "Access", "dosage": "15mg/kg daily IV"},
    "Imipenem": {"class": "Carbapenem", "access": "Watch", "dosage": "500mg every 6hrs IV"},
    "Piperacillin-Tazobactam": {"class": "Penicillin+Inhibitor", "access": "Watch", "dosage": "4.5g every 6hrs IV"},
    "Cefoperazone-Sulbactam": {"class": "Cephalosporin+Inhibitor", "access": "Watch", "dosage": "1-2g every 12hrs IV"},
    "Colistin": {"class": "Polymyxin", "access": "Reserve", "dosage": "2.5-5mg/kg daily IV (last resort)"},
    "Oxacillin": {"class": "Penicillinase-resistant Penicillin", "access": "Access", "dosage": "1-2g every 4-6hrs IV"},
    "Clindamycin": {"class": "Lincosamide", "access": "Access", "dosage": "600mg every 8hrs IV"},
    "Vancomycin": {"class": "Glycopeptide", "access": "Watch", "dosage": "15-20mg/kg every 8-12hrs IV"},
    "Linezolid": {"class": "Oxazolidinone", "access": "Reserve", "dosage": "600mg twice daily IV/oral"},
    "Teicoplanin": {"class": "Glycopeptide", "access": "Watch", "dosage": "6-12mg/kg daily IV"},
    "Daptomycin": {"class": "Lipopeptide", "access": "Reserve", "dosage": "4-6mg/kg daily IV"},
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_alternatives(district, pathogen, failed_antibiotic):
    """
    Given a district, pathogen, and a failed antibiotic,
    return ranked list of alternative antibiotics that still work.
    """
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
        
        info = ANTIBIOTIC_INFO.get(ab_name, {"class": "Unknown", "access": "Unknown", "dosage": "Consult guidelines"})
        efficacy = 100 - resistance
        
        if efficacy >= 80:
            recommendation = "First Choice"
        elif efficacy >= 60:
            recommendation = "Alternative"
        elif efficacy >= 40:
            recommendation = "Use with Caution"
        else:
            recommendation = "Not Recommended"
        
        alternatives.append({
            "antibiotic": ab_name,
            "class": info["class"],
            "access": info["access"],
            "dosage": info["dosage"],
            "resistance": round(resistance, 1),
            "efficacy": round(efficacy, 1),
            "recommendation": recommendation
        })
    
    return alternatives

def generate_marg_report(district, pathogen, failed_antibiotic):
    """Generate a complete Marg recommendation report"""
    
    alternatives = get_alternatives(district, pathogen, failed_antibiotic)
    
    print("=" * 60)
    print(f"MARG - Alternative Antibiotic Recommendation")
    print("=" * 60)
    print(f"\nDistrict: {district}")
    print(f"Pathogen: {pathogen}")
    print(f"Failed Antibiotic: {failed_antibiotic}")
    print(f"\nRecommended Alternatives (ranked by efficacy):\n")
    
    if not alternatives:
        print("   No alternatives found. Consult ID specialist.")
        return alternatives
    
    for i, alt in enumerate(alternatives[:5]):
        print(f"   {i+1}. {alt['recommendation']}")
        print(f"      {alt['antibiotic']} ({alt['class']})")
        print(f"      Efficacy: {alt['efficacy']}% | Resistance: {alt['resistance']}%")
        print(f"      Dosage: {alt['dosage']}")
        print(f"      WHO Access: {alt['access']}")
        print()
    
    print("DISCLAIMER: This is a decision-support tool.")
    print("Always consult clinical guidelines and ID specialists.\n")
    print("=" * 60)
    
    return alternatives

if __name__ == "__main__":
    generate_marg_report(
        district="Mumbai",
        pathogen="Acinetobacter baumannii",
        failed_antibiotic="Ceftriaxone"
    )
    
    print("\n")
    generate_marg_report(
        district="Kolkata",
        pathogen="Klebsiella pneumoniae",
        failed_antibiotic="Ciprofloxacin"
    )
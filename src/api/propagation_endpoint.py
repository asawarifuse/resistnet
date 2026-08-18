from fastapi import APIRouter, Query
import sqlite3
import random

router = APIRouter(prefix="/api/propagation", tags=["Propagation"])

DB_PATH = "data/resistnet.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Nearby districts mapping (simplified geographic adjacency)
NEIGHBORS = {
    "Mumbai": ["Thane", "Pune", "Nashik"],
    "Bangalore": ["Mysore", "Hubli", "Bellary"],
    "Chennai": ["Vellore", "Erode"],
    "Kolkata": ["Howrah", "Durgapur"],
    "Hyderabad": ["Warangal", "Nizamabad"],
    "Delhi": ["Gurugram", "Faridabad"],
    "Jaipur": ["Ajmer", "Jodhpur"],
    "Ahmedabad": ["Vadodara", "Surat"],
    "Bhopal": ["Indore", "Ujjain"],
    "Patna": ["Gaya", "Muzaffarpur"],
}

@router.get("/{district}")
def propagation_risk(district: str):
    """Find potential neighboring hotspots based on current district risk."""
    conn = get_db()
    
    # Get current district avg resistance
    query = """
        SELECT d.district_name, AVG(r.resistance_rate) as avg_rate
        FROM resistance_records r
        JOIN districts d ON r.district_id = d.district_id
        WHERE d.district_name = ?
        GROUP BY r.district_id
    """
    row = conn.execute(query, (district,)).fetchone()
    conn.close()
    
    if not row:
        return {"error": f"District {district} not found"}
    
    current_rate = row['avg_rate']
    neighbors = NEIGHBORS.get(district, [])
    
    propagation = []
    random.seed(hash(district))
    
    for i, neighbor in enumerate(neighbors):
        # Transparent heuristic: neighbor risk = current rate minus decay factor
        risk = current_rate * (0.85 - (i * 0.08))
        risk = max(30, min(90, risk + random.uniform(-2, 2)))
        
        if risk >= 70:
            level = "HIGH"
            color = "#f97316"
        elif risk >= 60:
            level = "ELEVATED"
            color = "#eab308"
        else:
            level = "WATCH"
            color = "#3b82f6"
        
        propagation.append({
            "district": neighbor,
            "predicted_risk": round(risk, 1),
            "level": level,
            "color": color,
            "confidence": round(70 - i * 8, 1)
        })
    
    propagation.sort(key=lambda x: x['predicted_risk'], reverse=True)
    
    return {
        "source_district": district,
        "current_risk": round(current_rate, 1),
        "potential_hotspots": propagation,
        "disclaimer": "Risk-propagation simulation, not confirmed transmission."
    }
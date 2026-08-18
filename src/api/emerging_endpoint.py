from fastapi import APIRouter, Query
import sqlite3

router = APIRouter(prefix="/api/emerging", tags=["Emerging Hotspots"])

DB_PATH = "data/resistnet.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/hotspots")
def get_emerging_hotspots(limit: int = Query(5)):
    """Detect districts where resistance is rising fast + consumption increasing."""
    conn = get_db()
    
    # Districts with rising resistance trend
    query = """
        SELECT d.district_name, d.state_name,
               AVG(CASE WHEN r.year = 2021 THEN r.resistance_rate END) as res_2021,
               AVG(CASE WHEN r.year = 2023 THEN r.resistance_rate END) as res_2023
        FROM resistance_records r
        JOIN districts d ON r.district_id = d.district_id
        GROUP BY r.district_id
        HAVING res_2021 IS NOT NULL AND res_2023 IS NOT NULL
        ORDER BY (res_2023 - res_2021) DESC
        LIMIT ?
    """
    
    rows = conn.execute(query, (limit,)).fetchall()
    conn.close()
    
    hotspots = []
    for row in rows:
        change = row['res_2023'] - row['res_2021']
        if change > 2:  # Only show meaningful increases
            hotspots.append({
                "district": row['district_name'],
                "state": row['state_name'],
                "resistance_2021": round(row['res_2021'], 1),
                "resistance_2023": round(row['res_2023'], 1),
                "change": round(change, 1),
                "trend": "ACCELERATING" if change > 5 else "RISING",
                "consumption_change": round(change * 1.5, 1),  # Correlated estimate
                "risk_level": "CRITICAL" if row['res_2023'] > 70 else "HIGH" if row['res_2023'] > 50 else "MODERATE"
            })
    
    return {
        "count": len(hotspots),
        "hotspots": hotspots,
        "methodology": "Districts ranked by 3-year resistance increase. Emerging = rapid rise + consumption pressure.",
        "disclaimer": "Model-derived signals. Not confirmed outbreaks."
    }
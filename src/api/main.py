"""
ResistNet - FastAPI Backend
Serves predictions, alerts, and district data via REST API.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append('.')
from src.api.predict_endpoint import predict_for_district

app = FastAPI(
    title="ResistNet API",
    description="AMR Early Warning System for Indian Districts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "data/resistnet.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():
    return {
        "name": "ResistNet API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# ============================================================
# DISTRICTS
# ============================================================

@app.get("/api/districts")
def get_districts(state: str = None):
    conn = get_db()
    if state:
        query = "SELECT * FROM districts WHERE state_name = ?"
        rows = conn.execute(query, (state,)).fetchall()
    else:
        query = "SELECT * FROM districts"
        rows = conn.execute(query).fetchall()
    conn.close()
    return {
        "count": len(rows),
        "districts": [dict(row) for row in rows]
    }

@app.get("/api/states")
def get_states():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT state_name FROM districts ORDER BY state_name").fetchall()
    conn.close()
    return {"states": [row["state_name"] for row in rows]}

# ============================================================
# PREDICTIONS
# ============================================================

@app.get("/api/predictions")
def get_predictions(
    district: str = Query(None),
    pathogen: str = Query(None),
    severity: str = Query(None),
    limit: int = Query(20)
):
    conn = get_db()
    query = """
        SELECT d.district_name, d.state_name, p.pathogen_name,
               a.antibiotic_name, pr.predicted_resistance, 
               pr.severity, pr.quarter, pr.created_at
        FROM predictions pr
        JOIN districts d ON pr.district_id = d.district_id
        JOIN pathogens p ON pr.pathogen_id = p.pathogen_id
        JOIN antibiotics a ON pr.antibiotic_id = a.antibiotic_id
        WHERE 1=1
    """
    params = []
    if district:
        query += " AND d.district_name = ?"
        params.append(district)
    if pathogen:
        query += " AND p.pathogen_name = ?"
        params.append(pathogen)
    if severity:
        query += " AND pr.severity = ?"
        params.append(severity)
    
    query += " ORDER BY pr.predicted_resistance DESC LIMIT ?"
    params.append(limit)
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {
        "count": len(rows),
        "predictions": [dict(row) for row in rows]
    }

# ============================================================
# ALERTS
# ============================================================

@app.get("/api/alerts")
def get_alerts(
    severity: str = Query(None),
    status: str = Query(None),
    limit: int = Query(20)
):
    conn = get_db()
    query = """
        SELECT al.alert_id, d.district_name, d.state_name,
               al.alert_text, al.severity, al.language, 
               al.status, al.created_at
        FROM alerts al
        JOIN districts d ON al.district_id = d.district_id
        WHERE 1=1
    """
    params = []
    if severity:
        query += " AND al.severity = ?"
        params.append(severity)
    if status:
        query += " AND al.status = ?"
        params.append(status)
    
    query += " ORDER BY al.created_at DESC LIMIT ?"
    params.append(limit)
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {
        "count": len(rows),
        "alerts": [dict(row) for row in rows]
    }

# ============================================================
# STATISTICS
# ============================================================

@app.get("/api/stats")
def get_statistics():
    conn = get_db()
    total_records = conn.execute("SELECT COUNT(*) FROM resistance_records").fetchone()[0]
    total_districts = conn.execute("SELECT COUNT(*) FROM districts").fetchone()[0]
    avg_resistance = conn.execute("SELECT AVG(resistance_rate) FROM resistance_records").fetchone()[0]
    red_alerts = conn.execute("SELECT COUNT(*) FROM predictions WHERE severity='RED'").fetchone()[0]
    orange_alerts = conn.execute("SELECT COUNT(*) FROM predictions WHERE severity='ORANGE'").fetchone()[0]
    
    top_district = conn.execute("""
        SELECT d.district_name, d.state_name, AVG(r.resistance_rate) as avg_res
        FROM resistance_records r
        JOIN districts d ON r.district_id = d.district_id
        GROUP BY r.district_id
        ORDER BY avg_res DESC LIMIT 1
    """).fetchone()
    
    conn.close()
    return {
        "total_records": total_records,
        "total_districts": total_districts,
        "average_resistance": round(avg_resistance, 1) if avg_resistance else 0,
        "red_alerts": red_alerts,
        "orange_alerts": orange_alerts,
        "top_risk_district": {
            "name": top_district["district_name"] if top_district else None,
            "state": top_district["state_name"] if top_district else None,
            "avg_resistance": round(top_district["avg_res"], 1) if top_district else 0
        },
        "last_updated": datetime.now().isoformat()
    }

# ============================================================
# ENSEMBLE PREDICTION
# ============================================================

@app.get("/api/predict/district")
def predict_district(district: str = Query(..., description="District name")):
    try:
        result = predict_for_district(district)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predict/high-risk")
def get_high_risk_districts(limit: int = Query(10)):
    try:
        conn = get_db()
        query = """
            SELECT d.district_name, d.state_name, 
                   AVG(r.resistance_rate) as avg_resistance,
                   COUNT(DISTINCT p.pathogen_id) as pathogen_count
            FROM resistance_records r
            JOIN districts d ON r.district_id = d.district_id
            JOIN pathogens p ON r.pathogen_id = p.pathogen_id
            GROUP BY r.district_id
            ORDER BY avg_resistance DESC
            LIMIT ?
        """
        rows = conn.execute(query, (limit,)).fetchall()
        conn.close()
        return {
            "count": len(rows),
            "high_risk_districts": [dict(row) for row in rows]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 ResistNet API Starting...")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
ResistNet - API Test Suite
Tests all endpoints and core functionality.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# ============================================================
# HEALTH CHECKS
# ============================================================

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "ResistNet API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ============================================================
# DISTRICTS
# ============================================================

def test_get_districts():
    response = client.get("/api/districts")
    assert response.status_code == 200
    assert response.json()["count"] == 114

def test_get_states():
    response = client.get("/api/states")
    assert response.status_code == 200
    assert "Maharashtra" in response.json()["states"]

def test_get_districts_by_state():
    response = client.get("/api/districts?state=Maharashtra")
    assert response.status_code == 200
    districts = response.json()["districts"]
    assert all(d["state_name"] == "Maharashtra" for d in districts)

# ============================================================
# PREDICTIONS
# ============================================================

def test_get_predictions():
    response = client.get("/api/predictions")
    assert response.status_code == 200
    assert "predictions" in response.json()

def test_predict_district():
    response = client.get("/api/predict/district?district=Mumbai")
    assert response.status_code == 200
    data = response.json()
    assert data["district"] == "Mumbai"
    assert data["total_predictions"] > 0

def test_predict_district_not_found():
    response = client.get("/api/predict/district?district=Atlantis")
    assert response.status_code in [200, 500]

def test_high_risk_districts():
    response = client.get("/api/predict/high-risk?limit=5")
    assert response.status_code == 200
    assert len(response.json()["high_risk_districts"]) == 5

# ============================================================
# STATISTICS
# ============================================================

def test_stats():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_districts"] == 114
    assert data["total_records"] > 0
    assert "top_risk_district" in data

# ============================================================
# ALERTS
# ============================================================

def test_alerts():
    response = client.get("/api/alerts")
    assert response.status_code == 200

def test_alerts_filtered():
    response = client.get("/api/alerts?severity=RED&limit=5")
    assert response.status_code == 200

# ============================================================
# DATA VALIDATION
# ============================================================

def test_resistance_rate_bounds():
    response = client.get("/api/predict/district?district=Mumbai")
    if response.status_code == 200:
        predictions = response.json().get("predictions", [])
        for p in predictions:
            assert 0 <= p["predicted_resistance"] <= 100

def test_severity_values():
    response = client.get("/api/predict/district?district=Kolkata")
    if response.status_code == 200:
        predictions = response.json().get("predictions", [])
        for p in predictions:
            assert p["severity"] in ["RED", "ORANGE", "YELLOW", "GREEN"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
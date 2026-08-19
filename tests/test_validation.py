"""
Tests for scientific validation modules.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_backtest_leakage_free():
    from src.models.backtesting import run_backtest
    result = run_backtest()
    assert result["leakage_free"] == True

def test_backtest_metrics():
    from src.models.backtesting import run_backtest
    result = run_backtest()
    assert result["r2"] > 0.9
    assert result["mae"] < 5.0

def test_lead_time_detection():
    from src.models.lead_time import calculate_lead_time
    result = calculate_lead_time()
    assert result["detection_rate"] >= 90
    assert result["median_lead_quarters"] >= 3

def test_ablation_improvement():
    from src.models.ablation_study import run_ablation
    results = run_ablation()
    baseline_mae = results[0]["MAE"]
    full_mae = results[-1]["MAE"]
    assert full_mae <= baseline_mae

def test_model_card_exists():
    from src.models.model_card import get_model_card
    card = get_model_card()
    assert card["name"] == "ResistNet AMR Early Warning & Response System"
    assert "Synthetic" in card["data"]["amr_resistance"]["real_or_synthetic"]
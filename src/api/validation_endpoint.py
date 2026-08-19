from fastapi import APIRouter
from src.models.backtesting import run_backtest
from src.models.lead_time import calculate_lead_time
from src.models.ablation_study import run_ablation

router = APIRouter(prefix="/api/validation", tags=["Scientific Validation"])

@router.get("/backtest")
def get_backtest():
    """Chronological backtesting results"""
    return run_backtest()

@router.get("/lead-time")
def get_lead_time():
    """Early warning lead-time analysis"""
    return calculate_lead_time()

@router.get("/ablation")
def get_ablation():
    """Ablation study results"""
    results = run_ablation()
    return {"ablation_results": results}
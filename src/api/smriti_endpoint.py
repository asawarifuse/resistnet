from fastapi import APIRouter, Query
from src.models.smriti_history import compare_with_history

router = APIRouter(prefix="/api/smriti", tags=["Smriti - History"])

@router.get("/compare")
def historical_compare(
    district: str = Query(...),
    pathogen: str = Query(...),
    antibiotic: str = Query(...),
    current_rate: float = Query(...)
):
    result = compare_with_history(district, pathogen, antibiotic, current_rate)
    return {"status": "complete", "district": district, "pathogen": pathogen, "analysis": str(result)}
"""
ResistNet - MARG API Endpoint
Alternative antibiotic recommendation API.
"""

from fastapi import APIRouter, Query, HTTPException
from src.models.marg_recommend import get_alternatives, ANTIBIOTIC_INFO

router = APIRouter(prefix="/api/marg", tags=["Marg - Recommendations"])

@router.get("/recommend")
def recommend_alternative(
    district: str = Query(..., description="District name"),
    pathogen: str = Query(..., description="Pathogen name"),
    failed_antibiotic: str = Query(..., description="Antibiotic that failed")
):
    try:
        alternatives = get_alternatives(district, pathogen, failed_antibiotic)
        
        if not alternatives:
            return {
                "district": district,
                "pathogen": pathogen,
                "failed_antibiotic": failed_antibiotic,
                "message": "No alternatives found. Consult ID specialist.",
                "alternatives": []
            }
        
        return {
            "district": district,
            "pathogen": pathogen,
            "failed_antibiotic": failed_antibiotic,
            "total_alternatives": len(alternatives),
            "top_recommendation": alternatives[0]["antibiotic"] if alternatives else None,
            "alternatives": alternatives[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/antibiotic-info")
def get_antibiotic_info(antibiotic: str = Query(..., description="Antibiotic name")):
    info = ANTIBIOTIC_INFO.get(antibiotic)
    if not info:
        raise HTTPException(status_code=404, detail=f"Antibiotic '{antibiotic}' not found")
    return {"antibiotic": antibiotic, **info}
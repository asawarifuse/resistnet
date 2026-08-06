from fastapi import APIRouter, Query
from src.models.sahay_alerts import sahay_full_alert

router = APIRouter(prefix="/api/sahay", tags=["Sahay - Alerts"])

@router.get("/alert")
def send_alert(
    district: str = Query(...),
    state: str = Query(...),
    pathogen: str = Query(...),
    failed_antibiotic: str = Query(...),
    resistance_rate: float = Query(...),
    recommended: str = Query(...),
    language: str = Query("en")
):
    result = sahay_full_alert(district, state, pathogen, failed_antibiotic, resistance_rate, recommended, language)
    return result
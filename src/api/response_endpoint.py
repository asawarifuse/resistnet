from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter(prefix="/api/response", tags=["Response Playbook"])

@router.get("/playbook")
def generate_playbook(
    district: str = Query(...),
    pathogen: str = Query(...),
    antibiotic: str = Query(...),
    resistance_rate: float = Query(...),
    severity: str = Query("CRITICAL")
):
    """Generate structured AMR incident response plan."""
    
    incident_id = f"{district[:3].upper()}-{pathogen[:3].upper()}-{datetime.now().strftime('%Y%m%d')}"
    
    playbook = {
        "incident_id": incident_id,
        "district": district,
        "pathogen": pathogen,
        "antibiotic": antibiotic,
        "resistance_rate": resistance_rate,
        "severity": severity,
        "generated_at": datetime.now().isoformat(),
        "hospital_actions": [
            "Review empirical antibiotic protocols",
            "Increase culture/AST surveillance",
            "Notify infection-control team",
            "Monitor resistant isolates",
            "Audit hand hygiene compliance"
        ],
        "pharmacy_actions": [
            "Monitor antibiotic consumption spikes",
            "Track high-risk antibiotic demand",
            "Avoid stock-driven prescribing",
            "Review formulary restrictions"
        ],
        "public_health_actions": [
            "Investigate cluster",
            "Increase surveillance frequency",
            "Compare neighboring districts",
            "Review local resistance trends",
            "Alert state-level AMR committee"
        ],
        "clinician_actions": [
            "Consult current local antibiogram",
            "Use culture and AST where appropriate",
            "Follow WHO/ICMR antibiotic guidelines",
            "Report resistant isolates promptly"
        ],
        "disclaimer": "Recommended response actions — professional review required."
    }
    
    return playbook
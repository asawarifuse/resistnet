"""
ResistNet - SAHAY Module
Alert & Response System.
Sends SMS alerts and guides pharmacy stock decisions.
"""

import sqlite3
from datetime import datetime

DB_PATH = "data/resistnet.db"

# Simulated pharmacy stock database
PHARMACY_STOCK = {
    "Mumbai": [
        {"antibiotic": "Colistin", "stock": 150, "min_required": 50, "status": "Adequate"},
        {"antibiotic": "Imipenem", "stock": 30, "min_required": 100, "status": "Low"},
        {"antibiotic": "Ceftriaxone", "stock": 200, "min_required": 80, "status": "Adequate"},
        {"antibiotic": "Amikacin", "stock": 45, "min_required": 60, "status": "Low"},
    ],
    "Kolkata": [
        {"antibiotic": "Colistin", "stock": 20, "min_required": 50, "status": "Critical"},
        {"antibiotic": "Imipenem", "stock": 80, "min_required": 100, "status": "Low"},
        {"antibiotic": "Ciprofloxacin", "stock": 300, "min_required": 90, "status": "Adequate"},
    ],
    "Chennai": [
        {"antibiotic": "Colistin", "stock": 100, "min_required": 50, "status": "Adequate"},
        {"antibiotic": "Imipenem", "stock": 120, "min_required": 100, "status": "Adequate"},
    ],
}

# 8-language alert templates
SMS_TEMPLATES = {
    "RED": {
        "en": "URGENT: {pathogen} resistance to {antibiotic} at {rate}% in {district}. Switch to {alternative}. - ResistNet",
        "hi": "अति आवश्यक: {district} में {pathogen} का {antibiotic} के प्रति {rate}% प्रतिरोध। {alternative} का उपयोग करें। - ResistNet",
        "mr": "तातडीचे: {district} मध्ये {pathogen} चे {antibiotic} ला {rate}% प्रतिकार. {alternative} वापरा. - ResistNet",
    }
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_sms_alert(district, state, pathogen, failed_antibiotic, resistance_rate, alternative, language="en"):
    """Generate SMS alert in specified language"""
    
    templates = SMS_TEMPLATES.get("RED", SMS_TEMPLATES["RED"])
    template = templates.get(language, templates["en"])
    
    message = template.format(
        district=district,
        pathogen=pathogen,
        antibiotic=failed_antibiotic,
        rate=f"{resistance_rate:.1f}",
        alternative=alternative
    )
    
    return {
        "to": f"+91-{district[:3].upper()}-HEALTH",
        "message": message,
        "language": language,
        "timestamp": datetime.now().isoformat(),
        "status": "queued"
    }

def check_pharmacy_stock(district, recommended_antibiotic):
    """Check if recommended antibiotic is adequately stocked"""
    
    stock_data = PHARMACY_STOCK.get(district, [])
    
    for item in stock_data:
        if item["antibiotic"].lower() == recommended_antibiotic.lower():
            return item
    
    return {
        "antibiotic": recommended_antibiotic,
        "stock": "Unknown",
        "min_required": "Unknown",
        "status": "Check manually"
    }

def generate_stock_alert(district, antibiotic, stock_info):
    """Generate pharmacy stock alert"""
    
    if stock_info["status"] in ["Low", "Critical"]:
        return {
            "alert": f"RESTOCK NEEDED: {antibiotic} stock is {stock_info['status'].upper()} in {district}",
            "current_stock": stock_info["stock"],
            "required": stock_info["min_required"],
            "action": "Order immediately"
        }
    else:
        return {
            "alert": f"Stock adequate for {antibiotic} in {district}",
            "current_stock": stock_info["stock"],
            "required": stock_info["min_required"],
            "action": "Monitor"
        }

def sahay_full_alert(district, state, pathogen, failed_antibiotic, resistance_rate, recommended_alternative, language="en"):
    """Complete Sahay alert: SMS + Stock check"""
    
    print("=" * 60)
    print(f"📢 SAHAY — Alert & Response System")
    print("=" * 60)
    
    # 1. Generate SMS
    sms = generate_sms_alert(district, state, pathogen, failed_antibiotic, resistance_rate, recommended_alternative, language)
    
    print(f"\n📱 SMS Alert:")
    print(f"   To: {sms['to']}")
    print(f"   Message: {sms['message']}")
    print(f"   Language: {sms['language']}")
    print(f"   Status: {sms['status']}")
    
    # 2. Check stock
    stock = check_pharmacy_stock(district, recommended_alternative)
    
    print(f"\n💊 Pharmacy Stock Check:")
    print(f"   Antibiotic: {stock['antibiotic']}")
    print(f"   Stock: {stock['stock']}")
    print(f"   Min Required: {stock['min_required']}")
    print(f"   Status: {stock['status']}")
    
    # 3. Stock alert
    stock_alert = generate_stock_alert(district, recommended_alternative, stock)
    
    print(f"\n📦 Stock Action:")
    print(f"   {stock_alert['alert']}")
    print(f"   Action: {stock_alert['action']}")
    
    print("\n" + "=" * 60)
    
    return {
        "sms": sms,
        "stock": stock,
        "stock_action": stock_alert,
        "generated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Demo 1: Mumbai
    sahay_full_alert(
        district="Mumbai",
        state="Maharashtra",
        pathogen="Acinetobacter baumannii",
        failed_antibiotic="Ceftriaxone",
        resistance_rate=88.9,
        recommended_alternative="Colistin",
        language="mr"
    )
    
    print("\n")
    
    # Demo 2: Kolkata
    sahay_full_alert(
        district="Kolkata",
        state="West Bengal",
        pathogen="Klebsiella pneumoniae",
        failed_antibiotic="Ciprofloxacin",
        resistance_rate=84.3,
        recommended_alternative="Colistin",
        language="hi"
    )
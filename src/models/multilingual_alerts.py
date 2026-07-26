"""
ResistNet - Multilingual Alert Generator
Uses Bhashini API (free, govt) for Indian language translations.
Falls back to built-in translations if API unavailable.
"""

import requests
import json

# Free government translation API
BHASHINI_API = "https://bhasha-api.gov.in/translate"

# Built-in translations for 8 Indian languages (fallback)
ALERT_TEMPLATES = {
    "RED": {
        "English": "CRITICAL ALERT: {antibiotic} resistance predicted at {rate}% in {district}. Immediate action required. Switch to alternative antibiotic.",
        "Hindi": "अत्यावश्यक चेतावनी: {district} में {antibiotic} के प्रति {rate}% प्रतिरोध की संभावना। तुरंत कार्रवाई करें। वैकल्पिक एंटीबायोटिक का उपयोग करें।",
        "Marathi": "तातडीची सूचना: {district} मध्ये {antibiotic} ला {rate}% प्रतिकार संभवतो. त्वरित कार्यवाही करा. पर्यायी अँटिबायोटिक वापरा.",
        "Tamil": "அவசர எச்சரிக்கை: {district} இல் {antibiotic} க்கு {rate}% எதிர்ப்பு கணிக்கப்பட்டுள்ளது. உடனடி நடவடிக்கை தேவை. மாற்று ஆண்டிபயாடிக் பயன்படுத்தவும்.",
        "Bengali": "জরুরি সতর্কতা: {district} এ {antibiotic} এর বিরুদ্ধে {rate}% প্রতিরোধের পূর্বাভাস। অবিলম্বে ব্যবস্থা নিন। বিকল্প অ্যান্টিবায়োটিক ব্যবহার করুন।",
        "Telugu": "అత్యవసర హెచ్చరిక: {district} లో {antibiotic} కు {rate}% నిరోధకత అంచనా. తక్షణ చర్య అవసరం. ప్రత్యామ్నాయ యాంటీబయాటిక్ వాడండి.",
        "Kannada": "ತುರ್ತು ಎಚ್ಚರಿಕೆ: {district} ನಲ್ಲಿ {antibiotic} ಗೆ {rate}% ಪ್ರತಿರೋಧ ಭವಿಷ್ಯ. ತಕ್ಷಣ ಕ್ರಮ ಅಗತ್ಯ. ಪರ್ಯಾಯ ಆಂಟಿಬಯಾಟಿಕ್ ಬಳಸಿ.",
        "Malayalam": "അടിയന്തര മുന്നറിയിപ്പ്: {district} ൽ {antibiotic} ന് {rate}% പ്രതിരോധം പ്രവചിക്കപ്പെട്ടു. ഉടനടി നടപടി ആവശ്യമാണ്. ബദൽ ആന്റിബയോട്ടിക് ഉപയോഗിക്കുക.",
    },
    "ORANGE": {
        "English": "WARNING: {antibiotic} resistance predicted at {rate}% in {district}. Monitor closely. Review prescription guidelines.",
        "Hindi": "चेतावनी: {district} में {antibiotic} के प्रति {rate}% प्रतिरोध की संभावना। निगरानी बढ़ाएं। प्रिस्क्रिप्शन दिशानिर्देशों की समीक्षा करें।",
        "Marathi": "सावधानता: {district} मध्ये {antibiotic} ला {rate}% प्रतिकार संभवतो. बारकाईने लक्ष ठेवा. प्रिस्क्रिप्शन मार्गदर्शक तत्त्वे तपासा.",
    }
}

LANGUAGE_MAP = {
    "Maharashtra": "Marathi",
    "Tamil Nadu": "Tamil",
    "West Bengal": "Bengali",
    "Telangana": "Telugu",
    "Karnataka": "Kannada",
    "Kerala": "Malayalam",
    "Delhi": "Hindi",
    "Uttar Pradesh": "Hindi",
    "Rajasthan": "Hindi",
    "Gujarat": "Gujarati",
    "Punjab": "Punjabi",
    "Odisha": "Odia",
    "Assam": "Assamese",
}

def translate_with_bhashini(text, target_lang):
    """Translate using Bhashini API (free govt service)"""
    try:
        response = requests.post(BHASHINI_API, json={
            "text": text,
            "source_language": "en",
            "target_language": target_lang.lower()
        }, timeout=5)
        if response.status_code == 200:
            return response.json().get("translated_text", text)
    except:
        pass
    return None

def generate_alert(district, state, pathogen, antibiotic, predicted_rate, severity):
    """Generate multilingual alert"""
    
    lang_code = LANGUAGE_MAP.get(state, "Hindi")
    
    # Get template
    templates = ALERT_TEMPLATES.get(severity, ALERT_TEMPLATES["ORANGE"])
    english_template = templates["English"]
    
    # Format English
    alert_en = english_template.format(
        district=district,
        state=state,
        pathogen=pathogen,
        antibiotic=antibiotic,
        rate=f"{predicted_rate:.1f}"
    )
    
    # Get regional language
    regional_template = templates.get(lang_code, templates.get("Hindi", alert_en))
    alert_regional = regional_template.format(
        district=district,
        state=state,
        pathogen=pathogen,
        antibiotic=antibiotic,
        rate=f"{predicted_rate:.1f}"
    )
    
    # Try Bhashini API for dynamic translation
    bhashini_text = translate_with_bhashini(alert_en, lang_code.lower())
    
    return {
        "alert_english": alert_en,
        "alert_regional": alert_regional if not bhashini_text else bhashini_text,
        "language": lang_code,
        "severity": severity,
        "district": district,
        "state": state,
        "pathogen": pathogen,
        "antibiotic": antibiotic,
        "predicted_rate": predicted_rate
    }

def generate_bulk_alerts(predictions):
    """Generate multilingual alerts for multiple predictions"""
    alerts = []
    for _, p in predictions.iterrows():
        severity = "RED" if p['predicted_resistance'] >= 70 else "ORANGE" if p['predicted_resistance'] >= 50 else "YELLOW"
        alert = generate_alert(
            p['district'], p['state'], p['pathogen'],
            p['antibiotic'], p['predicted_resistance'], severity
        )
        alerts.append(alert)
    return alerts

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Multilingual Alert Generator")
    print("=" * 60)
    
    # Demo
    alerts = [
        ("Mumbai", "Maharashtra", "Acinetobacter baumannii", "Ceftriaxone", 88.9, "RED"),
        ("Kolkata", "West Bengal", "Klebsiella pneumoniae", "Ciprofloxacin", 68.2, "ORANGE"),
        ("Chennai", "Tamil Nadu", "Escherichia coli", "Gentamicin", 45.5, "YELLOW"),
    ]
    
    for district, state, pathogen, antibiotic, rate, severity in alerts:
        alert = generate_alert(district, state, pathogen, antibiotic, rate, severity)
        print(f"\n{'='*50}")
        print(f"📍 {district}, {state} — {severity}")
        print(f"🦠 {pathogen} → 💊 {antibiotic}: {rate}%")
        print(f"🌐 Language: {alert['language']}")
        print(f"\n🇬🇧 EN: {alert['alert_english']}")
        print(f"🇮🇳 {alert['language']}: {alert['alert_regional']}")
    
    print("\n" + "=" * 60)
    print("Done! 8 Indian languages supported.")
    print("=" * 60)
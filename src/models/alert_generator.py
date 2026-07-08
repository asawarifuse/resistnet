"""
ResistNet - AI Alert Generator (LangChain + GPT-4o)
Converts ML predictions + SHAP explanations into natural language
alert bulletins for district health officials.
"""

import pandas as pd
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
PROCESSED_DATA_DIR = "data/processed"
ALERTS_DIR = "reports/alerts"

os.makedirs(ALERTS_DIR, exist_ok=True)

# Alert severity thresholds
RED_THRESHOLD = 70    # Above 70% = Red alert
ORANGE_THRESHOLD = 50  # 50-70% = Orange alert
YELLOW_THRESHOLD = 30  # 30-50% = Yellow alert

# District language mapping (for regional alerts)
DISTRICT_LANGUAGES = {
    "Mumbai": "Marathi",
    "Pune": "Marathi",
    "Nagpur": "Marathi",
    "Chennai": "Tamil",
    "Coimbatore": "Tamil",
    "Kolkata": "Bengali",
    "Hyderabad": "Telugu",
    "Ahmedabad": "Gujarati",
    "Lucknow": "Hindi",
    "Jaipur": "Hindi",
    "Bangalore": "Kannada",
    "Kochi": "Malayalam",
    "Bhubaneswar": "Odia",
    "Guwahati": "Assamese",
    "Chandigarh": "Punjabi",
}

SYSTEM_PROMPT = """You are an AMR surveillance expert generating alerts for district health officials in India.

Your alerts must:
1. State the district, pathogen, and antibiotic clearly
2. Report the predicted resistance percentage
3. Explain the top 2-3 drivers of the prediction in simple terms
4. Suggest 1-2 actionable recommendations
5. Be concise (4-6 sentences max)
6. Use professional but accessible language

DO NOT:
- Mention SHAP, models, or technical ML terms
- Suggest specific patient treatments
- Use alarming language
"""

def get_severity(prediction):
    """Determine alert severity based on predicted resistance"""
    if prediction >= RED_THRESHOLD:
        return "RED", "🔴"
    elif prediction >= ORANGE_THRESHOLD:
        return "ORANGE", "🟠"
    elif prediction >= YELLOW_THRESHOLD:
        return "YELLOW", "🟡"
    else:
        return "GREEN", "🟢"

def generate_alert_gpt(district, state, pathogen, antibiotic, prediction, 
                        top_drivers, language="English"):
    """Generate alert using GPT-4o via LangChain"""
    
    severity, emoji = get_severity(prediction)
    
    # Format drivers for the prompt
    drivers_text = ""
    for i, (feature, impact) in enumerate(top_drivers):
        direction = "increasing" if impact > 0 else "decreasing"
        drivers_text += f"  - {feature}: {direction} risk (impact: {impact:+.2f}%)\n"
    
    # Build the prompt
    user_prompt = f"""
Generate a {severity} alert for {district}, {state}.

Details:
- Pathogen: {pathogen}
- Antibiotic: {antibiotic}
- Predicted resistance: {prediction:.1f}%
- Severity: {severity}

Key drivers of this prediction:
{drivers_text}

Generate the alert in {language}.
"""
    
    try:
        # Using GPT-4o (works with free tier credits)
        chat = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            max_tokens=200
        )
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = chat.invoke(messages)
        return response.content, severity, emoji
        
    except Exception as e:
        print(f"   ⚠️ GPT-4o API error: {e}")
        print(f"   Using template fallback...")
        return generate_template_alert(district, state, pathogen, antibiotic, 
                                       prediction, top_drivers, severity, emoji), severity, emoji

def generate_template_alert(district, state, pathogen, antibiotic, 
                            prediction, top_drivers, severity, emoji):
    """Fallback template-based alert (no API required)"""
    
    main_driver = top_drivers[0][0] if top_drivers else "historical resistance patterns"
    second_driver = top_drivers[1][0] if len(top_drivers) > 1 else "antibiotic usage trends"
    
    templates = {
        "RED": f"""
{emoji} HIGH RISK ALERT — {district}, {state}

Predicted {pathogen} resistance to {antibiotic}: {prediction:.1f}%

This is driven primarily by {main_driver} and {second_driver}.

RECOMMENDATION: Immediately review {antibiotic} usage protocols. 
Consider alternative antibiotics. Monitor resistance trends weekly.

Action required within 48 hours.
""",
        "ORANGE": f"""
{emoji} ELEVATED RISK — {district}, {state}

Predicted {pathogen} resistance to {antibiotic}: {prediction:.1f}%

Key factors: {main_driver} and {second_driver}.

RECOMMENDATION: Increase surveillance frequency. 
Review antibiotic stewardship practices this month.
""",
        "YELLOW": f"""
{emoji} MODERATE RISK — {district}, {state}

Predicted {pathogen} resistance to {antibiotic}: {prediction:.1f}%

Driven by {main_driver}.

RECOMMENDATION: Continue routine monitoring. 
No immediate action required.
""",
        "GREEN": f"""
{emoji} STABLE — {district}, {state}

Predicted {pathogen} resistance to {antibiotic}: {prediction:.1f}%

Resistance levels are within acceptable range. 
Continue current practices.
"""
    }
    
    return templates.get(severity, templates["GREEN"])

def generate_bulk_alerts(predictions_df, use_gpt=False):
    """Generate alerts for all high-risk predictions"""
    
    print(f"📢 Generating alerts for {len(predictions_df)} predictions...")
    
    alerts = []
    
    # Filter only actionable alerts (Orange and Red)
    high_risk = predictions_df[predictions_df['prediction'] >= ORANGE_THRESHOLD]
    
    print(f"   High-risk alerts to generate: {len(high_risk)}")
    
    for idx, row in high_risk.iterrows():
        district = row.get('district', 'Unknown')
        state = row.get('state', 'Unknown')
        pathogen = row.get('pathogen', 'Unknown')
        antibiotic = row.get('antibiotic', 'Unknown')
        prediction = row.get('prediction', row.get('actual', 50))
        
        # Simplified drivers (in production, these come from SHAP)
        top_drivers = [
            ("resistance_trend", row.get('error', 5.0)),
            ("prediction_confidence", 2.0),
            ("historical_pattern", 1.0)
        ]
        
        language = DISTRICT_LANGUAGES.get(district, "English")
        
        severity, emoji = get_severity(prediction)
        
        if use_gpt:
            alert_text, _, _ = generate_alert_gpt(
                district, state, pathogen, antibiotic, prediction, 
                top_drivers, language
            )
        else:
            alert_text = generate_template_alert(
                district, state, pathogen, antibiotic, prediction, 
                top_drivers, severity, emoji
            )
        
        alerts.append({
            'district': district,
            'state': state,
            'pathogen': pathogen,
            'antibiotic': antibiotic,
            'prediction': prediction,
            'severity': severity,
            'language': language,
            'alert_text': alert_text
        })
    
    # Save alerts
    alerts_df = pd.DataFrame(alerts)
    alerts_df.to_csv(f"{ALERTS_DIR}/generated_alerts.csv", index=False)
    
    # Save individual alert files
    for _, alert in alerts_df.iterrows():
        filename = f"{alert['district']}_{alert['pathogen']}_{alert['antibiotic']}".replace(' ', '_')
        with open(f"{ALERTS_DIR}/{filename}.txt", 'w', encoding='utf-8') as f:
            f.write(alert['alert_text'])
    
    print(f"\n✅ Alerts generated: {len(alerts)}")
    print(f"   Saved to: {ALERTS_DIR}/")
    
    # Print summary
    red_count = len(alerts_df[alerts_df['severity'] == 'RED'])
    orange_count = len(alerts_df[alerts_df['severity'] == 'ORANGE'])
    
    print(f"\n📊 Alert Summary:")
    print(f"   🔴 RED: {red_count}")
    print(f"   🟠 ORANGE: {orange_count}")
    
    return alerts_df

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - AI Alert Generator")
    print("=" * 60)
    
    # Load predictions (from Prophet output)
    print("\n📥 Loading predictions...")
    try:
        predictions = pd.read_csv(f"{PROCESSED_DATA_DIR}/prophet_predictions.csv")
        print(f"   Loaded {len(predictions)} predictions")
    except FileNotFoundError:
        print("   ⚠️ Prophet predictions not found. Creating sample...")
        predictions = pd.DataFrame({
            'district': ['Mumbai', 'Chennai', 'Kolkata', 'Jaipur', 'Bangalore'],
            'state': ['Maharashtra', 'Tamil Nadu', 'West Bengal', 'Rajasthan', 'Karnataka'],
            'pathogen': ['Acinetobacter baumannii', 'Klebsiella pneumoniae', 
                        'Escherichia coli', 'Pseudomonas aeruginosa', 'Staphylococcus aureus'],
            'antibiotic': ['Ceftriaxone', 'Ciprofloxacin', 'Gentamicin', 
                          'Imipenem', 'Oxacillin'],
            'prediction': [92.5, 78.3, 65.0, 45.2, 28.7],
            'resistance_velocity': [8.5, 5.2, 3.1, -1.0, -2.3],
            'sales_anomaly_score': [2, 1, 0, 0, 0],
            'is_monsoon': [1, 0, 1, 0, 0]
        })
    
    # Generate alerts (template mode - no API key needed)
    alerts = generate_bulk_alerts(predictions, use_gpt=False)
    
    # Display sample alert
    print("\n" + "=" * 60)
    print("SAMPLE ALERT")
    print("=" * 60)
    print(alerts.iloc[0]['alert_text'])
    
    print("\n" + "=" * 60)
    print("Alert Generation Complete!")
    print("=" * 60)
    print("\n💡 To use GPT-4o, set your OpenAI API key and change use_gpt=True")
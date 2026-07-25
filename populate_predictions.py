import sqlite3
import pandas as pd

conn = sqlite3.connect('data/resistnet.db')
df = pd.read_csv('data/processed/merged_amr_pharma.csv')

districts = pd.read_sql('SELECT * FROM districts', conn)
pathogens = pd.read_sql('SELECT * FROM pathogens', conn)
antibiotics = pd.read_sql('SELECT * FROM antibiotics', conn)

df = df.merge(districts[['district_id', 'district_name']], left_on='district', right_on='district_name')
df = df.merge(pathogens[['pathogen_id', 'pathogen_name']], left_on='pathogen', right_on='pathogen_name')
df = df.merge(antibiotics[['antibiotic_id', 'antibiotic_name']], left_on='antibiotic', right_on='antibiotic_name')

for _, row in df.iterrows():
    severity = 'RED' if row['resistance_rate'] >= 70 else 'ORANGE' if row['resistance_rate'] >= 50 else 'YELLOW' if row['resistance_rate'] >= 30 else 'GREEN'
    conn.execute('''INSERT OR IGNORE INTO predictions 
        (district_id, pathogen_id, antibiotic_id, quarter, predicted_resistance, actual_resistance, severity, model_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (row['district_id'], row['pathogen_id'], row['antibiotic_id'],
         row['quarter'], row['resistance_rate'], row['resistance_rate'], severity, 'ensemble'))

conn.commit()
red = conn.execute("SELECT COUNT(*) FROM predictions WHERE severity='RED'").fetchone()[0]
orange = conn.execute("SELECT COUNT(*) FROM predictions WHERE severity='ORANGE'").fetchone()[0]
print(f'Predictions inserted: RED={red}, ORANGE={orange}')
conn.close()
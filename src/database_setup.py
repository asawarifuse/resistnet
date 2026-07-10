"""
ResistNet - Database Setup & Schema
Uses SQLite (zero-install) for local development.
Same schema works with PostgreSQL for production.
"""

import sqlite3
import pandas as pd
import os

DB_DIR = "data"
DB_NAME = "resistnet.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

PROCESSED_DATA_DIR = "data/processed"

def create_database():
    """Create database and all tables"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🗄️ Creating ResistNet database schema...")
    
    # 1. Districts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS districts (
            district_id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_name TEXT NOT NULL,
            state_name TEXT NOT NULL,
            is_urban INTEGER DEFAULT 0,
            population INTEGER,
            UNIQUE(district_name, state_name)
        )
    """)
    print("   ✅ districts")
    
    # 2. Pathogens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pathogens (
            pathogen_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pathogen_name TEXT NOT NULL UNIQUE,
            pathogen_type TEXT
        )
    """)
    print("   ✅ pathogens")
    
    # 3. Antibiotics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS antibiotics (
            antibiotic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            antibiotic_name TEXT NOT NULL UNIQUE,
            antibiotic_class TEXT
        )
    """)
    print("   ✅ antibiotics")
    
    # 4. Resistance records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resistance_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_id INTEGER,
            pathogen_id INTEGER,
            antibiotic_id INTEGER,
            quarter TEXT NOT NULL,
            year INTEGER,
            month INTEGER,
            resistance_rate REAL,
            samples_tested INTEGER,
            resistant_samples INTEGER,
            data_source TEXT,
            FOREIGN KEY (district_id) REFERENCES districts(district_id),
            FOREIGN KEY (pathogen_id) REFERENCES pathogens(pathogen_id),
            FOREIGN KEY (antibiotic_id) REFERENCES antibiotics(antibiotic_id)
        )
    """)
    print("   ✅ resistance_records")
    
    # 5. Pharma sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharma_sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_id INTEGER,
            antibiotic_id INTEGER,
            month TEXT NOT NULL,
            year INTEGER,
            sales_volume_ddd REAL,
            sales_channel TEXT,
            total_revenue_inr REAL,
            FOREIGN KEY (district_id) REFERENCES districts(district_id),
            FOREIGN KEY (antibiotic_id) REFERENCES antibiotics(antibiotic_id)
        )
    """)
    print("   ✅ pharma_sales")
    
    # 6. Predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_id INTEGER,
            pathogen_id INTEGER,
            antibiotic_id INTEGER,
            quarter TEXT NOT NULL,
            predicted_resistance REAL,
            actual_resistance REAL,
            severity TEXT,
            confidence REAL,
            model_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (district_id) REFERENCES districts(district_id),
            FOREIGN KEY (pathogen_id) REFERENCES pathogens(pathogen_id),
            FOREIGN KEY (antibiotic_id) REFERENCES antibiotics(antibiotic_id)
        )
    """)
    print("   ✅ predictions")
    
    # 7. Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            district_id INTEGER,
            alert_text TEXT,
            severity TEXT,
            language TEXT,
            status TEXT DEFAULT 'generated',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acknowledged_at TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id),
            FOREIGN KEY (district_id) REFERENCES districts(district_id)
        )
    """)
    print("   ✅ alerts")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database created: {DB_PATH}")

def populate_database():
    """Populate database from CSV files"""
    
    conn = sqlite3.connect(DB_PATH)
    
    print("\n📥 Populating database from CSVs...")
    
    # Load merged data
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/merged_amr_pharma.csv")
    print(f"   Loaded {len(df):,} records")
    
    # Insert unique districts
    districts = df[['district', 'state', 'is_urban']].drop_duplicates()
    for _, row in districts.iterrows():
        conn.execute(
            "INSERT OR IGNORE INTO districts (district_name, state_name, is_urban) VALUES (?, ?, ?)",
            (row['district'], row['state'], int(row['is_urban']))
        )
    print(f"   ✅ Districts: {len(districts)}")
    
    # Insert unique pathogens
    pathogens = df[['pathogen']].drop_duplicates()
    for _, row in pathogens.iterrows():
        conn.execute(
            "INSERT OR IGNORE INTO pathogens (pathogen_name) VALUES (?)",
            (row['pathogen'],)
        )
    print(f"   ✅ Pathogens: {len(pathogens)}")
    
    # Insert unique antibiotics
    antibiotics = df[['antibiotic']].drop_duplicates()
    for _, row in antibiotics.iterrows():
        conn.execute(
            "INSERT OR IGNORE INTO antibiotics (antibiotic_name) VALUES (?)",
            (row['antibiotic'],)
        )
    print(f"   ✅ Antibiotics: {len(antibiotics)}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database populated!")

def run_sample_queries():
    """Run sample queries to verify database"""
    
    conn = sqlite3.connect(DB_PATH)
    
    print("\n📊 Sample Queries:")
    
    # Query 1: Count records
    q1 = pd.read_sql("SELECT COUNT(*) as total FROM resistance_records", conn)
    print(f"\n1. Total resistance records: {q1['total'][0]:,}")
    
    # Query 2: Top 5 high resistance districts
    q2 = pd.read_sql("""
        SELECT d.district_name, d.state_name, 
               AVG(r.resistance_rate) as avg_resistance
        FROM resistance_records r
        JOIN districts d ON r.district_id = d.district_id
        GROUP BY d.district_id
        ORDER BY avg_resistance DESC
        LIMIT 5
    """, conn)
    print("\n2. Top 5 High Resistance Districts:")
    print(q2.to_string())
    
    # Query 3: Resistance by pathogen
    q3 = pd.read_sql("""
        SELECT p.pathogen_name, 
               AVG(r.resistance_rate) as avg_resistance,
               COUNT(*) as sample_count
        FROM resistance_records r
        JOIN pathogens p ON r.pathogen_id = p.pathogen_id
        GROUP BY p.pathogen_id
        ORDER BY avg_resistance DESC
    """, conn)
    print("\n3. Resistance by Pathogen:")
    print(q3.to_string())
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - Database Setup")
    print("=" * 60)
    
    create_database()
    populate_database()
    run_sample_queries()
    
    print("\n" + "=" * 60)
    print("Database Setup Complete!")
    print("=" * 60)
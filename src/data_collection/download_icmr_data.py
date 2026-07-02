"""
ResistNet - ICMR AMR Data Downloader
Downloads the latest AMR surveillance report from ICMR website
"""

import requests
import os
from datetime import datetime

# ICMR AMR Annual Report URL (2022 - latest available)
ICMR_REPORT_URL = "https://main.icmr.nic.in/sites/default/files/upload_documents/AMR_Annual_Report_2022.pdf"

# Save path
RAW_DATA_DIR = "data/raw"
REPORT_FILENAME = "ICMR_AMR_Annual_Report_2022.pdf"

def download_icmr_report():
    """Download the ICMR AMR annual report PDF"""
    
    # Create directory if it doesn't exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    save_path = os.path.join(RAW_DATA_DIR, REPORT_FILENAME)
    
    # Skip if already downloaded
    if os.path.exists(save_path):
        print(f"✅ Report already exists: {save_path}")
        print(f"   Size: {os.path.getsize(save_path) / 1024:.1f} KB")
        return save_path
    
    print(f"📥 Downloading ICMR AMR Report...")
    print(f"   URL: {ICMR_REPORT_URL}")
    
    try:
        response = requests.get(ICMR_REPORT_URL, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded successfully!")
        print(f"   Saved to: {save_path}")
        print(f"   Size: {os.path.getsize(save_path) / 1024:.1f} KB")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")
        print("\n💡 Alternative: Download manually from:")
        print("   https://main.icmr.nic.in/content/antimicrobial-resistance-amr")
        print(f"   Save as: {save_path}")
    
    return save_path

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - ICMR Data Downloader")
    print("=" * 60)
    download_icmr_report()
    print("=" * 60)
    print("Done!")
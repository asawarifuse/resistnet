import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

CRITICAL_THRESHOLD = 70.0
WARNING_THRESHOLD = 40.0

def calculate_lead_time():
    print("=" * 60)
    print("RESISTNET - EARLY WARNING LEAD-TIME ANALYSIS")
    print("=" * 60)

    df = pd.read_csv("data/processed/dataset_ml_ready.csv")
    df = df.sort_values(['district','pathogen','antibiotic','quarter'])

    lead_times = []
    detected = 0
    missed = 0
    total = 0
    excluded_already_high = 0
    false_positives = 0

    for _, group in df.groupby(['district','pathogen','antibiotic']):
        rates = group['resistance_rate'].tolist()

        if rates[0] >= CRITICAL_THRESHOLD:
            excluded_already_high += 1
            continue

        critical_pos = None
        for i, r in enumerate(rates):
            if r >= CRITICAL_THRESHOLD:
                critical_pos = i
                break

        if critical_pos is None:
            if any(r >= WARNING_THRESHOLD for r in rates):
                false_positives += 1
            continue

        total += 1

        warning_pos = None
        for i in range(critical_pos):
            if rates[i] >= WARNING_THRESHOLD:
                warning_pos = i
                break

        if warning_pos is not None and warning_pos < critical_pos:
            lead = critical_pos - warning_pos
            lead_times.append(lead)
            detected += 1
        else:
            missed += 1

    if lead_times:
        mean_lead = np.mean(lead_times)
        median_lead = np.median(lead_times)
        max_lead = np.max(lead_times)
        min_lead = np.min(lead_times)
        detection_rate = (detected/total*100) if total else 0
        missed_rate = (missed/total*100) if total else 0
    else:
        mean_lead = median_lead = max_lead = min_lead = 0
        detection_rate = missed_rate = 0

    false_positive_rate = (false_positives / (false_positives + detected) * 100) if (false_positives + detected) > 0 else 0

    print(f"\nEvent Detection Results:")
    print(f"   Events detected: {detected}/{total}")
    print(f"   Detection rate: {detection_rate:.1f}%")
    print(f"   False negatives: {missed}")
    print(f"   False positives: {false_positives}")
    print(f"   False positive rate: {false_positive_rate:.1f}%")
    print(f"   (Warnings that did not lead to critical events)")
    print(f"   Warning threshold: {WARNING_THRESHOLD}%")
    print(f"   Critical threshold: {CRITICAL_THRESHOLD}%")
    print(f"   Evaluation period: 2021-2023")
    print(f"   Lead time - Min: {min_lead:.0f}Q | Median: {median_lead:.1f}Q | Max: {max_lead:.0f}Q")

    return {
        "warning_threshold": WARNING_THRESHOLD,
        "critical_threshold": CRITICAL_THRESHOLD,
        "excluded_already_high": excluded_already_high,
        "total_events": total,
        "detected_early": detected,
        "missed": missed,
        "false_positives": false_positives,
        "false_positive_rate": round(false_positive_rate, 1),
        "detection_rate": round(detection_rate, 1),
        "missed_rate": round(missed_rate, 1),
        "min_lead_quarters": round(min_lead, 0),
        "mean_lead_quarters": round(mean_lead, 1),
        "median_lead_quarters": round(median_lead, 1),
        "max_lead_quarters": round(max_lead, 0),
        "backtest_period": "2021-2023"
    }

if __name__ == "__main__":
    calculate_lead_time()
    print("\nDone!")
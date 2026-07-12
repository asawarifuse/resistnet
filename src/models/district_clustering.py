"""
ResistNet - District Clustering (PCA + K-Means)
Groups Indian districts by AMR resistance profiles.
Identifies risk zones for targeted intervention.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

PROCESSED_DATA_DIR = "data/processed"
REPORTS_DIR = "reports/figures"

def prepare_data():
    """Create district-level feature matrix"""
    print("📥 Preparing district-level data...")
    
    df = pd.read_csv(f"{PROCESSED_DATA_DIR}/dataset_ml_ready.csv")
    
    # Aggregate to district level
    district_features = df.groupby(['state', 'district']).agg({
        'resistance_rate': 'mean',
        'resistance_velocity': 'mean',
        'sales_volume_ddd': 'mean',
        'sales_anomaly_score': 'mean',
        'is_urban_int': 'first',
        'is_monsoon': 'mean'
    }).reset_index()
    
    print(f"   Districts: {len(district_features)}")
    
    return district_features

def apply_pca(X_scaled, feature_names):
    """Reduce dimensions with PCA"""
    print("\n📊 Applying PCA...")
    
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)
    
    # Explained variance
    print("   Variance explained:")
    for i, var in enumerate(pca.explained_variance_ratio_):
        print(f"   PC{i+1}: {var:.3f} ({var*100:.1f}%)")
    
    # Cumulative
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    print(f"\n   First 2 PCs explain: {cumsum[1]*100:.1f}% of variance")
    
    # Scree plot
    plt.figure(figsize=(8, 4))
    plt.bar(range(1, len(pca.explained_variance_ratio_)+1), 
            pca.explained_variance_ratio_, color='steelblue', alpha=0.7)
    plt.plot(range(1, len(cumsum)+1), cumsum, 'ro-', linewidth=2)
    plt.axhline(y=0.9, color='gray', linestyle='--', label='90% threshold')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Explained')
    plt.title('PCA Scree Plot - District AMR Features')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/pca_scree_plot.png", dpi=150, bbox_inches='tight')
    plt.show()
    
    return pca, X_pca

def find_optimal_k(X_pca, max_k=10):
    """Elbow method + silhouette score"""
    print("\n🔍 Finding optimal K...")
    
    inertias = []
    silhouettes = []
    K_range = range(2, max_k+1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_pca[:, :2])
        inertias.append(kmeans.inertia_)
        silhouettes.append(silhouette_score(X_pca[:, :2], labels))
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(K_range, inertias, 'bo-')
    ax1.set_xlabel('Number of Clusters (K)')
    ax1.set_ylabel('Inertia')
    ax1.set_title('Elbow Method')
    
    ax2.plot(K_range, silhouettes, 'ro-')
    ax2.set_xlabel('Number of Clusters (K)')
    ax2.set_ylabel('Silhouette Score')
    ax2.set_title('Silhouette Analysis')
    
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/kmeans_optimal_k.png", dpi=150, bbox_inches='tight')
    plt.show()
    
    best_k = K_range[np.argmax(silhouettes)]
    print(f"   Best silhouette at K={best_k}: {max(silhouettes):.3f}")
    
    return best_k

def cluster_districts(X_pca, district_df, k):
    """Apply K-Means clustering"""
    print(f"\n🎯 Clustering districts into {k} risk groups...")
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    district_df['cluster'] = kmeans.fit_predict(X_pca[:, :2])
    
    # Cluster centers
    centers = kmeans.cluster_centers_
    
    # Plot
    plt.figure(figsize=(10, 7))
    colors = ['#4ECDC4', '#FF6B6B', '#45B7D1', '#FFE66D', '#96CEB4'][:k]
    
    for i in range(k):
        mask = district_df['cluster'] == i
        plt.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   c=colors[i], label=f'Cluster {i+1}', alpha=0.7, s=50)
        plt.scatter(centers[i, 0], centers[i, 1], 
                   c=colors[i], marker='X', s=200, edgecolors='black', linewidth=2)
    
    # Annotate top districts
    for _, row in district_df.iterrows():
        idx = district_df.index.get_loc(row.name)
        if row['resistance_rate'] > district_df['resistance_rate'].quantile(0.95):
            plt.annotate(row['district'], 
                        (X_pca[idx, 0], X_pca[idx, 1]),
                        fontsize=7, alpha=0.8)
    
    plt.xlabel('PC1 — Resistance Magnitude')
    plt.ylabel('PC2 — Resistance Velocity')
    plt.title(f'District AMR Risk Clusters (K={k})')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/district_clusters.png", dpi=150, bbox_inches='tight')
    plt.show()
    
    return district_df

def analyze_clusters(district_df, k):
    """Profile each cluster"""
    print("\n📋 Cluster Analysis:")
    
    for i in range(k):
        cluster = district_df[district_df['cluster'] == i]
        print(f"\n   Cluster {i+1} ({len(cluster)} districts):")
        print(f"   Avg Resistance: {cluster['resistance_rate'].mean():.1f}%")
        print(f"   Avg Sales: {cluster['sales_volume_ddd'].mean():.1f} DDD")
        print(f"   Top districts: {', '.join(cluster.nlargest(3, 'resistance_rate')['district'].tolist())}")
    
    # Save
    district_df.to_csv(f"{PROCESSED_DATA_DIR}/district_clusters.csv", index=False)
    print(f"\n✅ Clusters saved to: data/processed/district_clusters.csv")

if __name__ == "__main__":
    print("=" * 60)
    print("RESISTNET - District Clustering")
    print("=" * 60)
    
    # Prepare
    district_df = prepare_data()
    
    features = ['resistance_rate', 'resistance_velocity', 'sales_volume_ddd', 
                'sales_anomaly_score', 'is_monsoon']
    X = district_df[features].fillna(0)
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA
    pca, X_pca = apply_pca(X_scaled, features)
    
    # Optimal K
    k = find_optimal_k(X_pca)
    
    # Cluster
    district_df = cluster_districts(X_pca, district_df, k)
    
    # Analyze
    analyze_clusters(district_df, k)
    
    print("\n" + "=" * 60)
    print("Clustering Complete!")
    print("=" * 60)
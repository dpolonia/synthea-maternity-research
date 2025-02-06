import pandas as pd
from sklearn.cluster import KMeans

if __name__ == '__main__':
    df = pd.read_csv('data/featured_data.csv')
    # Select relevant features for clustering
    features = df[['financial_stress_index', 'emotional_distress_score', 'age']].fillna(0)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)

    df.to_csv('data/clustered_data.csv', index=False)
    print("Clustering complete. Saved to data/clustered_data.csv")

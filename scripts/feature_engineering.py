import pandas as pd

def compute_emotional_distress_score(row):
    # Example: define a proxy based on number of unscheduled visits
    return row['unscheduled_visits'] * 0.5

if __name__ == '__main__':
    df = pd.read_csv('data/cleaned_data.csv')
    df['emotional_distress_score'] = df.apply(compute_emotional_distress_score, axis=1)
    df.to_csv('data/featured_data.csv', index=False)
    print("Feature engineering complete.")

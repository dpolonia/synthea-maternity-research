import pandas as pd
import os

def load_data(data_path='data'):
    # Example: read all CSV files in data folder
    dfs = []
    for file in os.listdir(data_path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_path, file))
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

if __name__ == '__main__':
    df = load_data()
    print("Data loaded, shape:", df.shape)
    # Additional cleaning steps...
    df.to_csv('data/cleaned_data.csv', index=False)

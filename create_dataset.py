import pandas as pd
import numpy as np

# Create sample dataset
np.random.seed(42)
n_samples = 1000

data = {
    'feature1': np.random.randn(n_samples),
    'feature2': np.random.randn(n_samples),
    'feature3': np.random.randn(n_samples),
    'feature4': np.random.randn(n_samples),
    'target': np.random.randint(0, 2, n_samples)
}

df = pd.DataFrame(data)
df.to_csv('data/dataset.csv', index=False)
print("Dataset created: data/dataset.csv")
print(f"Shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import json

# Load dataset
df = pd.read_csv('data/dataset.csv')
print(f"Dataset loaded: {df.shape}")

# Split features and target
X = df.drop('target', axis=1)
y = df['target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training accuracy: {train_score:.4f}")
print(f"Testing accuracy: {test_score:.4f}")

# Save model
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved to models/model.pkl")

# Save metrics
metrics = {
    'train_accuracy': float(train_score),
    'test_accuracy': float(test_score),
    'n_samples': len(df),
    'n_features': len(X.columns)
}

with open('models/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("Metrics saved to models/metrics.json")

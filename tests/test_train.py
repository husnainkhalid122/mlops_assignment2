import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


def test_data_loading():
    """Test that dataset can be loaded successfully"""
    df = pd.read_csv('data/dataset.csv')
    assert df.shape[0] > 0, "Dataset should not be empty"
    assert df.shape[1] == 5, "Dataset should have 5 columns"
    assert 'target' in df.columns, "Dataset should have target column"


def test_data_shape():
    """Test that dataset has correct shape"""
    df = pd.read_csv('data/dataset.csv')
    assert df.shape == (1000, 5), "Dataset should have shape (1000, 5)"


def test_features_exist():
    """Test that all features exist"""
    df = pd.read_csv('data/dataset.csv')
    required_features = ['feature1', 'feature2', 'feature3', 'feature4', 'target']
    for feature in required_features:
        assert feature in df.columns, f"Dataset should have {feature} column"


def test_model_training():
    """Test that model can be trained"""
    df = pd.read_csv('data/dataset.csv')
    X = df.drop('target', axis=1)
    y = df['target']

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)

    assert model is not None, "Model should be created"
    score = model.score(X, y)
    assert 0 <= score <= 1, "Score should be between 0 and 1"


def test_model_saved():
    """Test that trained model is saved"""
    assert os.path.exists('models/model.pkl'), "Model file should exist"

    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)

    assert model is not None, "Model should be loadable"


def test_model_prediction():
    """Test that model can make predictions"""
    df = pd.read_csv('data/dataset.csv')
    X = df.drop('target', axis=1)

    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)

    predictions = model.predict(X.head(10))
    assert len(predictions) == 10, "Should return predictions for 10 samples"
    assert all(pred in [0, 1] for pred in predictions), "Predictions should be 0 or 1"

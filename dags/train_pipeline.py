from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

def load_data():
    """Load dataset"""
    logger.info("Loading dataset...")
    df = pd.read_csv('/opt/airflow/dags/data/dataset.csv')
    logger.info(f"Dataset loaded: {df.shape}")
    return df

def train_model():
    """Train ML model"""
    logger.info("Training model...")
    df = pd.read_csv('/opt/airflow/dags/data/dataset.csv')
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    logger.info(f"Training accuracy: {train_score:.4f}")
    logger.info(f"Testing accuracy: {test_score:.4f}")
    
    with open('/opt/airflow/dags/models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    logger.info("Model saved successfully")

def save_metrics():
    """Save training metrics"""
    logger.info("Saving metrics...")
    df = pd.read_csv('/opt/airflow/dags/data/dataset.csv')
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with open('/opt/airflow/dags/models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    metrics = {
        'train_accuracy': float(train_score),
        'test_accuracy': float(test_score),
        'n_samples': len(df),
        'n_features': len(X.columns),
        'timestamp': datetime.now().isoformat()
    }
    
    with open('/opt/airflow/dags/models/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info("Metrics saved successfully")
    logger.info(f"Metrics: {metrics}")

# Define DAG
default_args = {
    'owner': 'mlops',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'train_pipeline',
    default_args=default_args,
    description='MLOps Training Pipeline DAG',
    schedule_interval='@daily',
    catchup=False,
)

# Define tasks
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

save_metrics_task = PythonOperator(
    task_id='save_metrics',
    python_callable=save_metrics,
    dag=dag,
)

# Define task dependencies
load_data_task >> train_model_task >> save_metrics_task

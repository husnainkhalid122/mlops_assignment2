from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MLOps Model API",
    description="ML Model Inference API for predictions",
    version="1.0.0"
)

# Load model at startup
MODEL_PATH = "models/model.pkl"
model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")

# Define request schema
class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float

    class Config:
        json_schema_extra = {
            "example": {
                "feature1": 0.5,
                "feature2": 1.4,
                "feature3": -0.67,
                "feature4": -1.91
            }
        }

# Define response schema
class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    message: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running and model is loaded
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make predictions using the trained model
    
    Args:
        request: PredictionRequest with 4 features
        
    Returns:
        PredictionResponse with prediction and probability
    """
    if model is None:
        return {
            "prediction": -1,
            "probability": 0.0,
            "message": "Model not loaded"
        }
    
    try:
        # Prepare features
        features = np.array([[
            request.feature1,
            request.feature2,
            request.feature3,
            request.feature4
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        probability = float(max(probabilities))
        
        logger.info(f"Prediction made: {prediction} with probability {probability:.4f}")
        
        return {
            "prediction": int(prediction),
            "probability": probability,
            "message": f"Successfully predicted class {prediction}"
        }
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return {
            "prediction": -1,
            "probability": 0.0,
            "message": f"Error: {str(e)}"
        }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "MLOps Model Inference API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

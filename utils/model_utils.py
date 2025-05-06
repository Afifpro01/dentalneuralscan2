import os
import logging
import numpy as np
import random

logger = logging.getLogger(__name__)

class SimpleDentalModel:
    """
    A simple model class that simulates dental cavity detection without 
    requiring TensorFlow. For demonstration only.
    """
    def __init__(self):
        self.name = "SimpleDentalModel"
        logger.info("Simple dental model initialized")
    
    def predict(self, image_batch):
        """
        Simulates prediction by analyzing the image color patterns.
        Returns probabilities for each of the 5 dental conditions.
        """
        # Extract basic image features
        # This is a simplified approach for the demo
        avg_color = np.mean(image_batch[0], axis=(0, 1))
        
        # Create probabilities based on image features
        # This is not an actual model, just a demo simulation
        # The brighter the image (higher RGB values), the higher likelihood of early stage conditions
        # Darker images are given higher probability of serious conditions
        
        brightness = np.mean(avg_color)
        
        # Calculate probabilities that somewhat relate to image brightness
        # Darker images will weight more to later categories (more severe conditions)
        # Brighter images will weight more to earlier categories (less severe)
        probabilities = np.zeros(5)
        
        if brightness > 0.7:  # Very bright
            probabilities = np.array([0.6, 0.25, 0.1, 0.03, 0.02])
        elif brightness > 0.5:  # Moderately bright
            probabilities = np.array([0.3, 0.4, 0.2, 0.07, 0.03])
        elif brightness > 0.3:  # Medium
            probabilities = np.array([0.15, 0.25, 0.35, 0.15, 0.1])
        elif brightness > 0.2:  # Quite dark
            probabilities = np.array([0.1, 0.15, 0.25, 0.3, 0.2])
        else:  # Very dark
            probabilities = np.array([0.05, 0.1, 0.2, 0.25, 0.4])
            
        # Add a small random factor (for demonstration)
        noise = np.random.uniform(-0.05, 0.05, 5)
        probabilities += noise
        
        # Ensure probabilities are positive and sum to 1
        probabilities = np.maximum(probabilities, 0)
        probabilities = probabilities / np.sum(probabilities)
        
        return probabilities.reshape(1, 5)


def load_model():
    """
    Load a simple model for dental cavity detection.
    
    Returns:
        A simple model object for dental cavity detection
    """
    logger.info("Loading dental cavity detection model")
    
    try:
        # Create a simple model that doesn't require TensorFlow
        model = SimpleDentalModel()
        
        logger.info("Model initialized successfully")
        return model
    
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        # Return a fallback model in case of error
        return create_fallback_model()

def create_fallback_model():
    """Create a fallback model in case the main model fails to load"""
    logger.warning("Using fallback model")
    return SimpleDentalModel()

def predict_cavity(model, image):
    """
    Use the model to predict dental cavity condition from the image.
    
    Args:
        model: The loaded model
        image: Preprocessed image as a numpy array with shape (224, 224, 3)
        
    Returns:
        A tuple containing (predicted_class_id, confidence_percentage)
    """
    try:
        # Ensure image has correct shape and add batch dimension
        image_batch = np.expand_dims(image, axis=0)
        
        # Get predictions
        predictions = model.predict(image_batch)
        
        # Get the predicted class and confidence
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class]) * 100
        
        # In a real application, map prediction index to actual condition
        # For this example, we'll map the indices directly to condition IDs
        condition_id = predicted_class
        
        logger.info(f"Prediction made: condition_id={condition_id}, confidence={confidence:.2f}%")
        
        return condition_id, round(confidence, 2)
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        # Return a safe fallback prediction
        return 0, 75.0  # Default to the first condition with 75% confidence

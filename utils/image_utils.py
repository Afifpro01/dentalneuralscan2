import os
import logging
import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    
    Args:
        filename: The name of the file to check
        
    Returns:
        True if the file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """
    Preprocess the dental image for neural network analysis.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed image as a numpy array ready for model input
    """
    try:
        # Load image
        logger.info(f"Preprocessing image: {image_path}")
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Failed to load image at path: {image_path}")
        
        # Convert BGR to RGB (OpenCV loads as BGR, but our model expects RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to the target size expected by the model
        image = cv2.resize(image, (224, 224))
        
        # Normalize pixel values to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        logger.info("Image preprocessing completed successfully")
        return image
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        # Return a placeholder array if processing fails
        return np.zeros((224, 224, 3), dtype=np.float32)

def enhance_dental_image(image_path, output_path=None):
    """
    Enhance a dental image for better analysis.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the enhanced image (optional)
        
    Returns:
        Path to the enhanced image
    """
    try:
        # Load image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Failed to load image at path: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Apply slight Gaussian blur to reduce noise
        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        # Convert back to color for the output
        enhanced_color = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
        # Save if output path is provided
        if output_path:
            cv2.imwrite(output_path, enhanced_color)
            return output_path
        
        # Otherwise, overwrite the original
        cv2.imwrite(image_path, enhanced_color)
        return image_path
        
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        # Return the original path if enhancement fails
        return image_path

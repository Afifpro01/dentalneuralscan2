import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_babel import Babel
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np

# Import our utility functions
from utils.model_utils import load_model, predict_cavity
from utils.image_utils import preprocess_image, allowed_file
from utils.dental_conditions import get_dental_conditions
from utils.neural_network_calculator import NeuralNetworkCalculator, get_condition_names

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Configure Babel for internationalization
# In newer Flask-Babel versions, we need to use a different approach for the locale selector
def get_locale():
    # Use the language saved in the session, or default to English
    return session.get('language', 'en')

babel = Babel(app, locale_selector=get_locale)

# Load the model when the app starts
model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    dental_conditions = get_dental_conditions(get_locale())
    return render_template('education.html', conditions=dental_conditions)

@app.route('/neural-network')
def neural_network():
    # Simulasi data input berdasarkan diagnosis terakhir dari session
    # Atau menggunakan contoh data untuk demonstrasi
    sample_features = [0.67, 0.33, 0.5, 0.75, 0.5]  # Contoh fitur input
    
    # Initialize neural network calculator
    nn_calc = NeuralNetworkCalculator()
    
    # Forward propagation
    forward_results = nn_calc.forward_propagation(sample_features)
    
    # Backpropagation (menggunakan prediksi sebagai target untuk demo)
    target_class = forward_results['predicted_class']
    backprop_results = nn_calc.backpropagation(sample_features, target_class, forward_results)
    
    # Calculate metrics
    metrics = nn_calc.calculate_metrics()
    
    # Get formatted weights
    weights = nn_calc.get_weights_formatted()
    
    # Format calculations
    calculations = nn_calc.format_calculations(forward_results)
    
    # Get condition names
    condition_names = get_condition_names(get_locale())
    
    # Prepare data for template
    template_data = {
        'features': {
            'pain_level': sample_features[0],
            'discoloration': sample_features[1], 
            'sensitivity': sample_features[2],
            'additional_symptoms': sample_features[3],
            'duration': sample_features[4],
            'values': sample_features
        },
        'weights': weights,
        'calculations': calculations,
        'backprop': {
            'target_vector': [round(x, 2) for x in backprop_results['target_vector']],
            'output_error': [round(x, 4) for x in backprop_results['output_error']],
            'output_gradients': [round(x, 4) for x in backprop_results['output_gradients']],
            'hidden_gradients': [round(x, 4) for x in backprop_results['hidden_gradients']],
            'learning_rate': backprop_results['learning_rate']
        },
        'metrics': metrics,
        'condition_names': condition_names,
        'result': {
            'predicted_class': forward_results['predicted_class'],
            'confidence': round(forward_results['confidence'], 2)
        }
    }
    
    return render_template('neural_network.html', **template_data)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get form data
        pain_level = int(request.form.get('pain_level', 0))
        discoloration = int(request.form.get('discoloration', 0))
        
        # Get multiple checkbox values
        sensitivity = request.form.getlist('sensitivity[]')
        additional_symptoms = request.form.getlist('additional_symptoms[]')
        
        # Get duration
        duration = request.form.get('duration', '')
        
        # Process the symptoms to generate a feature vector for the model
        # This simulates what a neural network would do with these inputs
        
        # 1. Initialize a feature vector (simplified version for demo)
        feature_vector = np.zeros(5)  # 5 features for our model
        
        # 2. Process pain level (contributes to severity)
        feature_vector[0] = pain_level / 3.0  # Normalize to [0, 1]
        
        # 3. Process discoloration (contributes to condition type and stage)
        feature_vector[1] = discoloration / 3.0  # Normalize to [0, 1]
        
        # 4. Process sensitivity (contributes to condition type)
        # More sensitivity types selected means potentially more severe condition
        if 'none' in sensitivity or not sensitivity:
            feature_vector[2] = 0.0
        else:
            # Count types of sensitivity (excluding 'none')
            sensitivity_count = len(sensitivity)
            feature_vector[2] = min(sensitivity_count / 4.0, 1.0)  # Max 4 types, normalize to [0, 1]
        
        # 5. Process additional symptoms (contributes to severity and infection risk)
        if 'none' in additional_symptoms or not additional_symptoms:
            feature_vector[3] = 0.0
        else:
            # More symptoms means potentially more severe condition
            # Weight certain symptoms more heavily
            symptom_score = 0.0
            for symptom in additional_symptoms:
                if symptom == 'swelling':
                    symptom_score += 0.25
                elif symptom == 'bad-taste':
                    symptom_score += 0.3
                elif symptom == 'visible-hole':
                    symptom_score += 0.2
                elif symptom == 'bleeding':
                    symptom_score += 0.25
                elif symptom == 'fever':
                    symptom_score += 0.5  # Fever is a sign of serious infection
            feature_vector[3] = min(symptom_score, 1.0)  # Clamp to [0, 1]
        
        # 6. Process duration (longer duration might indicate chronic issue)
        if duration == 'recent':
            feature_vector[4] = 0.25
        elif duration == 'short':
            feature_vector[4] = 0.5
        elif duration == 'medium':
            feature_vector[4] = 0.75
        elif duration == 'long':
            feature_vector[4] = 1.0
        else:
            feature_vector[4] = 0.0  # Default
        
        # Use our model to predict condition based on features
        # Here we create a dummy image with the feature values to use our existing model infrastructure
        # In a real implementation, we'd have a separate model for symptom analysis
        dummy_image = np.ones((224, 224, 3)) * feature_vector[0]  # Pain level as base
        
        # Perform prediction
        prediction, confidence = predict_cavity(model, dummy_image)
        
        # Override the prediction based on our features for more realistic results
        # This is where we apply our medical knowledge rules
        
        # Calculate a weighted severity score that determines the condition
        severity_score = (
            feature_vector[0] * 0.3 +  # Pain
            feature_vector[1] * 0.2 +  # Discoloration
            feature_vector[2] * 0.15 + # Sensitivity
            feature_vector[3] * 0.25 + # Additional symptoms
            feature_vector[4] * 0.1    # Duration
        )
        
        # Map severity score to condition ID
        if severity_score < 0.2:
            prediction = 0  # Enamel Damage (Early Stage)
            confidence = min(95 - (severity_score * 100), 99)  # Higher confidence for clear early stage
        elif severity_score < 0.4:
            prediction = 1  # Enamel Decay (Moderate)
            confidence = 80 - abs(0.3 - severity_score) * 100  # Highest confidence at 0.3
        elif severity_score < 0.6:
            prediction = 2  # Dentin Decay
            confidence = 80 - abs(0.5 - severity_score) * 100  # Highest confidence at 0.5
        elif severity_score < 0.8:
            prediction = 3  # Pulp Involvement
            confidence = 80 - abs(0.7 - severity_score) * 100  # Highest confidence at 0.7
        else:
            prediction = 4  # Abscess Formation
            confidence = min((severity_score * 100) - 60, 99)  # Higher confidence for clearly severe cases
            
        # Ensure confidence is in valid range
        confidence = max(min(confidence, 99), 60)  # Between 60% and 99%
        
        # Get condition information in the correct language
        dental_conditions = get_dental_conditions(get_locale())
        condition_info = next((c for c in dental_conditions if c['id'] == prediction), None)
        
        if condition_info:
            # No image to display, so we remove the image_path
            return render_template('results.html', 
                                  prediction=condition_info,
                                  confidence=confidence)
        else:
            flash('Error in condition identification', 'error')
            return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Error processing symptoms: {str(e)}")
        flash('Error processing your symptoms. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/set_language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum file size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    flash('An internal server error occurred. Please try again later.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

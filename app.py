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

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'dental_image' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['dental_image']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Save and process the image
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess the image
        try:
            processed_image = preprocess_image(filepath)
            
            # Perform prediction
            prediction, confidence = predict_cavity(model, processed_image)
            
            # Get condition information in the correct language
            dental_conditions = get_dental_conditions(get_locale())
            condition_info = next((c for c in dental_conditions if c['id'] == prediction), None)
            
            if condition_info:
                return render_template('results.html', 
                                      prediction=condition_info,
                                      confidence=confidence,
                                      image_path=os.path.join('uploads', filename))
            else:
                flash('Error in condition identification', 'error')
                return redirect(url_for('index'))
            
        except Exception as e:
            app.logger.error(f"Error processing image: {str(e)}")
            flash('Error processing the image. Please try again with a clearer dental image.', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file (jpg, jpeg, png).', 'error')
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

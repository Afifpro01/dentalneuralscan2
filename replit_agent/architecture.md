# Architecture

## Overview

DentalScan AI is a web application designed to analyze dental images for early cavity detection. The application uses machine learning to identify potential dental issues from uploaded photos, provides educational resources about dental conditions, and supports multiple languages (currently English and Indonesian). It's built as a web service that provides preliminary analysis, not meant to replace professional dental consultations.

## System Architecture

The application follows a classic web application architecture with three main layers:

1. **Presentation Layer**: HTML templates with Jinja2 templating engine, CSS, and JavaScript
2. **Application Layer**: Flask web framework handling HTTP requests, business logic, and rendering templates
3. **Service Layer**: Utilities for image processing and machine learning model inference

### Architecture Diagram

```
┌─────────────────┐      ┌──────────────────────────────────┐      ┌─────────────────┐
│                 │      │                                  │      │                 │
│  Client Browser │─────▶│ Flask Application (main.py/app.py)│─────▶│ ML Model Service│
│                 │      │                                  │      │                 │
└─────────────────┘      └──────────────────────────────────┘      └─────────────────┘
                                        │
                                        │
                                        ▼
                          ┌────────────────────────────┐
                          │                            │
                          │ Static Files & Translations│
                          │                            │
                          └────────────────────────────┘
```

## Key Components

### Backend (Python/Flask)

- **app.py**: Core application file that initializes the Flask app, configures routes, and handles internationalization
- **main.py**: Entry point for running the application, imports the app from app.py
- **utils/**: Contains utility modules:
  - **model_utils.py**: Handles loading and inference with the dental cavity detection ML model
  - **image_utils.py**: Provides functions for image preprocessing and validation
  - **dental_conditions.py**: Delivers information about various dental conditions

### Frontend

- **templates/**: Jinja2 HTML templates:
  - **layout.html**: Base template with common elements like header and footer
  - **index.html**: Landing page with upload functionality
  - **results.html**: Displays analysis results
  - **education.html**: Educational content about dental conditions
  - **about.html**: Information about the application
- **static/**: Static assets:
  - **css/custom.css**: Custom styling
  - **js/**: JavaScript files for client-side functionality
  - **assets/**: SVG images and icons

### Internationalization

- **translations/**: Contains translation files:
  - **en/LC_MESSAGES/messages.po**: English translations
  - **id/LC_MESSAGES/messages.po**: Indonesian translations
- **babel.cfg**: Configuration for Flask-Babel

## Data Flow

1. **Image Upload**: User uploads a dental image through the web interface
2. **Image Processing**: 
   - Application validates the image format
   - Image is preprocessed using utility functions in image_utils.py
3. **Model Inference**:
   - Preprocessed image is passed to the ML model
   - Model predicts the likelihood of dental cavities
4. **Result Presentation**:
   - Model output is processed and relevant dental condition information is retrieved
   - Results are displayed to the user using the results.html template

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-Babel**: Internationalization support
- **TensorFlow/Keras**: Machine learning framework for the dental cavity detection model
- **OpenCV (cv2)**: Image processing library
- **NumPy**: Numerical computing library
- **Gunicorn**: WSGI HTTP server for production

### Frontend Libraries
- **Bootstrap**: CSS framework for responsive design
- **Font Awesome**: Icon library

## Deployment Strategy

The application is configured for deployment on Replit with the following characteristics:

- **Hosting**: Deployed on Replit's infrastructure using the "autoscale" deployment target
- **WSGI Server**: Gunicorn serves the application
- **Environment**: Python 3.11 environment with OpenSSL and PostgreSQL packages available
- **Starting Command**: `gunicorn --bind 0.0.0.0:5000 main:app`

### Development vs. Production

- **Development**: Run through `main.py` with debug mode enabled
- **Production**: Served via Gunicorn with appropriate settings

## Potential Future Enhancements

1. **Database Integration**: The models.py file suggests plans for database integration, possibly for storing user accounts, analysis history, or detailed dental condition information.
2. **User Authentication**: Currently there is no user authentication system, but the presence of a session secret suggests this might be a planned feature.
3. **Model Improvement**: The current ML model is a placeholder. A more sophisticated, properly trained model could be integrated.
4. **Additional Languages**: The infrastructure for internationalization is in place, allowing for easy addition of more languages.

## Architectural Decisions

### Decision: Use of Flask Framework
- **Rationale**: Flask provides a lightweight, flexible framework that's ideal for this type of application.
- **Alternatives**: Django (more heavyweight, with features not needed for this app), FastAPI (more API-focused)
- **Pros**: Simple to understand, good template system, easy to extend
- **Cons**: Less built-in functionality than Django, might require more manual configuration for larger applications

### Decision: Client-Side Heavy Architecture
- **Rationale**: The application needs to be responsive and user-friendly.
- **Alternatives**: Server-side rendering for all interactions
- **Pros**: Better user experience, reduced server load after initial page load
- **Cons**: Requires more client-side JavaScript, may not work well with JS disabled

### Decision: Separation of Utilities into Modules
- **Rationale**: Separates concerns and improves code organization
- **Alternatives**: Monolithic application file
- **Pros**: Better maintainability, easier testing, clearer responsibilities
- **Cons**: Slightly more complex import structure

### Decision: Flask-Babel for Internationalization
- **Rationale**: Need to support multiple languages (currently English and Indonesian)
- **Alternatives**: Custom internationalization solution
- **Pros**: Well-integrated with Flask, standard approach
- **Cons**: Adds a dependency
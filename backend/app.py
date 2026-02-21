# ===== APP INIT =====
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import uuid
import json
import requests
from dotenv import load_dotenv
import os

# Load specific python env file
load_dotenv('.env.python')

# ===== CUSTOM MODULES =====
from models.resume_text_extractor import extract_text
from models.resume_parser import extract_resume_with_llama
from models.description_analyzer import analyze_text_with_llama
from models.scrapper import LinkedInJobScraper
from models.ectract_skills import process_job_descriptions
from models.skills_analyzer import analyze_skills_with_llama, aggregate_skills
from models.google_api import GoogleSearchAPI
from models.educator_gap import analyze_and_suggest

# ===== NEW ML MODELS =====
from models.learning_path_model import LearningPathGenerator
from models.competency_matrix import CompetencyMatrix
from models.career_trajectory import CareerTrajectory
from models.skill_validation import SkillValidator
from models.market_analysis import MarketAnalyzer

# ===== BLUEPRINTS =====
from routes.roleAssessment import role_assessment_bp
from routes.proctoring import proctoring_bp
from routes.auth import auth_bp, users_db, users_by_id
from routes.skill_evaluation import skill_evaluation_bp

# ===== APP INIT =====
# Get the build directory path BEFORE creating Flask app
# Fix the path to correctly point to frontend build directory
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))

# Create Flask app WITHOUT static folder to avoid conflicts
app = Flask(__name__, static_folder=None)

# Allow same origin since frontend and backend are on same domain
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:63024", "http://localhost:63024", "http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)

# Register the blueprints with the correct URL prefix
# Register the blueprints with the correct URL prefix
app.register_blueprint(role_assessment_bp, url_prefix='/api')
app.register_blueprint(proctoring_bp, url_prefix='/api/proctor')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(skill_evaluation_bp, url_prefix='/api')

# Serve datasets folder
@app.route('/datasets/<path:filename>')
def serve_datasets(filename):
    datasets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
    return send_from_directory(datasets_dir, filename)

# Allow same origin since frontend and backend are on same domain
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:63024", "http://localhost:63024", "http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# ===== CONFIG =====
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-super-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads/resumes'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

jwt = JWTManager(app)

# ===== MOCK DB =====
# Users are now managed in routes/auth.py
active_sessions = {}

# ===== TEST ENDPOINT =====


# ===== GOOGLE API =====
CSE_ID = os.getenv("CSE_ID")
GOOGLE_API_KEY = os.getenv("Google_api_key")
google_search = GoogleSearchAPI(GOOGLE_API_KEY, CSE_ID)

SCRAPE_JOBS_API_URL = "http://127.0.0.1:5000/scrape_jobs"

# ===== NEW ML MODELS INITIALIZATION =====
# Initialize the new ML models
try:
    # Get Google API credentials for learning path model
    google_api_key = os.getenv("Google_api_key")
    google_cse_id = os.getenv("CSE_ID")
    
    # Initialize models
    learning_path_generator = LearningPathGenerator(google_api_key, google_cse_id)
    competency_matrix = CompetencyMatrix()
    career_trajectory = CareerTrajectory()
    skill_validator = SkillValidator()
    market_analyzer = MarketAnalyzer()
    
    print("[OK] All ML models initialized successfully")
except Exception as e:
    print(f"[ERROR] Error initializing ML models: {e}")
    # Fallback initialization without Google API
    learning_path_generator = LearningPathGenerator()
    competency_matrix = CompetencyMatrix()
    career_trajectory = CareerTrajectory()
    skill_validator = SkillValidator()
    market_analyzer = MarketAnalyzer()

# ===== HELPERS =====
def save_resume(file):
    if not file:
        return None
    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

# =========================
# DEBUG ENDPOINT
# =========================
@app.route('/api/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to see all users in database"""
    return jsonify({
        "total_users": len(users_db),
        "users": list(users_db.keys()),
        "user_details": users_db
    })

@app.route('/api/debug/create-test-user', methods=['POST'])
def create_debug_test_user():
    """Create a test user for debugging"""
    test_email = "test@example.com"
    test_password = "Test123!"
    
    if test_email in users_db:
        return jsonify({"message": "Test user already exists"})
    
    # Create test user
    users_db[test_email] = {
        'fullName': 'Test User',
        'email': test_email,
        'password': generate_password_hash(test_password),
        'userType': 'student',
        'profilePhoto': None,
        'resume': None,
        'createdAt': str(uuid.uuid4())
    }
    
    return jsonify({
        "message": "Test user created",
        "email": test_email,
        "password": test_password
    })

@app.route('/api/debug/create-specific-users', methods=['POST'])
def create_specific_users():
    """Create the specific users mentioned by the user"""
    users_to_create = [
        {
            'email': 'samykmottaya@gmail.com',
            'password': 'Danger!123',
            'fullName': 'Samy K Mottaya',
            'userType': 'professor'
        },
        {
            'email': 'abs@gmail.com', 
            'password': 'Danger!123',
            'fullName': 'Muthu',
            'userType': 'student'
        },
        {
            'email': 'test@example.com',
            'password': 'password123',
            'fullName': 'Test User',
            'userType': 'student'
        }
    ]
    
    created_users = []
    for user_data in users_to_create:
        if user_data['email'] in users_db:
            created_users.append({
                'email': user_data['email'],
                'status': 'already exists'
            })
            continue
            
        # Create user
        users_db[user_data['email']] = {
            'fullName': user_data['fullName'],
            'email': user_data['email'],
            'password': generate_password_hash(user_data['password']),
            'userType': user_data['userType'],
            'profilePhoto': None,
            'resume': None,
            'createdAt': str(uuid.uuid4())
        }
        
        created_users.append({
            'email': user_data['email'],
            'password': user_data['password'],
            'fullName': user_data['fullName'],
            'userType': user_data['userType'],
            'status': 'created'
        })
    
    return jsonify({
        "message": "Specific users created successfully",
        "users": created_users
    })

# =========================
# AUTH ROUTES
# =========================
@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("=== REGISTRATION REQUEST ===")
        print("Request headers:", dict(request.headers))
        
        # Check if form data or JSON
        if request.is_json:
            # Handle JSON registration (for testing)
            data = request.get_json()
            print("JSON data received:", data)
            
            fullName = data.get('fullName')
            email = data.get('email')
            password = data.get('password')
            userType = data.get('userType', 'student')
            profilePhoto = None
            resume = None
        else:
            # Handle FormData registration (with files)
            print("FormData received")
            print("Form data keys:", list(request.form.keys()))
            print("Files keys:", list(request.files.keys()))
            
            fullName = request.form.get('fullName')
            email = request.form.get('email')
            password = request.form.get('password')
            userType = request.form.get('userType', 'student')
            
            # Handle file uploads
            profilePhoto = None
            resume = None
            
            if 'profilePhoto' in request.files and request.files['profilePhoto'].filename:
                profilePhoto = save_resume(request.files['profilePhoto'])
                print(f"Profile photo saved: {profilePhoto}")
            
            if 'resume' in request.files and request.files['resume'].filename:
                if userType == 'student':
                    resume = save_resume(request.files['resume'])
                    print(f"Resume saved: {resume}")

        print(f"Registration data: fullName={fullName}, email={email}, userType={userType}")

        # Validate required fields
        if not fullName or not email or not password:
            error_msg = "Full name, email, and password are required"
            print(f"Validation error: {error_msg}")
            return jsonify({"error": error_msg}), 400
        
        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Basic password validation
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Check if user already exists
        if email in users_db:
            return jsonify({"error": "User with this email already exists"}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        
        users_db[email] = {
            'fullName': fullName,
            'email': email,
            'password': hashed_password,
            'userType': userType,
            'profilePhoto': profilePhoto,
            'resume': resume,
            'createdAt': str(uuid.uuid4())
        }
        
        print(f"User created successfully: {email}")
        print(f"Total users in database: {len(users_db)}")

        # Create access token
        access_token = create_access_token(identity=email)
        print("JWT token created successfully")

        # Return response
        response_data = {
            "token": access_token,
            "user": {
                "email": email,
                "fullName": fullName,
                "userType": userType,
                "profilePhoto": profilePhoto,
                "resume": resume
            },
            "message": "Registration successful"
        }
        
        print("Returning registration response")
        return jsonify(response_data)
        
    except Exception as e:
        print("=== REGISTRATION ERROR ===")
        print("Error in register endpoint:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("=== LOGIN REQUEST ===")
        print("Login request headers:", dict(request.headers))
        
        # Get JSON data
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        print("Login request data:", data)
        
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not email or not password:
            error_msg = "Email and password are required"
            print(f"Validation error: {error_msg}")
            return jsonify({"error": error_msg}), 400

        print(f"Login attempt for email: {email}")

        # Check if user exists
        if email not in users_db:
            print(f"User not found: {email}")
            print(f"Available users: {list(users_db.keys())}")
            return jsonify({"error": "Invalid credentials"}), 401

        # Verify password
        user_data = users_db[email]
        print(f"Found user data for: {email}")
        
        if not check_password_hash(user_data['password'], password):
            print(f"Password verification failed for {email}")
            return jsonify({"error": "Invalid credentials"}), 401
            
        print(f"Password verification successful for {email}")

        # Create access token
        access_token = create_access_token(identity=email)
        print("JWT token created successfully")
        
        # Track active session
        active_sessions[email] = {
            "login_time": str(uuid.uuid4()),
            "user_data": {
                "email": email,
                "fullName": user_data.get('fullName', 'User'),
                "userType": user_data.get('userType', 'student'),
                "profilePhoto": user_data.get('profilePhoto'),
                "resume": user_data.get('resume')
            },
            "token_created": True
        }
        
        print(f"✅ User logged in successfully: {email}")
        print(f"Active sessions: {len(active_sessions)}")

        # Return response
        response_data = {
            "token": access_token,
            "user": {
                "email": email,
                "fullName": user_data.get('fullName', 'User'),
                "userType": user_data.get('userType', 'student'),
                "profilePhoto": user_data.get('profilePhoto'),
                "resume": user_data.get('resume')
            },
            "message": "Login successful"
        }
        
        print("Returning login response")
        return jsonify(response_data)

    except Exception as e:
        print("=== LOGIN ERROR ===")
        print("Login error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/api/auth/validate', methods=['GET'])
@jwt_required()
def validate_token():
    """Validate JWT token endpoint"""
    try:
        current_user_email = get_jwt_identity()
        print(f"Token validation successful for: {current_user_email}")
        
        if current_user_email in users_db:
            user_data = users_db[current_user_email]
            return jsonify({
                "valid": True,
                "user": {
                    "email": user_data['email'],
                    "fullName": user_data['fullName'],
                    "userType": user_data['userType']
                }
            })
        else:
            return jsonify({"valid": False, "error": "User not found"}), 404
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return jsonify({"valid": False, "error": str(e)}), 401

@app.route('/api/proctor/log', methods=['POST'])
@jwt_required()
def log_proctor_event():
    """Log proctor mode events"""
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        
        # Log the proctor event
        log_entry = {
            'user_email': current_user_email,
            'timestamp': str(datetime.utcnow()),
            'event_type': data.get('event_type'),
            'message': data.get('message'),
            'severity': data.get('severity', 'info'),
            'metadata': data.get('metadata', {})
        }
        
        print(f"Proctor Log: {log_entry}")
        
        return jsonify({
            "success": True,
            "message": "Proctor event logged successfully"
        })
        
    except Exception as e:
        print(f"Error logging proctor event: {str(e)}")
        return jsonify({"error": "Failed to log proctor event"}), 500

@app.route('/api/proctor/camera', methods=['POST'])
@jwt_required()
def process_camera_frame():
    """Process camera frame for AI analysis"""
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        
        # Get frame data
        frame_data = data.get('frame', '')
        timestamp = data.get('timestamp', str(datetime.utcnow()))
        metadata = data.get('metadata', {})
        
        # Simulate AI camera analysis
        # In production, this would use actual computer vision
        analysis_result = {
            'user_email': current_user_email,
            'timestamp': timestamp,
            'frame_received': bool(frame_data),
            'analysis': {
                'face_detected': True,  # Simulate face detection
                'face_position': {'x': 320, 'y': 240, 'width': 100, 'height': 100},
                'eye_contact': True,  # Simulate eye contact detection
                'attention_score': 0.95,  # High attention
                'multiple_faces': False,  # Single person detected
                'looking_at_screen': True,  # User looking at screen
                'lighting_condition': 'good',  # Good lighting
                'background_clear': True  # Clear background
            },
            'alerts': [],
            'risk_score': 0.05  # Very low risk
        }
        
        # Add alerts if needed
        if not analysis_result['analysis']['face_detected']:
            analysis_result['alerts'].append({
                'type': 'no_face',
                'severity': 'warning',
                'message': 'No face detected in camera feed'
            })
            analysis_result['risk_score'] += 0.2
        
        if not analysis_result['analysis']['eye_contact']:
            analysis_result['alerts'].append({
                'type': 'no_eye_contact',
                'severity': 'info',
                'message': 'User not maintaining eye contact'
            })
            analysis_result['risk_score'] += 0.1
        
        if analysis_result['analysis']['multiple_faces']:
            analysis_result['alerts'].append({
                'type': 'multiple_faces',
                'severity': 'warning',
                'message': 'Multiple faces detected'
            })
            analysis_result['risk_score'] += 0.3
        
        print(f"Camera Analysis: {current_user_email} - Face: {analysis_result['analysis']['face_detected']}, Risk: {analysis_result['risk_score']}")
        
        return jsonify({
            "success": True,
            "analysis": analysis_result,
            "message": "Camera frame processed successfully"
        })
        
    except Exception as e:
        print(f"Error processing camera frame: {str(e)}")
        return jsonify({"error": "Failed to process camera frame"}), 500

@app.route('/api/proctor/camera/start', methods=['POST'])
@jwt_required()
def start_camera_monitoring():
    """Start camera monitoring session"""
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        
        session_info = {
            'user_email': current_user_email,
            'session_id': str(uuid.uuid4()),
            'start_time': str(datetime.utcnow()),
            'camera_config': data.get('config', {}),
            'status': 'started'
        }
        
        print(f"Camera monitoring started: {current_user_email} - Session: {session_info['session_id']}")
        
        return jsonify({
            "success": True,
            "session": session_info,
            "message": "Camera monitoring started successfully"
        })
        
    except Exception as e:
        print(f"Error starting camera monitoring: {str(e)}")
        return jsonify({"error": "Failed to start camera monitoring"}), 500

@app.route('/api/proctor/camera/stop', methods=['POST'])
@jwt_required()
def stop_camera_monitoring():
    """Stop camera monitoring session"""
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        session_id = data.get('session_id')
        
        session_info = {
            'user_email': current_user_email,
            'session_id': session_id,
            'stop_time': str(datetime.utcnow()),
            'status': 'stopped'
        }
        
        print(f"Camera monitoring stopped: {current_user_email} - Session: {session_id}")
        
        return jsonify({
            "success": True,
            "session": session_info,
            "message": "Camera monitoring stopped successfully"
        })
        
    except Exception as e:
        print(f"Error stopping camera monitoring: {str(e)}")
        return jsonify({"error": "Failed to stop camera monitoring"}), 500

@app.route('/api/proctor/analysis', methods=['POST'])
@jwt_required()
def analyze_proctor_data():
    """Analyze proctor data with AI"""
    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        
        # Simulate AI analysis
        analysis_result = {
            'user_email': current_user_email,
            'analysis_type': 'proctor_ai_analysis',
            'timestamp': str(datetime.utcnow()),
            'risk_score': 0.1,  # Low risk score
            'alerts': [
                {
                    'type': 'eye_movement',
                    'message': 'Normal eye movement patterns detected',
                    'severity': 'info'
                },
                {
                    'type': 'posture',
                    'message': 'User posture is appropriate',
                    'severity': 'info'
                },
                {
                    'type': 'environment',
                    'message': 'No unauthorized devices detected',
                    'severity': 'success'
                }
            ],
            'recommendations': [
                'Continue monitoring',
                'Maintain current position',
                'Good lighting conditions detected'
            ]
        }
        
        print(f"Proctor Analysis: {analysis_result}")
        
        return jsonify({
            "success": True,
            "analysis": analysis_result,
            "message": "Proctor data analyzed successfully"
        })
        
    except Exception as e:
        print(f"Error analyzing proctor data: {str(e)}")
        return jsonify({"error": "Failed to analyze proctor data"}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()
    if current_user_email in users_db:
        return jsonify(users_db[current_user_email])
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/profile/update', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_profile():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("=== PROFILE UPDATE DEBUG ===")
        print("Request headers:", dict(request.headers))
        
        current_user_email = get_jwt_identity()
        print(f"Current user from JWT: {current_user_email}")
        
        if current_user_email not in users_db:
            print(f"User not found: {current_user_email}")
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        print(f"Update data received: {data}")
        
        # Update user data
        users_db[current_user_email].update(data)
        
        print(f"Profile updated for {current_user_email}: {data}")
        print(f"Updated user data: {users_db[current_user_email]}")
        
        return jsonify({
            "message": "Profile updated successfully",
            "user": users_db[current_user_email]
        })
        
    except Exception as e:
        print("Error updating profile:", str(e))
        print("Error details:", e)
        return jsonify({"error": "Failed to update profile"}), 500

@app.route('/api/debug/jwt-test', methods=['GET'])
@jwt_required()
def jwt_test():
    try:
        current_user_email = get_jwt_identity()
        print(f"JWT Test - Current user: {current_user_email}")
        print(f"JWT Test - Users in DB: {list(users_db.keys())}")
        
        return jsonify({
            "current_user": current_user_email,
            "users_in_db": list(users_db.keys()),
            "user_exists": current_user_email in users_db
        })
    except Exception as e:
        print(f"JWT Test Error: {e}")
        return jsonify({"error": str(e)}), 500

# =========================
# RESUME ROUTES
# =========================
@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file"}), 400

    text = extract_text(request.files['resume'])
    return jsonify(extract_resume_with_llama(text))

@app.route('/api/ats-check', methods=['POST'])
@jwt_required()
def ats_check():
    try:
        data = request.get_json()
        resume_url = data.get('resumeUrl')
        
        print(f"Q&A evaluation request for resume URL: {resume_url}")
        
        if not resume_url:
            return jsonify({"error": "No resume URL provided"}), 400
        
        user_id = get_jwt_identity()
        if user_id not in users_by_id:
            return jsonify({"error": "User not found"}), 404
        
        # Get the user's resume file path from the URL
        if resume_url.startswith('/api/resumes/'):
            filename = resume_url.replace('/api/resumes/', '')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            print(f"Looking for resume file at: {filepath}")
            
            if os.path.exists(filepath):
                print(f"Resume file found, extracting text...")
                
                # Extract text from the resume file
                text = extract_text_from_file(filepath)
                print(f"Extracted text length: {len(text)} characters")
                
                # Generate ATS score and analysis
                ats_results = generate_ats_score(text)
                
                # Dynamic strengths and improvements based on breakdown
                strengths = []
                improvements = []
                
                if ats_results['breakdown']['formatting'] >= 80:
                    strengths.append("Excellent contact information and basic structure")
                else:
                    improvements.append("Ensure contact details and professional links are clearly visible")
                    
                if ats_results['breakdown']['impact'] >= 60:
                    strengths.append("Good use of quantifiable metrics and action verbs")
                else:
                    improvements.append("Use more numbers and percentages to show impact (e.g., 'Reduced costs by 15%')")
                    
                if len(ats_results['detected_skills']) >= 5:
                    strengths.append(f"Highly relevant keywords detected ({', '.join(ats_results['detected_skills'][:3])})")
                else:
                    improvements.append("Include more industry-standard technical skills relevant to your target role")

                result = {
                    "score": ats_results['score'],
                    "breakdown": ats_results['breakdown'],
                    "detected_skills": ats_results['detected_skills'],
                    "found_sections": ats_results['found_sections'],
                    "analysis": {
                        "strengths": strengths,
                        "improvements": improvements,
                        "optimized_format": [
                            "Use standard section headers (Experience, Education, Skills)",
                            "Avoid using tables, columns, or graphics that confuse ATS scanners",
                            "Use reverse-chronological order for work experience",
                            "Ensure your contact information is in the header",
                            "Use a standard, web-safe font like Arial or Calibri"
                        ]
                    }
                }
                
                print(f"ATS analysis completed with score: {ats_results['score']}")
                
                return jsonify(result)
            else:
                print(f"Resume file not found at: {filepath}")
                return jsonify({"error": "Resume file not found"}), 404
        else:
            print(f"Invalid resume URL format: {resume_url}")
            return jsonify({"error": "Invalid resume URL format"}), 400
            
    except Exception as e:
        print("ATS check error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"ATS check failed: {str(e)}"}), 500

def extract_text_from_file(filepath):
    """Extract text from a PDF file"""
    try:
        # Try PyMuPDF first
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        # Fallback if PyMuPDF is not available
        try:
            # Try using PyPDF2 as fallback
            import PyPDF2
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except ImportError:
            # Final fallback - return mock text
            print("PDF library not available, using mock text")
            return "This is a sample resume text for ATS analysis. The candidate has experience in software development with skills in JavaScript, React, Node.js, and Python. They have a Bachelor's degree in Computer Science and 5+ years of professional experience."
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return "Resume text extraction failed. Please check the PDF file."

def generate_ats_score(text):
    """
    Advanced ATS scoring logic based on multi-factor analysis:
    1. Section Detection (20%)
    2. Keyword Density (40%)
    3. Quantifiable Impact (20%)
    4. Formatting & Contact (20%)
    """
    text_lower = text.lower()
    
    # --- 1. Section Detection (Max 20 pts) ---
    sections = {
        'experience': ['experience', 'work history', 'professional background', 'employment'],
        'education': ['education', 'academic', 'degree', 'university'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'projects': ['projects', 'personal projects', 'portfolio'],
        'summary': ['summary', 'objective', 'profile', 'about me']
    }
    section_score = 0
    found_sections = []
    for sec, keywords in sections.items():
        if any(kw in text_lower for kw in keywords):
            section_score += 4
            found_sections.append(sec.capitalize())
    
    # --- 2. Keyword Density (Max 40 pts) ---
    # Common tech skills library
    skills_library = [
        'python', 'javascript', 'react', 'node', 'java', 'c++', 'aws', 'docker', 'kubernetes',
        'sql', 'nosql', 'mongodb', 'git', 'ci/cd', 'agile', 'scrum', 'html', 'css', 'typescript',
        'machine learning', 'data science', 'analytics', 'rest api', 'graphql', 'express',
        'flask', 'django', 'spring', 'vue', 'angular', 'redux', 'postgreSQL', 'mysql'
    ]
    detected_skills = [skill for skill in skills_library if skill in text_lower]
    # Reward based on number of relevant skills (4 pts per skill, cap at 40)
    keyword_score = min(len(detected_skills) * 4, 40)
    
    # --- 3. Quantifiable Impact (Max 20 pts) ---
    # Detect numbers, percentages, currency, and action verbs
    impact_indicators = [
        r'\d+%', r'%\s+increase', r'%\s+decrease', r'\$\d+', r'₹\d+',
        r'improved', r'delivered', r'managed', r'led', r'built', r'developed'
    ]
    import re
    impact_score = 0
    for pattern in impact_indicators:
        if re.search(pattern, text_lower):
            impact_score += 5
    impact_score = min(impact_score, 20)
    
    # --- 4. Formatting & Contact (Max 20 pts) ---
    formatting_score = 0
    if '@' in text and any(domain in text_lower for domain in ['.com', '.edu', '.org', '.in']):
        formatting_score += 10
    if re.search(r'\d{10}', text) or re.search(r'\+\d+', text): # Phone number
        formatting_score += 10
    
    # Overall Score
    total_score = section_score + keyword_score + impact_score + formatting_score
    
    return {
        "score": min(total_score, 100),
        "breakdown": {
            "keywords": keyword_score * 2.5, # Normalized to 100 for UI display
            "formatting": formatting_score * 5,
            "impact": impact_score * 5,
            "sections": section_score * 5
        },
        "detected_skills": detected_skills,
        "found_sections": found_sections
    }

@app.route('/api/resume/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    print("=== RESUME UPLOAD DEBUG ===")
    print("Request headers:", dict(request.headers))
    print("Request files:", dict(request.files))
    
    if 'resume' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['resume']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        print("File is not PDF")
        return jsonify({"error": "Only PDF files are allowed"}), 400
    
    try:
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save file temporarily to extract text
        temp_filename = f"temp_{uuid.uuid4()}_{secure_filename(file.filename)}"
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(temp_filepath)
        
        # Extract text and verify name/email
        resume_text = extract_text_from_file(temp_filepath)
        user_id = get_jwt_identity()
        user_info = users_by_id.get(user_id, {})
        full_name = user_info.get('fullName', '')
        current_user_email = user_info.get('email', '')
        
        if not user_info:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return jsonify({"error": "User not found"}), 404

        print(f"Verifying resume for {full_name} ({current_user_email})")
        name_parts = [p.lower() for p in full_name.split() if len(p) > 1]
        print(f"Searching for all name parts: {name_parts}")
        name_found = all(part in resume_text.lower() for part in name_parts)
        email_found = current_user_email.lower() in resume_text.lower()
        
        if not name_found or not email_found:
            # Remove temp file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            
            mismatch_reason = []
            if not name_found: mismatch_reason.append(f"Name '{full_name}' not found")
            if not email_found: mismatch_reason.append(f"Email '{current_user_email}' not found")
            
            print(f"Verification failed: {', '.join(mismatch_reason)}")
            return jsonify({
                "error": "Resume information mismatch",
                "message": f"Verify that your resume contains your correct name ({full_name}) and email ({current_user_email}).",
                "details": mismatch_reason
            }), 400
            
        # If verification passes, rename to final filename
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.rename(temp_filepath, filepath)
        
        print(f"File verified and saved: {filename}")
        
        # Update resume URL in database
        users_db[current_user_email]['resumeUrl'] = f"/api/resumes/{filename}"
        print(f"Updated resume URL for {current_user_email} to {users_db[current_user_email]['resumeUrl']}")
        
        response_data = {
            "success": True,
            "fileUrl": f"/api/resumes/{filename}",
            "message": "Resume verified and uploaded successfully"
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error during file upload: {str(e)}")
        return jsonify({"error": "Failed to upload file"}), 500

# Dynamic question generation functions
def generate_dynamic_questions(course, difficulty, base_questions, num_needed):
    """Generate additional questions dynamically based on course content"""
    import random
    
    # Course-specific question generation
    if course == 'quantitative-aptitude':
        return generate_quantitative_questions(base_questions, num_needed)
    elif course == 'logical-reasoning':
        return generate_logical_reasoning_questions(base_questions, num_needed)
    elif course == 'verbal-ability':
        return generate_verbal_ability_questions(base_questions, num_needed)
    elif course == 'data-structures':
        return generate_data_structures_questions(base_questions, num_needed)
    else:
        # Generic questions for unknown courses
        return generate_generic_questions(num_needed)

def generate_additional_questions(course, difficulty, current_count, num_needed):
    """Generate additional questions to reach the required number"""
    additional_questions = []
    
    # Generate course-specific questions based on templates
    if course == 'quantitative-aptitude':
        # Mathematical operations and number theory
        import random, math
        operations = ['+', '-', '*', '/', '÷', '√', '^', 'log']
        numbers = [random.randint(1, 50) for _ in range(3)]
        
        for i in range(num_needed):
            op = random.choice(operations)
            a, b = numbers[i], numbers[i+1] if i+1 < len(numbers) else numbers[0]
            
            if op == '+':
                result = a + b
                explanation = f"Addition: {a} + {b} = {result}"
            elif op == '-':
                result = a - b
                explanation = f"Subtraction: {a} - {b} = {result}"
            elif op == '*':
                result = a * b
                explanation = f"Multiplication: {a} × {b} = {result}"
            elif op == '÷':
                result = a // b
                explanation = f"Division: {a} ÷ {b} = {result:.2f}"
            elif op == '^':
                result = a ** b
                explanation = f"Exponentiation: {a}^{b} = {result}"
            elif op == 'log':
                result = math.log(a, b)
                explanation = f"Logarithm: log({a}) + log({b}) = {result:.4f}"
            elif op == '√':
                result = math.sqrt(a * b)
                explanation = f"Square root: √({a} × {b}) = {result:.4f}"
            
            additional_questions.append({
                'id': current_count + i + 1,
                'question': f'What is {op} when applied to {a} and {b}?',
                'options': [f'{result}', f'{a-b}', f'{a*b}', f'{a/b}', f'{a//b}'],
                'correct': 0,
                'explanation': explanation
            })
    else:
        # Use the dynamic generation for other courses
        base_questions = []
        additional_questions = generate_dynamic_questions(course, difficulty, base_questions, num_needed)
    
    return additional_questions

def generate_quantitative_questions(base_questions, num_needed):
    """Generate quantitative aptitude questions"""
    import random, math
    
    questions = []
    current_count = len(base_questions)
    
    # Percentage problems
    for i in range(min(num_needed, 3)):
        base = random.randint(50, 200)
        percent = random.randint(10, 50)
        result = (base * percent) // 100
        
        questions.append({
            'id': current_count + i + 1,
            'question': f'What is {percent}% of {base}?',
            'options': [str(result), str(base + percent), str(base - percent), str(base * percent)],
            'correct': 0,
            'explanation': f'{percent}% of {base} = ({percent}/100) × {base} = {result}'
        })
    
    # Equation problems
    remaining = num_needed - len(questions)
    for i in range(remaining):
        x = random.randint(1, 20)
        constant = random.randint(1, 50)
        
        questions.append({
            'id': current_count + len(questions) + 1,
            'question': f'If x + {constant} = {x + constant}, what is the value of x?',
            'options': [str(x), str(x + 1), str(x - 1), str(constant)],
            'correct': 0,
            'explanation': f'x + {constant} = {x + constant}, so x = {x}'
        })
    
    return questions

def generate_logical_reasoning_questions(base_questions, num_needed):
    """Generate logical reasoning questions"""
    import random
    
    questions = []
    current_count = len(base_questions)
    
    # Number series
    for i in range(min(num_needed, 2)):
        start = random.randint(2, 10)
        multiplier = random.randint(2, 4)
        series = [start * (multiplier ** j) for j in range(4)]
        next_val = series[-1] * multiplier
        
        questions.append({
            'id': current_count + i + 1,
            'question': f'Find the next number in the series: {", ".join(map(str, series))}, ?',
            'options': [str(next_val), str(series[-1] + start), str(series[-1] * 2), str(series[-1] + multiplier)],
            'correct': 0,
            'explanation': f'Each number is multiplied by {multiplier}. {series[-1]} × {multiplier} = {next_val}'
        })
    
    # Logical deductions
    remaining = num_needed - len(questions)
    for i in range(remaining):
        questions.append({
            'id': current_count + len(questions) + 1,
            'question': 'If all A are B, and some B are C, which statement must be true?',
            'options': ['Some A are C', 'All A are C', 'No A are C', 'Some C are A'],
            'correct': 0,
            'explanation': 'Since all A are B and some B are C, it follows that some A must be C'
        })
    
    return questions

def generate_verbal_ability_questions(base_questions, num_needed):
    """Generate verbal ability questions"""
    import random
    
    synonyms = {
        'happy': ['joyful', 'sad', 'angry', 'tired'],
        'fast': ['quick', 'slow', 'heavy', 'light'],
        'big': ['large', 'small', 'tiny', 'huge'],
        'smart': ['intelligent', 'dumb', 'stupid', 'wise']
    }
    
    antonyms = {
        'hot': ['cold', 'warm', 'cool', 'mild'],
        'up': ['down', 'above', 'over', 'under'],
        'good': ['bad', 'nice', 'great', 'well'],
        'hard': ['soft', 'tough', 'difficult', 'easy']
    }
    
    questions = []
    current_count = len(base_questions)
    
    # Synonym questions
    for i, (word, options) in enumerate(list(synonyms.items())[:min(num_needed, 2)]):
        questions.append({
            'id': current_count + i + 1,
            'question': f'Choose the correct synonym for "{word}":',
            'options': options,
            'correct': 0,
            'explanation': f'{options[0]} is a synonym for {word}'
        })
    
    # Antonym questions
    remaining = num_needed - len(questions)
    for i, (word, options) in enumerate(list(antonyms.items())[:remaining]):
        questions.append({
            'id': current_count + len(questions) + 1,
            'question': f'Which word is the antonym of "{word}"?',
            'options': options,
            'correct': 0,
            'explanation': f'{options[0]} is the antonym (opposite) of {word}'
        })
    
    return questions

def generate_data_structures_questions(base_questions, num_needed):
    """Generate data structures questions"""
    import random
    
    questions = []
    current_count = len(base_questions)
    
    # Time complexity questions
    complexities = [
        ('Binary search', 'O(log n)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
        ('Linear search', 'O(n)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
        ('Bubble sort', 'O(n²)', ['O(n)', 'O(n log n)', 'O(n²)', 'O(n³)']),
        ('Merge sort', 'O(n log n)', ['O(n)', 'O(n log n)', 'O(n²)', 'O(n³)']),
        ('Quick sort', 'O(n log n)', ['O(n)', 'O(n log n)', 'O(n²)', 'O(n³)']),
        ('Hash table lookup', 'O(1)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
        ('Tree traversal', 'O(n)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
        ('Heap insertion', 'O(log n)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)']),
        ('Graph DFS', 'O(V + E)', ['O(V)', 'O(E)', 'O(V + E)', 'O(V * E)']),
        ('Binary tree search', 'O(log n)', ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'])
    ]
    
    # Data structure properties questions
    properties = [
        ('Which data structure uses LIFO principle?', 'Stack', ['Stack', 'Queue', 'Tree', 'Hash Table']),
        ('Which data structure uses FIFO principle?', 'Queue', ['Stack', 'Queue', 'Tree', 'Hash Table']),
        ('What is the main advantage of a hash table?', 'O(1) average lookup time', ['Fast insertion', 'O(1) average lookup time', 'Ordered storage', 'Memory efficiency']),
        ('Which structure is best for priority queue?', 'Heap', ['Array', 'Linked List', 'Heap', 'Stack']),
        ('What is the difference between array and linked list?', 'Memory allocation', ['Memory allocation', 'Time complexity', 'Space complexity', 'Both are same'])
    ]
    
    # Algorithm questions
    algorithms = [
        ('How does binary search work?', 'Divide and conquer', ['Linear scan', 'Divide and conquer', 'Random access', 'Sequential search']),
        ('What is the purpose of dynamic programming?', 'Optimal substructure', ['Greedy choice', 'Optimal substructure', 'Divide and conquer', 'Backtracking']),
        ('Which sorting algorithm is stable?', 'Merge Sort', ['Quick Sort', 'Merge Sort', 'Heap Sort', 'Selection Sort']),
        ('What is a balanced binary tree?', 'O(log n) height', ['O(1) height', 'O(log n) height', 'O(n) height', 'O(n²) height'])
    ]
    
    all_templates = complexities + properties + algorithms
    
    # Generate questions based on num_needed
    for i in range(num_needed):
        template = all_templates[i % len(all_templates)]
        
        # Check if this is a time complexity question (has 3 elements where first is algorithm name)
        if (len(template) == 3 and 
            isinstance(template[0], str) and 
            isinstance(template[1], str) and 
            isinstance(template[2], list) and
            '(' in template[1]):  # Time complexity patterns have O() notation
            algorithm, correct, options = template
            questions.append({
                'id': current_count + i + 1,
                'question': f'What is the time complexity of {algorithm}?',
                'options': options,
                'correct': options.index(correct),
                'explanation': f'{algorithm} has {correct} time complexity'
            })
        else:  # Properties or algorithm question
            question, correct, options = template
            questions.append({
                'id': current_count + i + 1,
                'question': question,
                'options': options,
                'correct': options.index(correct),
                'explanation': f'The correct answer is: {correct}'
            })
    
    return questions

def generate_generic_questions(num_needed):
    """Generate generic questions for unknown courses"""
    questions = []
    
    for i in range(num_needed):
        questions.append({
            'id': i + 1,
            'question': f'Generic question {i + 1}',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': 0,
            'explanation': f'The correct answer is Option A for question {i + 1}'
        })
    
    return questions

# ===== ROLE-SPECIFIC QUESTION GENERATION =====
@app.route('/api/generate-role-questions', methods=['POST'])
@jwt_required()
def generate_role_questions():
    """Generate AI-powered questions for specific job roles"""
    try:
        data = request.get_json()
        role_id = data.get('roleId')
        role_title = data.get('roleTitle')
        required_skills = data.get('requiredSkills', [])
        
        if not role_id or not role_title:
            return jsonify({"error": "Role ID and title are required"}), 400
        
        print(f"Generating questions for role: {role_title} (ID: {role_id})")
        print(f"Required skills: {required_skills}")
        
        # Generate role-specific questions based on the role and skills
        questions = generate_role_specific_questions(role_id, role_title, required_skills)
        
        return jsonify({
            "success": True,
            "role": role_title,
            "questions": questions,
            "totalQuestions": len(questions)
        })
        
    except Exception as e:
        print(f"Error generating role questions: {str(e)}")
        return jsonify({"error": "Failed to generate questions"}), 500

def generate_role_specific_questions(role_id, role_title, required_skills):
    """Generate exactly 10 questions specific to a job role and its required skills"""
    questions = []
    
    # Comprehensive role-specific question templates (ensure at least 10 per role)
    role_question_templates = {
        'frontend-developer': [
            {
                'question': 'What is the purpose of React hooks in modern frontend development?',
                'options': ['To manage component state and lifecycle', 'To style components', 'To handle routing', 'To make API calls'],
                'correct': 0,
                'explanation': 'React hooks allow functional components to use state and lifecycle features'
            },
            {
                'question': 'Which CSS property is used for creating flexible layouts?',
                'options': ['display: block', 'display: flex', 'display: inline', 'display: none'],
                'correct': 1,
                'explanation': 'display: flex creates a flexible container that can arrange items in rows or columns'
            },
            {
                'question': 'What is the purpose of responsive web design?',
                'options': ['To make websites load faster', 'To ensure websites work on all devices', 'To improve SEO', 'To add animations'],
                'correct': 1,
                'explanation': 'Responsive design ensures websites adapt to different screen sizes and devices'
            },
            {
                'question': 'What is the Virtual DOM in React?',
                'options': ['A real DOM tree', 'A JavaScript representation of the DOM', 'A CSS framework', 'A database'],
                'correct': 1,
                'explanation': 'The Virtual DOM is a JavaScript representation of the actual DOM that allows efficient updates'
            },
            {
                'question': 'Which JavaScript method is used to select elements by ID?',
                'options': ['getElementByClass()', 'querySelector()', 'getElementById()', 'getElementsByName()'],
                'correct': 2,
                'explanation': 'getElementById() is the standard method to select elements by their ID'
            },
            {
                'question': 'What is CSS Grid primarily used for?',
                'options': ['Styling text', 'Creating two-dimensional layouts', 'Adding animations', 'Managing colors'],
                'correct': 1,
                'explanation': 'CSS Grid is designed for creating complex two-dimensional layouts'
            },
            {
                'question': 'Which HTTP status code indicates successful request?',
                'options': ['404', '500', '200', '301'],
                'correct': 2,
                'explanation': 'HTTP 200 OK indicates that the request was successful'
            },
            {
                'question': 'What is the purpose of webpack in frontend development?',
                'options': ['Writing CSS', 'Module bundling', 'Database management', 'User authentication'],
                'correct': 1,
                'explanation': 'Webpack is a module bundler that packages JavaScript files for browser use'
            },
            {
                'question': 'Which JavaScript concept allows functions to access variables from their parent scope?',
                'options': ['Hoisting', 'Closures', 'Promises', 'Callbacks'],
                'correct': 1,
                'explanation': 'Closures allow functions to access variables from their parent (enclosing) scope'
            },
            {
                'question': 'What is the primary purpose of responsive images?',
                'options': ['To load images faster', 'To serve appropriate image sizes for different devices', 'To add filters', 'To create animations'],
                'correct': 1,
                'explanation': 'Responsive images ensure optimal loading and display across different screen sizes and resolutions'
            }
        ],
        'backend-developer': [
            {
                'question': 'What is the primary purpose of REST APIs in backend development?',
                'options': ['Database management', 'Communication between client and server', 'User authentication', 'File storage'],
                'correct': 1,
                'explanation': 'REST APIs provide a standardized way for clients to communicate with backend services'
            },
            {
                'question': 'Which database type is best for handling unstructured data?',
                'options': ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite'],
                'correct': 2,
                'explanation': 'MongoDB is a NoSQL database that excels at handling unstructured and semi-structured data'
            },
            {
                'question': 'What is JWT authentication used for?',
                'options': ['Database encryption', 'Secure user authentication', 'API rate limiting', 'Data validation'],
                'correct': 1,
                'explanation': 'JWT tokens provide a secure way to authenticate users in stateless applications'
            },
            {
                'question': 'What is the purpose of database indexing?',
                'options': ['To encrypt data', 'To improve query performance', 'To backup data', 'To validate input'],
                'correct': 1,
                'explanation': 'Database indexes improve the speed of data retrieval operations'
            },
            {
                'question': 'Which HTTP method is typically used for updating existing resources?',
                'options': ['GET', 'POST', 'PUT', 'DELETE'],
                'correct': 2,
                'explanation': 'PUT is the standard HTTP method for updating existing resources'
            },
            {
                'question': 'What is the primary benefit of using microservices architecture?',
                'options': ['Single codebase', 'Independent deployment and scaling', 'Easier debugging', 'Better performance'],
                'correct': 1,
                'explanation': 'Microservices allow independent deployment and scaling of different application components'
            },
            {
                'question': 'What is database connection pooling used for?',
                'options': ['To encrypt connections', 'To reuse database connections for better performance', 'To backup databases', 'To validate queries'],
                'correct': 1,
                'explanation': 'Connection pooling reuses database connections to improve performance and reduce overhead'
            },
            {
                'question': 'Which design pattern is commonly used for database access?',
                'options': ['Singleton', 'Factory', 'Repository', 'Observer'],
                'correct': 2,
                'explanation': 'The Repository pattern provides a way to access data without exposing business logic'
            },
            {
                'question': 'What is the purpose of API rate limiting?',
                'options': ['To improve performance', 'To prevent abuse and ensure fair usage', 'To encrypt data', 'To validate inputs'],
                'correct': 1,
                'explanation': 'Rate limiting prevents API abuse and ensures fair resource usage among clients'
            },
            {
                'question': 'Which protocol is commonly used for real-time communication in web applications?',
                'options': ['HTTP', 'HTTPS', 'WebSocket', 'FTP'],
                'correct': 2,
                'explanation': 'WebSocket provides full-duplex communication channels for real-time web applications'
            }
        ],
        'fullstack-developer': [
            {
                'question': 'What is the key responsibility of a full stack developer?',
                'options': ['Only frontend development', 'Only backend development', 'Both frontend and backend development', 'Only database management'],
                'correct': 2,
                'explanation': 'Full stack developers work on both client-side and server-side development'
            },
            {
                'question': 'Which technology stack is commonly used for full stack development?',
                'options': ['HTML + CSS only', 'MERN Stack', 'Photoshop only', 'Excel macros'],
                'correct': 1,
                'explanation': 'MERN (MongoDB, Express, React, Node.js) is a popular full stack technology stack'
            },
            {
                'question': 'What is the purpose of a full stack developer understanding DevOps?',
                'options': ['Only for deployment', 'For understanding the entire development lifecycle', 'For database design', 'For frontend styling'],
                'correct': 1,
                'explanation': 'DevOps knowledge helps full stack developers understand deployment, CI/CD, and infrastructure'
            },
            {
                'question': 'Which database would a full stack developer typically choose for a new project?',
                'options': ['Only SQL databases', 'Only NoSQL databases', 'Based on project requirements', 'Never use databases'],
                'correct': 2,
                'explanation': 'Full stack developers choose databases based on project requirements, data structure, and scalability needs'
            },
            {
                'question': 'What is the primary purpose of version control in full stack development?',
                'options': ['Only for backup', 'To track changes and collaborate', 'For deployment only', 'For testing only'],
                'correct': 1,
                'explanation': 'Version control systems like Git track changes and enable team collaboration'
            },
            {
                'question': 'Which authentication method is commonly used in full stack applications?',
                'options': ['Only basic auth', 'JWT tokens', 'Only session auth', 'No authentication'],
                'correct': 1,
                'explanation': 'JWT tokens are widely used for stateless authentication in modern full stack applications'
            },
            {
                'question': 'What is the purpose of API documentation in full stack development?',
                'options': ['Only for frontend developers', 'To describe how to use the API', 'For database design', 'For styling'],
                'correct': 1,
                'explanation': 'API documentation helps other developers understand how to use the backend services'
            },
            {
                'question': 'Which testing approach should a full stack developer know?',
                'options': ['Only frontend testing', 'Only backend testing', 'Both unit and integration testing', 'No testing needed'],
                'correct': 2,
                'explanation': 'Full stack developers should understand both unit testing and integration testing'
            },
            {
                'question': 'What is the purpose of environment variables in full stack applications?',
                'options': ['Only for development', 'To manage configuration across environments', 'For styling', 'For database queries'],
                'correct': 1,
                'explanation': 'Environment variables help manage different configurations for development, testing, and production'
            },
            {
                'question': 'Which tool is commonly used for package management in full stack JavaScript development?',
                'options': ['Only npm', 'npm or yarn', 'Only pip', 'No package managers'],
                'correct': 1,
                'explanation': 'npm and yarn are the primary package managers for JavaScript full stack development'
            }
        ],
        'product-manager': [
            {
                'question': 'What is the primary role of a Product Manager?',
                'options': ['Writing code', 'Managing product strategy and development', 'Designing UI', 'Testing software'],
                'correct': 1,
                'explanation': 'Product Managers guide the product vision, strategy, and development process'
            },
            {
                'question': 'What is a product roadmap?',
                'options': ['A physical map', 'A strategic plan for product development', 'A user manual', 'A bug list'],
                'correct': 1,
                'explanation': 'A product roadmap outlines the vision, direction, and progress of a product over time'
            },
            {
                'question': 'What is the purpose of user stories in product management?',
                'options': ['To write code', 'To describe user requirements from their perspective', 'To design UI', 'To test software'],
                'correct': 1,
                'explanation': 'User stories capture requirements from the end user\'s perspective'
            },
            {
                'question': 'Which metric is most important for measuring product success?',
                'options': ['Lines of code', 'User engagement and satisfaction', 'Number of bugs', 'Server uptime'],
                'correct': 1,
                'explanation': 'User engagement and satisfaction are key indicators of product success'
            },
            {
                'question': 'What is the purpose of A/B testing in product management?',
                'options': ['To find bugs', 'To compare different versions of a feature', 'To write code', 'To design UI'],
                'correct': 1,
                'explanation': 'A/B testing helps determine which version of a feature performs better with users'
            },
            {
                'question': 'What is the primary goal of market research for product managers?',
                'options': ['To write code', 'To understand customer needs and market trends', 'To design UI', 'To test software'],
                'correct': 1,
                'explanation': 'Market research helps product managers understand customer needs and market opportunities'
            },
            {
                'question': 'Which framework is commonly used for agile product management?',
                'options': ['Waterfall', 'Scrum', 'Spiral', 'V-Model'],
                'correct': 1,
                'explanation': 'Scrum is widely used for agile product development and management'
            },
            {
                'question': 'What is the purpose of a minimum viable product (MVP)?',
                'options': ['To create a perfect product', 'To test assumptions with minimal features', 'To write all features', 'To design everything'],
                'correct': 1,
                'explanation': 'An MVP tests core assumptions with minimal features to validate the product concept'
            },
            {
                'question': 'Which stakeholder communication is most critical for product managers?',
                'options': ['Only developers', 'Only designers', 'All stakeholders including users, team, and management', 'Only management'],
                'correct': 2,
                'explanation': 'Product managers must communicate with all stakeholders to ensure alignment and success'
            },
            {
                'question': 'What is the purpose of product analytics?',
                'options': ['To count lines of code', 'To measure and improve product performance', 'To design UI', 'To write documentation'],
                'correct': 1,
                'explanation': 'Product analytics help measure user behavior and improve product performance'
            }
        ],
        'data-scientist': [
            {
                'question': 'What is the purpose of machine learning in data science?',
                'options': ['Data storage', 'Making predictions from data', 'Data visualization', 'Data cleaning'],
                'correct': 1,
                'explanation': 'Machine learning algorithms learn patterns from data to make predictions or decisions'
            },
            {
                'question': 'Which programming language is most commonly used in data science?',
                'options': ['Java', 'C++', 'Python', 'PHP'],
                'correct': 2,
                'explanation': 'Python is widely used in data science due to its extensive libraries and ease of use'
            },
            {
                'question': 'What is the purpose of data cleaning in data science?',
                'options': ['To make data look pretty', 'To improve data quality and accuracy', 'To store data', 'To visualize data'],
                'correct': 1,
                'explanation': 'Data cleaning improves data quality and accuracy for better analysis results'
            },
            {
                'question': 'Which statistical concept is fundamental to hypothesis testing?',
                'options': ['Mean', 'Median', 'P-value', 'Standard deviation'],
                'correct': 2,
                'explanation': 'P-values are fundamental to hypothesis testing and determining statistical significance'
            },
            {
                'question': 'What is the purpose of cross-validation in machine learning?',
                'options': ['To speed up training', 'To assess model performance and prevent overfitting', 'To store data', 'To visualize results'],
                'correct': 1,
                'explanation': 'Cross-validation helps assess model performance and prevent overfitting'
            },
            {
                'question': 'Which type of data is most suitable for linear regression?',
                'options': ['Categorical data only', 'Continuous numerical data', 'Text data only', 'Image data only'],
                'correct': 1,
                'explanation': 'Linear regression works best with continuous numerical data'
            },
            {
                'question': 'What is the purpose of feature selection in machine learning?',
                'options': ['To make models slower', 'To improve model performance by selecting relevant features', 'To store more data', 'To visualize data'],
                'correct': 1,
                'explanation': 'Feature selection improves model performance by choosing the most relevant variables'
            },
            {
                'question': 'Which library is commonly used for data manipulation in Python?',
                'options': ['React', 'Pandas', 'Flask', 'Django'],
                'correct': 1,
                'explanation': 'Pandas is the primary library for data manipulation and analysis in Python'
            },
            {
                'question': 'What is the purpose of data visualization in data science?',
                'options': ['To make data look pretty', 'To communicate insights and patterns in data', 'To store data', 'To clean data'],
                'correct': 1,
                'explanation': 'Data visualization helps communicate insights and patterns found in data'
            },
            {
                'question': 'Which machine learning algorithm is best for classification tasks?',
                'options': ['Linear regression', 'Random forest', 'K-means clustering', 'PCA'],
                'correct': 1,
                'explanation': 'Random forest is a powerful algorithm for classification tasks'
            }
        ]
    }
    
    # Get role-specific questions
    base_questions = role_question_templates.get(role_id, [])
    
    # If we have fewer than 10 questions, generate additional ones
    if len(base_questions) < 10:
        additional_questions = generate_additional_role_questions(role_id, required_skills, 10 - len(base_questions))
        base_questions.extend(additional_questions)
    
    # Take exactly 10 questions (or all if fewer than 10 available)
    selected_questions = base_questions[:10]
    
    # Format questions with IDs
    for i, question in enumerate(selected_questions):
        question['id'] = i + 1
    
    return selected_questions

def generate_additional_role_questions(role_id, required_skills, num_needed):
    """Generate additional questions for roles that don't have enough predefined questions"""
    questions = []
    
    # Generic role-based questions
    generic_questions = [
        {
            'question': f'How important is technical proficiency for a {role_id.replace("-", " ").title()}?',
            'options': ['Not important', 'Somewhat important', 'Very important', 'Critical'],
            'correct': 3,
            'explanation': f'Technical proficiency is critical for success as a {role_id.replace("-", " ").title()}'
        },
        {
            'question': f'What is the most valuable skill for a {role_id.replace("-", " ").title()}?',
            'options': ['Communication', 'Problem-solving', 'Technical expertise', 'Time management'],
            'correct': 2,
            'explanation': f'Technical expertise is fundamental for {role_id.replace("-", " ").title()} roles'
        },
        {
            'question': f'Which quality is most important for a {role_id.replace("-", " ").title()}?',
            'options': ['Speed', 'Accuracy', 'Creativity', 'Consistency'],
            'correct': 1,
            'explanation': f'Accuracy is crucial for {role_id.replace("-", " ").title()} work quality'
        }
    ]
    
    # Generate skill-specific questions
    for skill in required_skills[:num_needed]:
        questions.append({
            'question': f'How would you rate your proficiency in {skill}?',
            'options': ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
            'correct': 2,
            'explanation': f'{skill} proficiency is typically expected at an advanced level for professional roles'
        })
    
    # Add generic questions if needed
    while len(questions) < num_needed:
        questions.extend(generic_questions)
    
    return questions[:num_needed]

def generate_skill_based_questions(required_skills, start_id):
    """Generate questions based on specific skills"""
    questions = []
    
    skill_question_map = {
        'JavaScript': [
            {
                'question': 'What is a closure in JavaScript?',
                'options': ['A loop structure', 'A function with access to outer scope', 'An array method', 'A CSS property'],
                'correct': 1,
                'explanation': 'A closure is a function that has access to variables in its outer scope'
            }
        ],
        'React': [
            {
                'question': 'What is the purpose of useState in React?',
                'options': ['To style components', 'To manage component state', 'To handle routing', 'To make API calls'],
                'correct': 1,
                'explanation': 'useState is a hook that allows functional components to manage state'
            }
        ],
        'Python': [
            {
                'question': 'What is Python commonly used for in backend development?',
                'options': ['Frontend styling', 'Server-side scripting and APIs', 'Database design', 'Mobile apps'],
                'correct': 1,
                'explanation': 'Python is widely used for server-side scripting, API development, and backend services'
            }
        ],
        'SQL': [
            {
                'question': 'What is the purpose of SQL in database management?',
                'options': ['User interface design', 'Querying and managing databases', 'Network security', 'File compression'],
                'correct': 1,
                'explanation': 'SQL is used to query, insert, update, and manage data in relational databases'
            }
        ],
        'APIs': [
            {
                'question': 'What is an API endpoint?',
                'options': ['A database table', 'A URL where API requests are sent', 'A user interface', 'A security certificate'],
                'correct': 1,
                'explanation': 'An API endpoint is a specific URL where clients can send API requests'
            }
        ]
    }
    
    for skill in required_skills:
        skill_questions = skill_question_map.get(skill, [])
        for question in skill_questions:
            questions.append(question)
    
    # If we don't have enough skill-specific questions, add generic ones
    while len(questions) < 5:  # Ensure at least 5 questions total
        questions.append({
            'question': f'How important is {skill} for this role?',
            'options': ['Not important', 'Somewhat important', 'Very important', 'Critical'],
            'correct': 3,
            'explanation': f'{skill} is typically critical for success in this role'
        })
        skill = required_skills[0] if required_skills else 'technical skills'
    
    return questions
        
@app.route('/api/analyze-role-results', methods=['POST'])
@jwt_required()
def analyze_role_results():
    """Analyze the results of role-specific questions"""
    try:
        data = request.get_json()
        role_title = data.get('roleTitle')
        role_id = data.get('roleId')
        answers = data.get('answers', [])  # Array of {questionId, selectedOption}
        questions = data.get('questions', [])
        
        if not role_title or not answers or not questions:
            return jsonify({"error": "Role title, answers, and questions are required"}), 400
        
        print(f"Analyzing results for role: {role_title}")
        print(f"Total answers: {len(answers)}")
        
        # Calculate score and analysis
        analysis = calculate_role_analysis(role_id, role_title, questions, answers)
        
        return jsonify({
            "success": True,
            "role": role_title,
            "analysis": analysis
        })
        
    except Exception as e:
        print(f"Error analyzing role results: {str(e)}")
        return jsonify({"error": "Failed to analyze results"}), 500

def calculate_role_analysis(role_id, role_title, questions, answers):
    """Calculate analysis based on user answers"""
    correct_answers = 0
    total_questions = len(questions)
    skill_scores = {}
    
    # Create a map of question ID to question data
    question_map = {q['id']: q for q in questions}
    
    # Process each answer
    for answer in answers:
        question_id = answer.get('questionId')
        selected_option = answer.get('selectedOption')
        
        if question_id in question_map:
            question = question_map[question_id]
            correct_option = question.get('correct', 0)
            
            # Check if answer is correct
            if selected_option == correct_option:
                correct_answers += 1
            
            # Extract skill from question (simple approach)
            question_text = question.get('question', '').lower()
            if 'javascript' in question_text:
                skill = 'JavaScript'
            elif 'react' in question_text:
                skill = 'React'
            elif 'python' in question_text:
                skill = 'Python'
            elif 'sql' in question_text:
                skill = 'SQL'
            elif 'api' in question_text:
                skill = 'APIs'
            else:
                skill = 'General Knowledge'
            
            # Track skill performance
            if skill not in skill_scores:
                skill_scores[skill] = {'correct': 0, 'total': 0}
            
            skill_scores[skill]['total'] += 1
            if selected_option == correct_option:
                skill_scores[skill]['correct'] += 1
    
    # Calculate overall score
    overall_score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Calculate skill percentages
    skill_analysis = []
    for skill, scores in skill_scores.items():
        percentage = (scores['correct'] / scores['total'] * 100) if scores['total'] > 0 else 0
        skill_analysis.append({
            'skill': skill,
            'score': round(percentage),
            'correct': scores['correct'],
            'total': scores['total'],
            'level': 'Strong' if percentage >= 80 else 'Moderate' if percentage >= 60 else 'Needs Improvement'
        })
    
    # Determine readiness level
    readiness = 'High' if overall_score >= 80 else 'Medium' if overall_score >= 60 else 'Low'
    
    # Generate recommendations
    recommendations = generate_role_recommendations(role_id, overall_score, skill_analysis)
    
    # Generate next steps
    next_steps = generate_role_next_steps(role_title, overall_score)
    
    return {
        'overallScore': round(overall_score),
        'correctAnswers': correct_answers,
        'totalQuestions': total_questions,
        'readiness': readiness,
        'skillScores': skill_analysis,
        'recommendations': recommendations,
        'nextSteps': next_steps
    }

def generate_role_recommendations(role_id, overall_score, skill_analysis):
    """Generate recommendations based on role and performance"""
    recommendations = []
    
    # Find weak areas
    weak_skills = [skill for skill in skill_analysis if skill['score'] < 70]
    
    if overall_score >= 80:
        recommendations.append('Excellent performance! You have strong knowledge for this role.')
        recommendations.append('Consider advanced certifications or specialized training.')
    elif overall_score >= 60:
        recommendations.append('Good foundation with room for improvement.')
        if weak_skills:
            recommendations.append(f'Focus on strengthening: {", ".join([s["skill"] for s in weak_skills[:2]])}')
    else:
        recommendations.append('Additional learning recommended for this role.')
        if weak_skills:
            recommendations.append(f'Priority areas to study: {", ".join([s["skill"] for s in weak_skills[:3]])}')
        recommendations.append('Consider foundational courses and hands-on practice.')
    
    return recommendations

def generate_role_next_steps(role_title, overall_score):
    """Generate next steps based on performance"""
    if overall_score >= 80:
        return [
            f'Start applying for {role_title} positions',
            'Build a portfolio showcasing relevant projects',
            'Network with professionals in this field',
            'Consider specialized certifications'
        ]
    elif overall_score >= 60:
        return [
            'Complete recommended skill improvements',
            'Work on practical projects in this area',
            'Seek mentorship or guidance',
            'Consider intermediate certifications'
        ]
    else:
        return [
            'Focus on foundational skills and concepts',
            'Take beginner courses and tutorials',
            'Practice with hands-on exercises',
            'Find a mentor or study group'
        ]
        
@app.route('/api/resume/delete', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_resume():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        current_user_email = get_jwt_identity()
        if current_user_email not in users_db:
            return jsonify({"error": "User not found"}), 404
        
        # Get current resume URL
        resume_url = users_db[current_user_email].get('resumeUrl')
        
        if resume_url:
            # Delete the file from filesystem if it exists
            if resume_url.startswith('/api/resumes/'):
                filename = resume_url.replace('/api/resumes/', '')
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"Deleted resume file: {filepath}")
        
        # Clear resume URL from user data
        users_db[current_user_email]['resumeUrl'] = ''
        
        return jsonify({
            "success": True,
            "message": "Resume deleted successfully"
        })
        
    except Exception as e:
        print("Error deleting resume:", str(e))
        return jsonify({"error": "Failed to delete resume"}), 500

@app.route('/api/resumes/<filename>')
def get_resume(filename):
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename,
            mimetype='application/pdf',
            as_attachment=False
        )
    except Exception as e:
        print("Error serving resume:", str(e))
        return jsonify({"error": "Resume file not found"}), 404

@app.route('/api/resumes/<filename>/download')
def download_resume(filename):
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='Mottaya_Samy_K_Resume.pdf'
        )
    except Exception as e:
        print("Error downloading resume:", str(e))
        return jsonify({"error": "Resume file not found"}), 404

# Serve uploaded files
@app.route('/api/uploads/<path:folder>/<filename>')
def uploaded_file(folder, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)
# =========================
# ANALYSIS ROUTES
# =========================
@app.route('/analyze_description', methods=['POST'])
def analyze_description():
    return jsonify(analyze_text_with_llama(request.json.get('description', '')))


@app.route('/scrape_jobs', methods=['POST'])
def scrape_jobs():
    data = request.json
    scraper = LinkedInJobScraper()
    scraper.login(os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))
    scraper.scrape_job_listings(data['role'], data['location'], 10)
    return jsonify({"job_skills": process_job_descriptions()})


@app.route('/analyze_skills', methods=['POST'])
def analyze_skills():
    if not os.path.exists('job_skills.json'):
        return jsonify({"error": "Run scraper first"}), 400

    job_skills = json.load(open('job_skills.json'))
    common, missing = aggregate_skills(request.json['user_skills'], job_skills)
    return jsonify({
        "common_skills": common,
        "missing_skills": missing,
        "llama_recommendations": analyze_skills_with_llama(request.json['user_skills'], missing)
    })

# =========================
# LEARNING & EDUCATOR
# =========================
@app.route('/get-learning-path', methods=['POST'])
def learning_path():
    return jsonify({
        "resources": google_search.get_learning_path(request.json['language'])
    })


@app.route('/curriculum_plan')
def curriculum_plan():
    return jsonify(google_search.get_curriculum_plan(request.args.get('language')))


@app.route('/educator_gap', methods=['POST'])
def educator_gap():
    return jsonify(
        analyze_and_suggest(request.json['description'], 'job_skills.json')
    )

# =========================
# QUESTIONS API
# =========================
@app.route('/api/questions/<course>/<difficulty>', methods=['GET'])
def get_questions(course, difficulty):
    """Get practice questions for a specific course and difficulty level using AI generation"""
    try:
        print(f"=== QUESTIONS REQUEST ===")
        print(f"Course: {course}")
        print(f"Difficulty: {difficulty}")
        
        # Handle special case for 'technical' course - generate questions for all technical courses
        if course.lower() == 'technical':
            technical_courses = ['data-structures', 'algorithms', 'programming']
            all_questions = []
            
            # Generate questions for each technical course
            for tech_course in technical_courses:
                # Generate questions based on difficulty
                if tech_course == 'data-structures':
                    questions = generate_data_structures_questions([], 12)
                elif tech_course == 'algorithms':
                    questions = generate_data_structures_questions([], 10)
                elif tech_course == 'programming':
                    questions = generate_data_structures_questions([], 10)
                else:
                    questions = generate_generic_questions(8)
                
                # Add course and difficulty info to each question
                for q in questions:
                    q['course'] = tech_course
                    q['difficulty'] = difficulty
                    q['id'] = len(all_questions) + 1
                    all_questions.append(q)
            
            # Shuffle questions for variety
            import random
            random.shuffle(all_questions)
            
            # Limit based on difficulty
            if difficulty.lower() == 'low':
                questions = all_questions[:15]
            elif difficulty.lower() == 'medium':
                questions = all_questions[:25]
            else:  # high
                questions = all_questions[:35]
            
            return jsonify({
                "course": "technical",
                "difficulty": difficulty,
                "questions": questions,
                "total": len(questions),
                "generated": True,
                "courses_covered": technical_courses,
                "message": f"Generated {len(questions)} AI questions for technical - {difficulty} covering all technical courses"
            })
        
        # Validate inputs for individual courses
        valid_courses = ['data-structures', 'algorithms', 'programming', 'quantitative-aptitude', 'logical-reasoning', 'verbal-ability']
        valid_difficulties = ['low', 'medium', 'high']
        
        if course.lower() not in valid_courses:
            return jsonify({"error": f"Course '{course}' not found"}), 404
        
        if difficulty.lower() not in valid_difficulties:
            return jsonify({"error": f"Difficulty '{difficulty}' not found"}), 404
        
        # Generate questions dynamically using AI generation functions
        questions = []
        
        if course.lower() == 'data-structures':
            questions = generate_data_structures_questions([], 10)
        elif course.lower() == 'algorithms':
            questions = generate_data_structures_questions([], 8)  # Use data structures generator for algorithms
        elif course.lower() == 'programming':
            questions = generate_data_structures_questions([], 8)  # Use data structures generator for programming
        elif course.lower() == 'quantitative-aptitude':
            questions = generate_quantitative_questions([], 10)
        elif course.lower() == 'logical-reasoning':
            questions = generate_logical_reasoning_questions([], 10)
        elif course.lower() == 'verbal-ability':
            questions = generate_verbal_ability_questions([], 10)
        else:
            questions = generate_generic_questions(5)
        
        # Adjust question difficulty based on requested level
        if difficulty.lower() == 'low':
            # Keep simpler questions (first 5)
            questions = questions[:5]
        elif difficulty.lower() == 'medium':
            # Keep medium difficulty questions (first 8)
            questions = questions[:8]
        elif difficulty.lower() == 'high':
            # Use all questions for high difficulty
            questions = questions
        
        # Add course and difficulty info to each question
        for i, q in enumerate(questions):
            q['id'] = i + 1
            q['course'] = course
            q['difficulty'] = difficulty
        
        return jsonify({
            "course": course,
            "difficulty": difficulty,
            "questions": questions,
            "total": len(questions),
            "generated": True,
            "message": f"Generated {len(questions)} AI questions for {course} - {difficulty}"
        })
        
    except Exception as e:
        print(f"Error in get_questions: {e}")
        return jsonify({"error": "Failed to generate questions"}), 500

@app.route('/api/start-practice/<category>', methods=['GET'])
def start_practice_test(category):
    """Generate questions directly for a category without difficulty selection"""
    try:
        print(f"=== START PRACTICE TEST ===")
        print(f"Category: {category}")
        
        # Map categories to question types
        category_mapping = {
            'technical': ['data-structures', 'algorithms', 'programming'],
            'aptitude': ['quantitative-aptitude', 'logical-reasoning', 'verbal-ability'],
            'mock-interview': ['data-structures', 'logical-reasoning', 'quantitative-aptitude']
        }
        
        # Get courses for the selected category
        if category.lower() not in category_mapping:
            return jsonify({"error": f"Category '{category}' not found"}), 404
        
        courses = category_mapping[category.lower()]
        all_questions = []
        
        # Generate questions for each course in the category
        for course in courses:
            # Mix of difficulty levels for comprehensive practice
            difficulties = ['low', 'medium', 'high']
            
            for difficulty in difficulties:
                # Generate questions dynamically
                if course == 'data-structures':
                    questions = generate_data_structures_questions([], 5)
                elif course == 'quantitative-aptitude':
                    questions = generate_quantitative_questions([], 5)
                elif course == 'logical-reasoning':
                    questions = generate_logical_reasoning_questions([], 5)
                elif course == 'verbal-ability':
                    questions = generate_verbal_ability_questions([], 5)
                elif course == 'algorithms':
                    questions = generate_data_structures_questions([], 3)  # Use data structures for algorithms
                elif course == 'programming':
                    questions = generate_data_structures_questions([], 3)  # Use data structures for programming
                else:
                    questions = generate_generic_questions(3)
                
                # Add course and difficulty info to each question
                for q in questions:
                    q['course'] = course
                    q['difficulty'] = difficulty
                    q['id'] = len(all_questions) + 1
                
                all_questions.extend(questions)
        
        # Shuffle questions for random order
        import random
        random.shuffle(all_questions)
        
        # Limit to 20 questions for practice test
        practice_questions = all_questions[:20]
        
        return jsonify({
            "category": category,
            "total_questions": len(practice_questions),
            "questions": practice_questions,
            "courses_covered": courses,
            "message": f"Generated {len(practice_questions)} questions for {category} practice test"
        })
        
    except Exception as e:
        print(f"Error in start_practice_test: {e}")
        return jsonify({"error": "Failed to generate practice test"}), 500

@app.route('/api/difficulty-selection/<category>', methods=['GET'])
def difficulty_selection(category):
    """Generate AI questions for all courses in a category"""
    try:
        print(f"=== DIFFICULTY SELECTION ===")
        print(f"Category: {category}")
        
        # Map categories to question types
        category_mapping = {
            'technical-skills': ['data-structures', 'algorithms', 'programming'],
            'aptitude-skills': ['quantitative-aptitude', 'logical-reasoning', 'verbal-ability'],
            'interview-skills': ['data-structures', 'logical-reasoning', 'quantitative-aptitude']
        }
        
        if category.lower() not in category_mapping:
            return jsonify({"error": f"Category '{category}' not found"}), 404
        
        courses = category_mapping[category.lower()]
        all_questions = []
        
        # Generate questions for each course in the category
        for course in courses:
            # Mix of difficulty levels for comprehensive practice
            difficulties = ['low', 'medium', 'high']
            
            for difficulty in difficulties:
                # Generate questions dynamically
                if course == 'data-structures':
                    questions = generate_data_structures_questions([], 5)
                elif course == 'algorithms':
                    questions = generate_data_structures_questions([], 4)  # Use data structures generator for algorithms
                elif course == 'programming':
                    questions = generate_data_structures_questions([], 4)  # Use data structures generator for programming
                elif course == 'quantitative-aptitude':
                    questions = generate_quantitative_questions([], 5)
                elif course == 'logical-reasoning':
                    questions = generate_logical_reasoning_questions([], 5)
                elif course == 'verbal-ability':
                    questions = generate_verbal_ability_questions([], 5)
                else:
                    questions = generate_generic_questions(3)
                
                # Add course and difficulty info to each question
                for q in questions:
                    q['course'] = course
                    q['difficulty'] = difficulty
                    q['id'] = len(all_questions) + 1
                    all_questions.append(q)
        
        # Shuffle questions for random order
        import random
        random.shuffle(all_questions)
        
        # Limit to 30 questions for comprehensive test
        selection_questions = all_questions[:30]
        
        return jsonify({
            "category": category,
            "total_questions": len(selection_questions),
            "questions": selection_questions,
            "courses_covered": courses,
            "generated": True,
            "message": f"Generated {len(selection_questions)} AI questions for {category} covering all technical courses"
        })
        
    except Exception as e:
        print(f"Error in difficulty_selection: {e}")
        return jsonify({"error": "Failed to generate questions"}), 500

# Track active sessions (in production, use Redis or database)
active_sessions = {}

@app.route('/api/debug/sessions', methods=['GET'])
def debug_sessions():
    """Debug endpoint to show active sessions and recent logins"""
    return jsonify({
        "active_sessions": active_sessions,
        "total_users": len(users_db),
        "available_users": list(users_db.keys())
    })

# Add session tracking to login endpoint

@app.route('/test')
def test_route():
    return jsonify({"message": "Test route working!"})

@app.route('/test-static')
def test_static_route():
    return jsonify({"message": "Static route working!"})

@app.route('/routes')
def list_routes():
    import urllib
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({"routes": routes})

@app.route('/static-test/<path:filename>')
def static_test(filename):
    print(f"=== STATIC TEST CALLED ===")
    print(f"Filename: {filename}")
    return jsonify({"message": f"Static test called for: {filename}"})

@app.route('/test-static-file')
def test_static_file():
    """Test endpoint to verify static file serving"""
    try:
        # Check for both old and new CSS files
        css_file_old = os.path.join(BUILD_DIR, 'static', 'css', 'main.02f2feb1.css')
        css_file_new = os.path.join(BUILD_DIR, 'static', 'css', 'main.25484958.css')
        js_file = os.path.join(BUILD_DIR, 'static', 'js', 'main.df7e3c5b.js')
        
        # Find which CSS file exists
        css_file_path = None
        css_file_name = None
        if os.path.exists(css_file_new):
            css_file_path = css_file_new
            css_file_name = "main.25484958.css"
        elif os.path.exists(css_file_old):
            css_file_path = css_file_old
            css_file_name = "main.02f2feb1.css"
        
        # Test the actual static serving logic
        test_filename = "css/main.25484958.css"
        static_dir = os.path.join(BUILD_DIR, 'static')
        test_file_path = os.path.join(static_dir, test_filename)
        
        return jsonify({
            "css_file": {
                "path": css_file_path,
                "name": css_file_name,
                "exists": css_file_path is not None,
                "url": f"/static/css/{css_file_name}" if css_file_name else None
            },
            "js_file": {
                "path": js_file,
                "exists": os.path.exists(js_file),
                "url": "/static/js/main.df7e3c5b.js"
            },
            "build_dir": BUILD_DIR,
            "build_dir_exists": os.path.exists(BUILD_DIR),
            "static_dir": os.path.join(BUILD_DIR, 'static'),
            "static_dir_exists": os.path.exists(os.path.join(BUILD_DIR, 'static')),
            "test_static_logic": {
                "test_filename": test_filename,
                "static_dir": static_dir,
                "test_file_path": test_file_path,
                "test_file_exists": os.path.exists(test_file_path)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# SERVE REACT FRONTEND
# =========================

print(f"Build directory: {BUILD_DIR}")
print(f"Build directory exists: {os.path.exists(BUILD_DIR)}")

# Since Flask static serving is disabled, we need to handle all files manually
# Route order is critical - more specific routes must come first

# 1. SERVE STATIC FILES FIRST - HIGHEST PRIORITY
@app.route('/static/<path:filename>')
def serve_static_react(filename):
    try:
        print(f"=== STATIC REQUEST ===")
        print(f"Filename: {filename}")
        print(f"BUILD_DIR: {BUILD_DIR}")
        
        static_dir = os.path.join(BUILD_DIR, 'static')
        file_path = os.path.join(static_dir, filename)
        
        print(f"Static dir: {static_dir}")
        print(f"Full path: {file_path}")
        print(f"Exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            print(f"✅ Found and serving: {filename}")
            return send_from_directory(static_dir, filename)
        else:
            print(f"❌ Not found: {filename}")
            
            # List available files
            if os.path.exists(static_dir):
                try:
                    files = []
                    for root, dirs, filenames in os.walk(static_dir):
                        for f in filenames:
                            rel_path = os.path.relpath(os.path.join(root, f), static_dir)
                            files.append(rel_path)
                    print(f"Available files: {files}")
                except Exception as e:
                    print(f"Error listing files: {e}")
            
            return jsonify({"error": f"File not found: {filename}"}), 404
        
    except Exception as e:
        print(f"Error serving static file: {e}")
        return jsonify({"error": str(e)}), 500

# 2. Serve static files (CSS, JS, images) - Use /assets/ to avoid Flask static conflicts
@app.route('/assets/<path:filename>')
def serve_static(filename):
    try:
        print(f"=== STATIC FILE REQUEST ===")
        print(f"Serving static file: {filename}")
        static_path = os.path.join(BUILD_DIR, 'static', filename)
        print(f"Full static path: {static_path}")
        print(f"Static path exists: {os.path.exists(static_path)}")
        
        if os.path.exists(static_path):
            print(f"✅ Static file found, serving: {filename}")
            return send_from_directory(os.path.join(BUILD_DIR, 'static'), filename)
        else:
            print(f"❌ Static file not found: {static_path}")
            # List directory contents for debugging
            try:
                static_dir = os.path.join(BUILD_DIR, 'static')
                if os.path.exists(static_dir):
                    files = os.listdir(static_dir)
                    print(f"Files in static directory: {files}")
                else:
                    print(f"Static directory does not exist: {static_dir}")
            except Exception as e:
                print(f"Error listing static directory: {e}")
            return jsonify({"error": f"Static file not found: {filename}"}), 404
    except Exception as e:
        print(f"❌ Error serving static file {filename}: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# 3. Root route - serve index.html
@app.route('/')
def serve_index():
    try:
        print("Serving index.html for root route")
        return send_from_directory(BUILD_DIR, 'index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return jsonify({"error": "Application not found"}), 404

# 4. Catch-all route for React Router - LEAST SPECIFIC (must come last)
@app.route('/<path:filename>')
def serve_root_files(filename):
    try:
        print(f"Request for path: {filename}")
        
        # Check if it's a static file request - let the dedicated static route handle it
        if filename.startswith('static/'):
            print(f"Static file request, should be handled by dedicated route: {filename}")
            # Try to serve it directly from here to avoid routing conflicts
            try:
                static_dir = os.path.join(BUILD_DIR, 'static')
                file_path = os.path.join(static_dir, filename[7:])  # Remove 'static/' prefix
                if os.path.exists(file_path):
                    print(f"✅ Serving static file directly: {filename}")
                    return send_from_directory(static_dir, filename[7:])
                else:
                    print(f"❌ Static file not found: {filename}")
                    return jsonify({"error": f"Static file not found: {filename}"}), 404
            except Exception as e:
                print(f"Error serving static file {filename}: {e}")
                return jsonify({"error": f"Error serving static file: {filename}"}), 500
        
        # Check if file exists in build directory (favicon.ico, manifest.json, etc.)
        file_path = os.path.join(BUILD_DIR, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"Serving root file: {filename}")
            return send_from_directory(BUILD_DIR, filename)
        
        # For all other routes, serve index.html for React Router
        print(f"Serving index.html for React Router path: {filename}")
        return send_from_directory(BUILD_DIR, 'index.html')
        
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        # Fallback to index.html for React Router
        return send_from_directory(BUILD_DIR, 'index.html')

# =========================
# NEW ML MODELS API ENDPOINTS
# =========================

# ===== LEARNING PATH ENDPOINTS =====
@app.route('/api/learning-path/generate', methods=['POST'])
@jwt_required()
def generate_learning_path():
    """Generate personalized learning path"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Required parameters
        target_skills = data.get('target_skills', [])
        current_skills = data.get('current_skills', {})
        learning_goals = data.get('learning_goals', [])
        time_availability = data.get('time_availability', 5)  # hours per week
        
        if not target_skills:
            return jsonify({"error": "Target skills are required"}), 400
        
        # Generate learning path
        learning_path = learning_path_generator.generate_learning_path(
            user_id=user_id,
            target_skills=target_skills,
            current_skills=current_skills,
            learning_goals=learning_goals,
            time_availability=time_availability
        )
        
        return jsonify({
            "success": True,
            "learning_path": learning_path,
            "message": "Learning path generated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/learning-path/progress', methods=['POST'])
@jwt_required()
def update_learning_progress():
    """Update learning progress"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        path_id = data.get('path_id')
        skill = data.get('skill')
        progress = data.get('progress', 0)
        
        if not path_id or not skill:
            return jsonify({"error": "Path ID and skill are required"}), 400
        
        # Update progress
        result = learning_path_generator.update_progress(user_id, path_id, skill, progress)
        
        return jsonify({
            "success": True,
            "result": result,
            "message": "Progress updated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== COMPETENCY MATRIX ENDPOINTS =====
@app.route('/api/competency/assess', methods=['POST'])
@jwt_required()
def assess_competency():
    """Assess user competency matrix"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Required parameters
        target_role = data.get('target_role')
        user_skills = data.get('user_skills', {})
        experience_level = data.get('experience_level', 'beginner')
        
        if not target_role:
            return jsonify({"error": "Target role is required"}), 400
        
        # Initialize competency framework
        competency_matrix.initialize_framework()
        
        # Assess user competency
        assessment_result = competency_matrix.assess_user_competency(
            user_id=user_id,
            target_role=target_role,
            user_skills=user_skills,
            experience_level=experience_level
        )
        
        return jsonify({
            "success": True,
            "assessment": assessment_result,
            "message": "Competency assessment completed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/competency/gap-analysis', methods=['POST'])
@jwt_required()
def analyze_skill_gaps():
    """Analyze skill gaps"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        target_role = data.get('target_role')
        user_skills = data.get('user_skills', {})
        
        if not target_role:
            return jsonify({"error": "Target role is required"}), 400
        
        # Analyze skill gaps
        gap_analysis = competency_matrix.analyze_skill_gaps(target_role, user_skills)
        
        # Generate development plan
        development_plan = competency_matrix.generate_development_plan(
            target_role, user_skills, gap_analysis
        )
        
        return jsonify({
            "success": True,
            "gap_analysis": gap_analysis,
            "development_plan": development_plan,
            "message": "Skill gap analysis completed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== CAREER TRAJECTORY ENDPOINTS =====
@app.route('/api/career/predict', methods=['POST'])
@jwt_required()
def predict_career_trajectory():
    """Predict career trajectory"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        current_role = data.get('current_role')
        target_role = data.get('target_role')
        user_skills = data.get('user_skills', {})
        
        if not current_role or not target_role:
            return jsonify({"error": "Current and target roles are required"}), 400
        
        # Generate career path
        career_path = career_trajectory.generate_career_path(
            current_role, target_role, user_skills
        )
        
        # Predict salary trajectory
        if career_path:
            current_salary = data.get('current_salary', 75000)
            salary_predictions = career_trajectory.predict_salary_trajectory(
                career_path, current_salary
            )
        else:
            salary_predictions = {}
        
        return jsonify({
            "success": True,
            "career_path": career_path.__dict__ if career_path else None,
            "salary_predictions": salary_predictions,
            "message": "Career trajectory predicted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/career/next-roles', methods=['POST'])
@jwt_required()
def predict_next_roles():
    """Predict next best career roles"""
    try:
        data = request.get_json()
        
        current_role = data.get('current_role')
        user_skills = data.get('user_skills', {})
        top_k = data.get('top_k', 3)
        
        if not current_role:
            return jsonify({"error": "Current role is required"}), 400
        
        # Predict next roles
        next_roles = career_trajectory.predict_next_roles(
            current_role, user_skills, top_k
        )
        
        return jsonify({
            "success": True,
            "next_roles": next_roles,
            "message": "Next roles predicted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== SKILL VALIDATION ENDPOINTS =====
@app.route('/api/skills/validate', methods=['POST'])
@jwt_required()
def validate_skills():
    """Validate user skills"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        skill_name = data.get('skill_name')
        claimed_level = data.get('claimed_level')
        claimed_experience = data.get('claimed_experience', 0)
        evidence_urls = data.get('evidence_urls', [])
        
        if not skill_name or not claimed_level:
            return jsonify({"error": "Skill name and claimed level are required"}), 400
        
        # Submit skill claim
        claim_id = skill_validator.submit_skill_claim(
            user_id, skill_name, claimed_level, claimed_experience, evidence_urls
        )
        
        return jsonify({
            "success": True,
            "claim_id": claim_id,
            "message": "Skill validation submitted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/skills/assessment-test', methods=['POST'])
@jwt_required()
def take_assessment_test():
    """Take assessment test for skill validation"""
    try:
        data = request.get_json()
        
        claim_id = data.get('claim_id')
        test_id = data.get('test_id')
        answers = data.get('answers', [])
        
        if not claim_id or not test_id or not answers:
            return jsonify({"error": "Claim ID, test ID, and answers are required"}), 400
        
        # Validate assessment test
        result = skill_validator.validate_assessment_test(claim_id, test_id, answers)
        
        return jsonify({
            "success": True,
            "validation_result": result.__dict__,
            "message": "Assessment test validated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/skills/validation-summary', methods=['GET'])
@jwt_required()
def get_validation_summary():
    """Get skill validation summary for user"""
    try:
        user_id = get_jwt_identity()
        
        # Get validation summary
        summary = skill_validator.get_validation_summary(user_id)
        
        return jsonify({
            "success": True,
            "summary": summary,
            "message": "Validation summary retrieved successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== MARKET ANALYSIS ENDPOINTS =====
@app.route('/api/market/skill-demand', methods=['POST'])
def analyze_skill_demand():
    """Analyze skill demand in market"""
    try:
        data = request.get_json()
        
        skill_name = data.get('skill_name')
        
        if skill_name:
            # Analyze specific skill
            analysis = market_analyzer.get_skill_demand_analysis(skill_name)
        else:
            # Get overall analysis
            analysis = market_analyzer.get_skill_demand_analysis()
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "message": "Skill demand analysis completed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market/regional-insights', methods=['POST'])
def get_regional_insights():
    """Get regional market insights"""
    try:
        data = request.get_json()
        
        region = data.get('region')
        
        # Get regional insights
        insights = market_analyzer.get_regional_market_insights(region)
        
        return jsonify({
            "success": True,
            "insights": insights,
            "message": "Regional insights retrieved successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market/salary-trends', methods=['POST'])
def predict_salary_trends():
    """Predict salary trends for skills"""
    try:
        data = request.get_json()
        
        skill_name = data.get('skill_name')
        months_ahead = data.get('months_ahead', 6)
        
        if not skill_name:
            return jsonify({"error": "Skill name is required"}), 400
        
        # Predict salary trends
        prediction = market_analyzer.predict_salary_trends(skill_name, months_ahead)
        
        return jsonify({
            "success": True,
            "prediction": prediction,
            "message": "Salary trends predicted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market/competition-analysis', methods=['POST'])
def analyze_market_competition():
    """Analyze market competition for skill set"""
    try:
        data = request.get_json()
        
        skill_set = data.get('skill_set', [])
        
        if not skill_set:
            return jsonify({"error": "Skill set is required"}), 400
        
        # Analyze competition
        analysis = market_analyzer.analyze_market_competition(skill_set)
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "message": "Market competition analysis completed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market/comprehensive-report', methods=['POST'])
def generate_market_report():
    """Generate comprehensive market report"""
    try:
        data = request.get_json()
        
        skills = data.get('skills', [])
        region = data.get('region')
        
        if not skills:
            return jsonify({"error": "Skills list is required"}), 400
        
        # Generate comprehensive report
        report = market_analyzer.generate_market_report(skills, region)
        
        return jsonify({
            "success": True,
            "report": report,
            "message": "Market report generated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# END NEW ML MODELS ENDPOINTS
# =========================

# =========================
# SESSION VALIDATION
# =========================
@app.route('/api/auth/validate', methods=['GET'])
@jwt_required()
def validate_session():
    try:
        current_user_id = get_jwt_identity()
        user = users_db.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "valid": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "fullName": user["fullName"],
                "userType": user["userType"]
            }
        })
    except Exception as e:
        return jsonify({"error": "Token validation failed"}), 401

# =========================
# TOKEN REFRESH
# =========================


# =========================
# RUN
# =========================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print("[START] Starting Skills Gap Analysis Server...")
    print(f"Frontend: {os.environ.get('FRONTEND_URL', 'http://localhost:8000')}")
    print(f"API: http://localhost:{port}/api/*")
    print("All services running!")
    app.run(host='0.0.0.0', port=port, debug=True)

# Serve Frontend static files and support React Router catch-all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(BUILD_DIR, path)):
        return send_from_directory(BUILD_DIR, path)
    else:
        return send_from_directory(BUILD_DIR, 'index.html')

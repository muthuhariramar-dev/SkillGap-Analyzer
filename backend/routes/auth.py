from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
import uuid
import datetime

auth_bp = Blueprint('auth', __name__)

# In-memory user database (Consider SQLite for persistence if needed)
# {email: {id, email, password_hash, fullName, userType, ...}}
users_db = {}
# Mapping id -> user for easier lookup
users_by_id = {}

def initialize_users():
    """Initialize users database with default users"""
    if not users_db:
        print("[INFO] Initializing users database...")
        
        # Create test users
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
                'email': 'student@example.com',
                'password': 'password123',
                'fullName': 'Test Student',
                'userType': 'student'
            }
        ]
        
        for user_data in users_to_create:
            if user_data['email'] not in users_db:
                user_id = str(uuid.uuid4())
                hashed_password = generate_password_hash(user_data['password'])
                
                user = {
                    "id": user_id,
                    "email": user_data['email'],
                    "password": hashed_password,
                    "fullName": user_data['fullName'],
                    "userType": user_data['userType'],
                    "createdAt": datetime.datetime.now().isoformat()
                }
                
                users_db[user_data['email']] = user
                users_by_id[user_id] = user
        
        print(f"[INFO] Initialized {len(users_db)} users in database")

# Call initialization
initialize_users()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullName')
    user_type = data.get('userType', 'student') # default
    
    if not email or not password or not full_name:
        return jsonify({"error": "Missing required fields"}), 400
        
    if email in users_db:
        return jsonify({"error": "User already exists"}), 400
        
    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)
    
    user = {
        "id": user_id,
        "email": email,
        "password": hashed_password,
        "fullName": full_name,
        "userType": user_type,
        "createdAt": datetime.datetime.now().isoformat()
    }
    
    users_db[email] = user
    users_by_id[user_id] = user
    
    # Create tokens
    access_token = create_access_token(identity=user_id)
    
    return jsonify({
        "success": True,
        "token": access_token,
        "user": {
            "id": user_id,
            "email": email,
            "fullName": full_name,
            "userType": user_type
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400
        
    user = users_db.get(email)
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401
        
    access_token = create_access_token(identity=user['id'])
    
    return jsonify({
        "success": True,
        "token": access_token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "fullName": user['fullName'],
            "userType": user['userType']
        }
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = users_by_id.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "success": True,
        "data": {
            "id": user['id'],
            "email": user['email'],
            "fullName": user['fullName'],
            "userType": user['userType']
        }
    })

@auth_bp.route('/validate', methods=['GET'])
@jwt_required()
def validate_token():
    """Validate current JWT token"""
    user_id = get_jwt_identity()
    user = users_by_id.get(user_id)
    
    if not user:
        return jsonify({"valid": False, "error": "User not found"}), 404
        
    return jsonify({
        "valid": True,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "fullName": user['fullName'],
            "userType": user['userType']
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({"success": True, "message": "Logged out successfully"})

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "No user ID provided"}), 400
            
        user = users_by_id.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Generate new token
        new_token = create_access_token(identity=user_id)
        
        return jsonify({
            "token": new_token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "fullName": user["fullName"],
                "userType": user["userType"]
            }
        })
    except Exception as e:
        print(f"Token refresh error: {e}")
        return jsonify({"error": "Token refresh failed"}), 500

"""
Authentication routes for user registration, login, and token refresh
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Import after blueprint creation to avoid circular imports
def get_db_and_user():
    from app import db, User
    return db, User

# Input validation
def is_valid_email(email):
    """Check if email format is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    """Check if username is valid (3-20 chars, alphanumeric + underscore)"""
    if not (3 <= len(username) <= 20):
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None

def is_valid_password(password):
    """Check if password meets minimum requirements"""
    return len(password) >= 8

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    from app import db, User
    
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Validation checks
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if not is_valid_username(username):
        return jsonify({'error': 'Username must be 3-20 characters (alphanumeric + underscore only)'}), 400
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    if not is_valid_password(password):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return access + refresh tokens"""
    from app import User
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Find user
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Get new access token using refresh token"""
    from app import User
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info"""
    from app import User
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

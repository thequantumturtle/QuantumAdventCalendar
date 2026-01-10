"""
Quantum Advent Calendar - Backend Server
Main Flask application for challenge serving and solution grading
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///quantum_advent.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # 15 minute access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)    # 7 day refresh token

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define models inline to avoid circular imports
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    submissions = db.relationship('Submission', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        import bcrypt
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Challenge(db.Model):
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    test_code = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, default=1)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    submissions = db.relationship('Submission', backref='challenge', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'title': self.title,
            'description': self.description,
            'starter_code': self.starter_code,
            'difficulty': self.difficulty,
            'created_at': self.created_at.isoformat()
        }

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    test_results = db.Column(db.JSON)  # Store detailed test results
    submitted_at = db.Column(db.DateTime, default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'passed': self.passed,
            'test_results': self.test_results,
            'submitted_at': self.submitted_at.isoformat()
        }

# Import routes (models defined inline to avoid circular imports)
from routes import challenge_bp, submission_bp, leaderboard_bp
from auth import auth_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(challenge_bp)
app.register_blueprint(submission_bp)
app.register_blueprint(leaderboard_bp)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

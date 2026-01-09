"""
Database models for Quantum Advent Calendar
"""

from datetime import datetime

# db will be imported by app.py after initialization
db = None

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='user', lazy=True)
    
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'passed': self.passed,
            'test_results': self.test_results,
            'submitted_at': self.submitted_at.isoformat()
        }

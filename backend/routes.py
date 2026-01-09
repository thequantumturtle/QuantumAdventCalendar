"""
API Routes for Quantum Advent Calendar
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func
import json

# Import models and db from app
from app import db, User, Challenge, Submission
from grader import CodeGrader

# Challenge routes
challenge_bp = Blueprint('challenges', __name__, url_prefix='/api/challenges')

@challenge_bp.route('/', methods=['GET'])
def get_all_challenges():
    """Get all challenges"""
    challenges = Challenge.query.order_by(Challenge.day).all()
    return jsonify([c.to_dict() for c in challenges]), 200

@challenge_bp.route('/<int:day>', methods=['GET'])
def get_challenge(day):
    """Get specific challenge by day"""
    challenge = Challenge.query.filter_by(day=day).first()
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    return jsonify(challenge.to_dict()), 200

# Submission routes
submission_bp = Blueprint('submissions', __name__, url_prefix='/api/submissions')

@submission_bp.route('/', methods=['POST'])
def submit_solution():
    """Submit and grade a solution"""
    data = request.get_json()
    
    # Validate input
    if not data or 'username' not in data or 'day' not in data or 'code' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data['username']
    day = data['day']
    code = data['code']
    
    # Get or create user
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, email=f"{username}@quantum.local")
        db.session.add(user)
        db.session.commit()
    
    # Get challenge
    challenge = Challenge.query.filter_by(day=day).first()
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    # Grade submission
    passed, results = CodeGrader.validate_solution(code, challenge.test_code)
    
    # Save submission
    submission = Submission(
        user_id=user.id,
        challenge_id=challenge.id,
        code=code,
        passed=passed,
        test_results=results
    )
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({
        'submission_id': submission.id,
        'passed': passed,
        'results': results,
        'day': day,
        'username': username
    }), 200

@submission_bp.route('/user/<username>', methods=['GET'])
def get_user_submissions(username):
    """Get all submissions for a user"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    submissions = Submission.query.filter_by(user_id=user.id).all()
    return jsonify([s.to_dict() for s in submissions]), 200

@submission_bp.route('/user/<username>/progress', methods=['GET'])
def get_user_progress(username):
    """Get user's progress across all days"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get completed challenges
    completed = db.session.query(Submission.challenge_id).filter(
        Submission.user_id == user.id,
        Submission.passed == True
    ).distinct().count()
    
    return jsonify({
        'username': username,
        'completed': completed,
        'total': 25,
        'percentage': (completed / 25) * 100
    }), 200

# Leaderboard routes
leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    """Get global leaderboard sorted by completed challenges"""
    # Get top users by completed challenges
    top_users = db.session.query(
        User.username,
        func.count(Submission.id).label('total_submissions'),
        func.sum(func.cast(Submission.passed, db.Integer)).label('completed')
    ).join(Submission).group_by(User.id).order_by(
        func.sum(func.cast(Submission.passed, db.Integer)).desc()
    ).limit(100).all()
    
    leaderboard = []
    for rank, (username, total, completed) in enumerate(top_users, 1):
        leaderboard.append({
            'rank': rank,
            'username': username,
            'completed': completed or 0,
            'total_submissions': total
        })
    
    return jsonify(leaderboard), 200

@leaderboard_bp.route('/by-day/<int:day>', methods=['GET'])
def get_day_leaderboard(day):
    """Get leaderboard for a specific day challenge"""
    # Get users who completed this day, sorted by submission time
    top_users = db.session.query(
        User.username,
        Submission.submitted_at
    ).join(Submission).join(Challenge).filter(
        Challenge.day == day,
        Submission.passed == True
    ).order_by(Submission.submitted_at).limit(100).all()
    
    leaderboard = []
    for rank, (username, submitted_at) in enumerate(top_users, 1):
        leaderboard.append({
            'rank': rank,
            'username': username,
            'submitted_at': submitted_at.isoformat() if submitted_at else None
        })
    
    return jsonify(leaderboard), 200

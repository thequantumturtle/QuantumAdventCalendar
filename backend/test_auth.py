#!/usr/bin/env python
"""Test user creation with JWT auth"""

from app import app, db, User

with app.app_context():
    # Create all tables
    print("Creating tables...")
    db.create_all()
    print("Tables created!")
    
    # Create test user
    user = User(username='testuser', email='test@example.com')
    user.set_password('securepass123')
    db.session.add(user)
    db.session.commit()
    print(f"✓ User created: {user.username} (ID: {user.id})")
    
    # Verify password
    test_user = User.query.filter_by(username='testuser').first()
    if test_user and test_user.check_password('securepass123'):
        print(f"✓ Password verification successful")
    else:
        print(f"✗ Password verification failed")

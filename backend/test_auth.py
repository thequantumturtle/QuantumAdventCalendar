"""Pytest tests for user creation and password hashing.

These tests configure the Flask app to use an in-memory SQLite database
so they run isolated and do not affect the persistent development DB.
"""

import pytest

from app import app, db, User


@pytest.fixture(autouse=True)
def app_context(tmp_path):
    """Provide a Flask app context with an ephemeral SQLite DB for each test."""
    # Use in-memory SQLite for isolation
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


def test_user_creation_and_password():
    user = User(username='testuser', email='test@example.com')
    user.set_password('securepass123')
    db.session.add(user)
    db.session.commit()

    fetched = User.query.filter_by(username='testuser').first()
    assert fetched is not None
    assert fetched.email == 'test@example.com'
    assert fetched.check_password('securepass123')


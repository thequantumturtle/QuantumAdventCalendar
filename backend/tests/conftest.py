"""Pytest configuration and fixtures.

This file ensures tests run against an ephemeral in-memory SQLite database
to avoid interfering with the developer database file. It also provides an
autouse fixture that creates and drops the schema around each test.
"""

import sys
import os
import pytest

# Add backend directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Ensure tests use an ephemeral in-memory database. This must be set before
# importing the Flask app so SQLAlchemy binds to the in-memory URL.
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app, db


@pytest.fixture(autouse=True)
def session_db():
	"""Create and drop database schema around each test for isolation."""
	with app.app_context():
		db.create_all()
		yield
		db.session.remove()
		db.drop_all()

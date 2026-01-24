"""
Seed database with challenges discovered from the `days/` folders.

This script discovers each `days/dayNN_*` folder and reads:
 - `challenge.md` -> description
 - `starter_code.py` or `solution.py` -> starter_code
 - `test.py` -> test_code

It then clears and populates the `challenges` table.
"""

import os
import re
import json
try:
    import yaml
except Exception:
    yaml = None

from app import app, db, Challenge


def discover_challenges(days_root=None):
    """Discover challenges by scanning the `days/` directory.

    Returns a list of dicts matching the Challenge model fields.
    """
    if days_root is None:
        # In the container the backend code is mounted to /app, and days live at /app/days
        days_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'days'))

    challenges = []
    if not os.path.isdir(days_root):
        print(f"Days directory not found: {days_root}")
        return challenges

    for entry in sorted(os.listdir(days_root)):
        entry_path = os.path.join(days_root, entry)
        if not os.path.isdir(entry_path):
            continue

        m = re.match(r'day(\d+)_?(.*)', entry, re.IGNORECASE)
        if not m:
            continue

        day_num = int(m.group(1))

        desc_path = os.path.join(entry_path, 'challenge.md')
        if not os.path.isfile(desc_path):
            # skip folders without a challenge.md
            continue

        with open(desc_path, 'r', encoding='utf-8') as f:
            description = f.read().strip()

        # Title: first Markdown H1 or fallback
        title = None
        for line in description.splitlines():
            line = line.strip()
            if line.startswith('# '):
                title = line.lstrip('# ').strip()
                break
        if not title:
            title = f"Day {day_num}"

        # Read optional metadata from meta.yaml (title, difficulty, tags)
        meta = {}
        meta_path = os.path.join(entry_path, 'meta.yaml')
        if os.path.isfile(meta_path) and yaml is not None:
            try:
                with open(meta_path, 'r', encoding='utf-8') as mf:
                    meta = yaml.safe_load(mf) or {}
            except Exception:
                # ignore metadata parsing errors and continue
                meta = {}

        # Starter code
        starter_code = ''
        for fname in ('starter_code.py', 'solution.py'):
            p = os.path.join(entry_path, fname)
            if os.path.isfile(p):
                with open(p, 'r', encoding='utf-8') as f:
                    starter_code = f.read()
                break

        # Test code
        test_code = ''
        test_path = os.path.join(entry_path, 'test.py')
        if os.path.isfile(test_path):
            with open(test_path, 'r', encoding='utf-8') as f:
                test_code = f.read()

        # Use tags provided in meta.yaml when present; default to empty list
        challenge = {
            'day': day_num,
            'title': meta.get('title') or title,
            'description': description,
            'starter_code': starter_code or meta.get('starter_code') or '"""Starter code not provided."""',
            'test_code': test_code or '',
            'difficulty': int(meta.get('difficulty', 1)),
            'tags': meta.get('tags', []),
        }

        challenges.append(challenge)

    return challenges


def seed_database():
    with app.app_context():
        db.create_all()

        # Clear existing challenges
        Challenge.query.delete()

        challenges = discover_challenges()
        for c in challenges:
            challenge = Challenge(**c)
            db.session.add(challenge)

        db.session.commit()
        print(f"Seeded {len(challenges)} challenges from {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'days'))}")


if __name__ == '__main__':
    seed_database()

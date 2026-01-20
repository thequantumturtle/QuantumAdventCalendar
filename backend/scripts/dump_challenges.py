#!/usr/bin/env python3
import os
import sqlite3
import json

DB_PATHS = [
    os.path.join(os.path.dirname(__file__), '..', 'instance', 'quantum_advent.db'),
    os.path.join(os.path.dirname(__file__), '..', 'quantum_advent.db'),
]

def find_db():
    for p in DB_PATHS:
        p = os.path.abspath(p)
        if os.path.isfile(p):
            return p
    return None

p = find_db()
if not p:
    print('No database file found in expected locations:', DB_PATHS)
    raise SystemExit(1)

conn = sqlite3.connect(p)
conn.row_factory = sqlite3.Row
c = conn.cursor()
rows = c.execute('SELECT * FROM challenges ORDER BY day').fetchall()
result = [dict(r) for r in rows]
print(json.dumps({'db': p, 'count': len(result), 'challenges': result}, indent=2, ensure_ascii=False))
conn.close()

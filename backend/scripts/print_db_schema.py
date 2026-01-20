#!/usr/bin/env python3
import os
import sqlite3

def find_db():
    candidates = [
        os.path.join(os.path.dirname(__file__), '..', 'instance', 'quantum_advent.db'),
        os.path.join(os.path.dirname(__file__), '..', 'quantum_advent.db'),
        os.path.join(os.getcwd(), 'backend', 'instance', 'quantum_advent.db'),
        os.path.join(os.getcwd(), 'backend', 'quantum_advent.db')
    ]
    for p in candidates:
        p = os.path.abspath(p)
        if os.path.isfile(p):
            return p
    return None

p = find_db()
if not p:
    print('No database file found in expected locations.')
    raise SystemExit(1)

print('Using DB file:', p)
conn = sqlite3.connect(p)
c = conn.cursor()
print('\n-- Schema objects --\n')
for row in c.execute("SELECT type, name, sql FROM sqlite_master WHERE type IN ('table','index','trigger') ORDER BY type, name;"):
    typ, name, sql = row
    print(f"-- {typ} {name}\n")
    print(sql or '<no SQL>')
    print()

conn.close()

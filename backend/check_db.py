from app import app, db, User

with app.app_context():
    users = User.query.all()
    print("Users in database:")
    for u in users:
        print(f"  - {u.username} (id: {u.id})")
    if not users:
        print("  (empty)")

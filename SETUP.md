# Development Setup Guide

## Architecture Overview

The Quantum Advent Calendar is a full-stack web application with:

- **Backend**: Python Flask server with SQLAlchemy ORM for data persistence
- **Frontend**: React SPA with Ace editor for code submission
- **Grading Engine**: Qiskit-based code executor with automatic test validation
- **Database**: SQLite for local development, easily swappable for production

## Prerequisites

- Python 3.9+
- Node.js 16+
- pip and npm package managers

## Backend Setup

### 1. Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python seed.py
```

This creates the SQLite database and seeds it with 2 initial challenges.

### 4. Run Backend Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Endpoint

Update `frontend/src/config.js` (create if needed):

```javascript
export const API_URL = 'http://localhost:5000/api';
```

### 3. Run Frontend Dev Server

```bash
npm start
```

App will open on `http://localhost:3000`

### Notes on local CI parity and pre-push checks

The repository enforces a Docker-first pre-push check that runs quick smoke tests and then a frontend production build to mirror CI. You can control the behavior with these environment variables:

- `SKIP_FRONTEND_BUILD=1` — skip the frontend build check for a single push (useful for very fast pushes).
- `CI_FRONTEND_INSTALL=1` — run `npm ci` inside the frontend container before `npm run build` (useful when you want CI-accurate install behavior locally).

Note: if the repository does not contain a `frontend/package-lock.json`, the pre-push hook will fall back to running `npm install` instead of `npm ci`.

Example (PowerShell) to skip the build for one push:

```powershell
$env:SKIP_FRONTEND_BUILD = "1"
git push
```

Example to run CI-accurate install before build in the pre-push hook:

```powershell
$env:CI_FRONTEND_INSTALL = "1"
git push
```

## Testing the Application

### Submit a Challenge

1. Go to `http://localhost:3000`
2. Click "Login" and enter a username
3. Select Day 1: Qubits 101
4. Complete the code in the editor:

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def create_hadamard_circuit():
    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(q, c)
    circuit.h(q[0])
    circuit.measure(q[0], c[0])
    return circuit

def run_circuit():
    simulator = AerSimulator()
    circuit = create_hadamard_circuit()
    result = simulator.run(circuit, shots=1000).result()
    return result.get_counts(circuit)
```

5. Click "Submit Solution"
6. View results and check leaderboard

## API Endpoints

### Challenges

- `GET /api/challenges/` - Get all challenges
- `GET /api/challenges/<day>` - Get specific challenge

### Submissions

- `POST /api/submissions/` - Submit solution
  ```json
  {
    "username": "user123",
    "day": 1,
    "code": "..."
  }
  ```
- `GET /api/submissions/user/<username>` - Get user submissions
- `GET /api/submissions/user/<username>/progress` - Get progress

### Leaderboard

- `GET /api/leaderboard/` - Get global leaderboard
- `GET /api/leaderboard/by-day/<day>` - Get day-specific leaderboard

## Adding New Challenges

Edit `backend/seed.py` and add to `CHALLENGES` array:

```python
{
    'day': 3,
    'title': 'Entanglement',
    'description': '...',
    'starter_code': '...',
    'test_code': '...',
    'difficulty': 2
}
```

Then run: `python seed.py`

## Database Schema

### Users Table
- `id` (PK)
- `username` (unique)
- `email`
- `created_at`

### Challenges Table
- `id` (PK)
- `day` (unique)
- `title`
- `description`
- `starter_code`
- `test_code`
- `difficulty` (1-5)
- `created_at`

### Submissions Table
- `id` (PK)
- `user_id` (FK)
- `challenge_id` (FK)
- `code`
- `passed` (boolean)
- `test_results` (JSON)
- `submitted_at`

## Production Deployment

For production, consider:

1. **Backend**: Deploy Flask app to Heroku, AWS, or similar
   - Use PostgreSQL instead of SQLite
   - Set `FLASK_ENV=production`
   - Use gunicorn for WSGI server

2. **Frontend**: Deploy React build to Vercel, Netlify, or AWS S3
   ```bash
   npm run build
   ```

3. **Database**: Use PostgreSQL or similar managed service

4. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://...
   FLASK_ENV=production
   CORS_ORIGINS=https://yourdomain.com
   ```

## Troubleshooting

### Port Already in Use

- Backend: `python app.py --port 5001`
- Frontend: `PORT=3001 npm start`

### CORS Errors

Ensure Flask-CORS is enabled and frontend API URL matches backend URL

### Qiskit Import Errors

```bash
pip install --upgrade qiskit qiskit-aer
```

## Development Workflow

1. Make changes to backend/frontend
2. Test locally
3. Commit changes: `git add . && git commit -m "description"`
4. Push to GitHub: `git push origin main`
5. Deploy to production

## Next Steps

- [ ] Add Days 3-25 to seed.py
- [ ] Implement user authentication (JWT)
- [ ] Add email verification
- [ ] Create admin dashboard for challenge management
- [ ] Implement real-time collaboration features
- [ ] Add dark mode
- [ ] Mobile app support

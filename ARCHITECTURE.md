# Project Structure

```
QuantumAdventCalendar/
├── backend/                      # Python Flask backend
│   ├── app.py                    # Main Flask application
│   ├── models.py                 # SQLAlchemy database models
│   ├── routes.py                 # API route handlers
│   ├── grader.py                 # Code execution & grading engine
│   ├── seed.py                   # Database seeding script
│   ├── requirements.txt          # Python dependencies
│   └── .gitignore
│
├── frontend/                     # React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Global styles
│   │   ├── components/
│   │   │   └── Navigation.js    # Navigation bar
│   │   ├── pages/
│   │   │   ├── ChallengeList.js    # Challenge grid view
│   │   │   ├── ChallengeEditor.js  # Code editor & submission
│   │   │   ├── Leaderboard.js      # Global rankings
│   │   │   └── UserProgress.js     # User stats
│   │   └── styles/
│   │       ├── Navigation.css
│   │       ├── ChallengeList.css
│   │       ├── ChallengeEditor.css
│   │       ├── Leaderboard.css
│   │       └── UserProgress.css
│   ├── package.json
│   └── .gitignore
│
├── days/                        # Original challenge files
│   └── day01_qubits_101/
│       ├── challenge.md
│       ├── solution.py
│       └── test.py
│
├── README.md                    # Project overview
├── INDEX.md                     # Challenge index
├── SETUP.md                     # Development setup guide
├── ARCHITECTURE.md              # This file
├── requirements.txt             # Root dependencies
└── LICENSE                      # MIT License
```

## Key Components

### Backend

**app.py**: Flask application factory
- Initializes Flask app with CORS
- Sets up SQLAlchemy database
- Registers API blueprints
- Defines error handlers

**models.py**: Database models
- `User`: Stores user accounts
- `Challenge`: Stores challenge definitions
- `Submission`: Stores code submissions and results

**routes.py**: API endpoints
- `/api/challenges/` - Challenge CRUD
- `/api/submissions/` - Submit and grade code
- `/api/leaderboard/` - Rankings and stats

**grader.py**: Code execution engine
- `CodeGrader.execute_code()`: Safely executes user code
- Imports Qiskit libraries
- Captures output and errors
- Returns structured results

**seed.py**: Database initialization
- Defines challenge data
- Creates database tables
- Populates initial challenges

### Frontend

**Navigation.js**: Header component
- Username login/logout
- Navigation links
- Sticky positioning

**ChallengeList.js**: Challenge grid
- Displays all 25 challenges
- Shows difficulty stars
- Links to challenge editor

**ChallengeEditor.js**: Code submission interface
- Ace editor for Python code
- Challenge description panel
- Submit button
- Results display

**Leaderboard.js**: Global rankings
- Top users by completed challenges
- Submission counts
- Rank display

**UserProgress.js**: Personal stats
- Challenges completed
- Progress bar
- Percentage display

## Data Flow

### Challenge Submission Flow

```
1. User writes code in ChallengeEditor
2. User clicks "Submit Solution"
3. Frontend sends POST to /api/submissions/
4. Backend receives submission
5. CodeGrader executes code + tests
6. Results stored in database
7. Response returned to frontend
8. Results displayed in UI
9. Leaderboard updates
```

### User Progress Flow

```
1. User navigates to /progress
2. Frontend GET /api/submissions/user/<username>/progress
3. Backend queries database for completed challenges
4. Returns summary with percentage
5. Frontend renders progress bar
```

## Technology Stack

### Backend
- **Framework**: Flask 2.3.0
- **Database**: SQLAlchemy with SQLite (dev) / PostgreSQL (prod)
- **Grading**: Qiskit 0.43.0+
- **CORS**: flask-cors
- **Environment**: python-dotenv

### Frontend
- **Framework**: React 18.2.0
- **Router**: React Router 6.8.0
- **Editor**: Ace Editor via react-ace
- **HTTP Client**: Axios 1.3.0
- **Styling**: CSS3 with responsive grid

## Security Considerations

### Code Execution
- Runs in isolated Python environment
- No access to filesystem or system commands
- Timeout protection (30 seconds)
- Limited to Qiskit + NumPy imports

### User Data
- No passwords stored (usernames only for MVP)
- Consider JWT auth for production
- CORS enabled for frontend domain
- Input validation on all endpoints

### Database
- SQLite for development (unsafe for production)
- Use PostgreSQL for multi-user deployment
- Connection pooling recommended
- Prepared statements via SQLAlchemy ORM

## Scalability Plan

### Phase 1 (Current)
- SQLite database
- Single server deployment
- 25 challenges

### Phase 2 (Next)
- PostgreSQL database
- Horizontal scaling with load balancer
- Caching layer (Redis)
- Real-time leaderboard updates

### Phase 3 (Advanced)
- Microservices architecture
- Separate grading workers
- Message queue (Celery + RabbitMQ)
- CDN for frontend assets
- WebSocket for real-time updates

## Testing Strategy

### Unit Tests (Backend)
```bash
# Create test_routes.py, test_grader.py, test_models.py
pytest backend/tests/
```

### Integration Tests (Full Stack)
```bash
# Test complete submission flow
pytest backend/tests/test_integration.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
# Cypress or Playwright
npx cypress run
```

## Monitoring & Analytics

Consider adding:
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- User analytics (Mixpanel)
- Challenge completion rates
- Average submission time per day
- Most common errors

## Future Enhancements

1. **Hints System**: Progressive hints for stuck users
2. **Discussion Forum**: Per-challenge discussions
3. **Team Mode**: Collaborative problem solving
4. **Badges/Achievements**: Gamification
5. **API for Integrations**: Export results, certificates
6. **Mobile App**: React Native version
7. **Offline Mode**: Work without internet
8. **Content Management**: Admin UI for adding challenges

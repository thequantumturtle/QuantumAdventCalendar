# Docker Quick Start

Run the entire Quantum Advent Calendar application with Docker!

## Prerequisites

- Docker Desktop installed
- Docker Compose installed

## Start Everything

```bash
# From the project root
docker-compose up --build
```

This will:
- Build and start the Flask backend on `http://localhost:5000`
- Build and start the React frontend on `http://localhost:3000`
- Initialize the database with seed data
- Enable hot-reloading for development

## Access the App

Open your browser and go to:
**http://localhost:3000**

The frontend automatically connects to the backend API at `http://localhost:5000/api`

## Useful Commands

```bash
# Stop all containers
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild without cache
docker-compose up --build --no-cache

# Run command in container
docker-compose exec backend python seed.py
docker-compose exec frontend npm install
```

## Troubleshooting

### Port already in use
If port 3000 or 5000 is already in use, modify `docker-compose.yml`:

```yaml
backend:
  ports:
    - "5001:5000"  # Change host port
frontend:
  ports:
    - "3001:3000"  # Change host port
```

Then update the frontend API URL in the environment variable.

### Database errors
To reset the database, delete `backend/quantum_advent.db` and rebuild:

```bash
docker-compose down
rm backend/quantum_advent.db
docker-compose up --build
```

### Frontend not connecting to backend
Ensure `REACT_APP_API_URL` is set correctly. In Docker, use:
```
http://backend:5000/api  # Inside Docker network
```

For development from host machine, it's:
```
http://localhost:5000/api  # From host browser
```

## Production Build

For a production-ready image:

```bash
# Build optimized frontend
docker build -t quantum-advent-frontend:latest frontend/

# Build production backend
docker build -t quantum-advent-backend:latest backend/

# Push to registry
docker push your-registry/quantum-advent-frontend:latest
docker push your-registry/quantum-advent-backend:latest
```

Then use in production deployment with:
- PostgreSQL instead of SQLite
- HTTPS/SSL certificates
- Environment-specific variables
- Container orchestration (Kubernetes, ECS, etc.)

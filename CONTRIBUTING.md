# Contributing to Quantum Advent Calendar

Thank you for your interest in contributing to the Quantum Advent Calendar! We welcome contributions from developers, educators, and quantum computing enthusiasts.

## Code of Conduct

Please be respectful and inclusive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## How to Contribute

### Reporting Bugs
1. Check [existing issues](https://github.com/thequantumturtle/QuantumAdventCalendar/issues) first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, Node version)

### Suggesting Enhancements
1. Open an issue with label `enhancement`
2. Describe the feature and its benefits
3. Provide examples or mockups if applicable

### Contributing Code

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/thequantumturtle/QuantumAdventCalendar.git
cd QuantumAdventCalendar

# Create a feature branch
git checkout -b feature/your-feature-name

# Follow SETUP.md for local environment setup
```

#### Branch Naming Convention
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test additions

#### Commit Guidelines
- Use clear, descriptive commit messages
- Reference issues: "Fixes #123"
- Format: `type(scope): description`
  - Examples:
    - `feat(grader): add timeout limits`
    - `fix(frontend): resolve ESLint warnings`
    - `docs(readme): update setup instructions`

#### Code Style

**Python**
- Follow PEP 8 standards
- Max line length: 100 characters
- Run `black` for formatting (if available)
- Add type hints where possible

**JavaScript/React**
- Follow ESLint configuration
- Use meaningful variable names
- Add JSDoc comments for components
- Format with Prettier (if available)

#### Testing Requirements

**Backend**
```bash
cd backend
python -m pytest tests/ -v --cov=. --cov-report=html
```

**Frontend**
```bash
cd frontend
npm run build  # Must succeed
npm test       # Run component tests
```

All tests must pass before submitting a PR.

#### Pull Request Process

1. **Create a feature branch** from `main`
2. **Write/update tests** for your changes
3. **Update documentation** if needed
4. **Ensure CI passes** (GitHub Actions workflow)
5. **Submit PR with description** including:
   - What changes were made
   - Why these changes were needed
   - Related issues (use "Fixes #123")
   - Screenshots (if UI changes)
6. **Address review feedback**
7. **Merge after approval**

#### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Related Issues
Fixes #(issue number)

## Testing Done
How was this tested locally?

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

### Adding a New Challenge

To add a challenge (Days 3-25):

1. Create directory: `days/day##_name/`
2. Add files:
   - `challenge.md` - Problem description
   - `solution.py` - Reference solution
   - `test.py` - Unit tests
3. Update `backend/seed.py` with challenge data
4. Test locally: verify solution passes tests
5. Submit PR with challenge content

**Challenge Template:**
```python
"""
Day X: Challenge Title
======================

Challenge Description and background here.

Key Concepts:
- Concept 1
- Concept 2
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def solve_challenge():
    # Your solution here
    pass

if __name__ == "__main__":
    result = solve_challenge()
    print(result)
```

### Documentation Contributions

1. Clone the repository
2. Edit relevant `.md` files
3. Ensure clarity and correctness
4. Submit PR for review

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed project structure.

## Development Commands

```bash
# Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m pytest tests/   # Run tests
python app.py             # Run server

# Frontend
cd frontend
npm start                 # Dev server
npm run build            # Production build
npm test                 # Run tests

# Docker
docker-compose up        # Start all services
docker-compose down      # Stop services
docker-compose build     # Rebuild images
```

## Questions?

- Check [README.md](README.md) and [SETUP.md](SETUP.md)
- Open an issue for clarification
- Start a discussion in the repo

## License

By contributing, you agree your contributions will be licensed under the MIT License.

Thank you for contributing to Quantum Advent Calendar! 🎉

## Local Docker tests & pre-push hook

We run local smoke tests inside Docker to ensure the development environment matches CI and other contributors.

- A Husky pre-push hook is provided which runs a quick Docker-based smoke test before pushing. The hook is strict:
   - **Docker is required** locally. If `docker` is not present in your PATH the hook will block the push and explain how to install Docker.
   - It runs the POSIX script `./scripts/test-local.sh` by default (macOS/Linux/WSL). On Windows the hook will attempt to run PowerShell if available, but Docker is still required.
   - If neither Docker nor PowerShell is available the hook will block the push (strict) and instruct how to install Docker.

- The smoke test performs a minimal check designed to be fast:
   1. Starts containers with `docker-compose up -d --build` (if they are not already running)
   2. Runs a small backend health check (`GET /health` via Flask test client)

Running smoke tests locally (recommended)

PowerShell (Windows):
```powershell
cd c:\Users\djust\Projects\QuantumAdventCalendar
.\scripts\test-local.ps1
```

POSIX (macOS / Linux / WSL):
```bash
cd /path/to/QuantumAdventCalendar
./scripts/test-local.sh
# or use the Makefile shortcut
make test-local
```

One-time local setup for Husky hooks

On a new machine, enable Husky hooks in the repository (frontend dev dependencies are required for some hooks):

```bash
# from repo root
cd frontend
npm install
npx husky install
```

Notes
- The pre-push hook is intentionally light-weight (fast smoke checks). Full test suites and builds are executed in CI.
- If you need to bypass the hook for a specific push, use `git push --no-verify` (use with caution).

If you'd like me to make the pre-push hook stricter (fail when Docker is missing) or optional via a config flag, say so and I will update it.

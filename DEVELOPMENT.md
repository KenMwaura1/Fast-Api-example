# Development Guide

This guide covers setup, development workflow, testing, and contribution guidelines for the Fast API Example project.

## Prerequisites

- Python 3.13+
- PostgreSQL 12+
- Node.js 16+ (for frontend development)
- Docker & Docker Compose (optional, for containerized development)
- Git

## Local Development Setup

### 1. Clone and Setup Python Environment

```bash
# Clone repository
git clone https://github.com/KenMwaura1/Fast-Api-example.git
cd Fast-Api-example

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### 2. Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Local PostgreSQL

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE fast_api_dev;
CREATE USER hello_fastapi WITH PASSWORD 'hello_fastapi';
GRANT ALL PRIVILEGES ON DATABASE fast_api_dev TO hello_fastapi;
EOF
```

#### Option B: Docker PostgreSQL

```bash
# From project root
docker-compose up -d db
```

### 4. Environment Configuration

Copy and configure the environment file:

```bash
cp src/app/.env-example src/app/.env
# Edit src/app/.env with your settings
```

### 5. Run Development Server

```bash
# From project root
./run.sh
```

The API will be available at: http://localhost:8000

Access documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── db.py                # Database configuration
│   ├── .env-example         # Environment variables template
│   └── api/
│       ├── __init__.py
│       ├── models.py        # Pydantic models
│       ├── crud.py          # Database operations
│       ├── notes.py         # Notes endpoints
│       └── ping.py          # Health check endpoint
└── tests/
    ├── conftest.py          # Pytest configuration
    ├── test_ping.py         # Health check tests
    └── test_notes.py        # Notes endpoint tests
```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Edit files in `src/app/`
   - Follow code style guidelines (see below)
   - Add/update tests as needed

3. **Test your changes:**
   ```bash
   pytest src -v
   ```

4. **Run linting:**
   ```bash
   pylint src/app
   ```

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: descriptive message of changes"
   ```

6. **Push and create Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style Guidelines

#### Python (PEP 8)

- Line length: 100 characters (soft limit)
- 4 spaces for indentation
- Imports organized: stdlib, third-party, local
- Use type hints for function parameters and returns

**Good:**
```python
async def get_notes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    completed: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Retrieve notes with optional filtering and pagination."""
    ...
```

**Bad:**
```python
async def get_notes(skip=0, limit=10, search=None, completed=None):
    ...
```

#### Naming Conventions

- Classes: `PascalCase` (e.g., `NoteSchema`)
- Functions/variables: `snake_case` (e.g., `get_notes`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_LIMIT = 100`)
- Private members: prefix with `_` (e.g., `_internal_helper`)

#### Documentation

All functions should have docstrings:

```python
async def create_note(payload: NoteSchema) -> NoteDB:
    """
    Create a new note.
    
    Args:
        payload: Note data from request body
        
    Returns:
        Created note with ID and metadata
        
    Raises:
        HTTPException: If note creation fails
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest src -v

# Run specific test file
pytest src/tests/test_notes.py -v

# Run with coverage
pytest src --cov=src/app --cov-report=html

# Run tests matching pattern
pytest src -k "create_note" -v
```

### Writing Tests

Tests use pytest with mocking. Example:

```python
def test_create_note_success(test_app, monkeypatch):
    """Test successful note creation"""
    test_data = {"title": "Test", "description": "Desc", "completed": False}
    
    async def mock_post(payload):
        return 1
    
    async def mock_get(id):
        return {"id": 1, **test_data, "created_date": "2024-01-01T00:00:00"}
    
    monkeypatch.setattr(crud, "post", mock_post)
    monkeypatch.setattr(crud, "get", mock_get)
    
    response = test_app.post("/notes/", json=test_data)
    assert response.status_code == 201
```

### Test Structure

- **Unit tests**: Test individual functions in `crud.py`
- **Integration tests**: Test endpoints in `test_notes.py` and `test_ping.py`
- **Parametrized tests**: Use `@pytest.mark.parametrize` for testing multiple scenarios

### Test Coverage Goals

- Aim for 80%+ code coverage
- Test all happy paths and error cases
- Test validation and edge cases

## Adding New Features

### 1. Update Models (if needed)

Edit `src/app/api/models.py`:

```python
class NoteSchema(NoteBase):
    """Schema for creating/updating notes"""
    tags: List[str] = Field(default_factory=list, description="Note tags")
```

### 2. Update CRUD Operations

Edit `src/app/api/crud.py`:

```python
async def get_notes_by_tag(tag: str) -> List[Dict[str, Any]]:
    """Retrieve notes filtered by tag"""
    ...
```

### 3. Add/Update Endpoints

Edit `src/app/api/notes.py`:

```python
@router.get("/tags/{tag}")
async def get_notes_by_tag(tag: str = Path(...)):
    """Get notes with specific tag"""
    ...
```

### 4. Add Tests

Edit `src/tests/test_notes.py`:

```python
def test_get_notes_by_tag(test_app, monkeypatch):
    """Test retrieving notes by tag"""
    ...
```

### 5. Update Documentation

Update `API.md` with new endpoint documentation.

## Docker Development

### Building Docker Image

```bash
# Build image
docker build -t fast-api-example:latest ./src

# Run container
docker run -p 8002:8000 --env-file src/app/.env fast-api-example:latest
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Debugging

### Enable Debug Mode

Set in `.env`:
```env
ENVIRONMENT=development
```

### Print Debugging

```python
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Variable value: {variable}")
```

### Using Breakpoints

For VS Code debugging, add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/src"
    }
  ]
}
```

## Database Migrations

Currently, the project uses SQLAlchemy's `metadata.create_all()` for schema creation. For production with migrations:

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Performance Optimization

### Pagination Limits

The API enforces a maximum limit of 100 items per page to prevent performance issues.

### Database Indexes

Consider adding indexes to frequently queried fields:

```python
Column("title", String(255), index=True)
```

### Caching

For future optimization, consider adding Redis caching:

```bash
pip install redis aioredis
```

## Common Issues

### Issue: "Database connection refused"

**Solution:**
1. Verify PostgreSQL is running: `sudo systemctl status postgresql`
2. Check connection string in `.env`
3. Verify database exists: `psql -U hello_fastapi -l`

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:**
Ensure `PYTHONPATH` is set:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
PORT=8001 ./run.sh
```

## Version Control Conventions

### Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: fix a bug
docs: update documentation
test: add/update tests
refactor: refactor code
style: formatting changes
chore: dependencies, build changes
```

### Branch Naming

```
feature/description-of-feature
bugfix/description-of-bug
docs/description-of-docs
refactor/description-of-refactor
```

## Useful Commands

```bash
# Check code with pylint
pylint src/app

# Check code formatting
black --check src/app

# Format code automatically
black src/app

# Check imports
isort src/app --check-only

# Sort imports automatically
isort src/app

# Run type checking
mypy src/app

# Clean up __pycache__
find . -type d -name __pycache__ -exec rm -r {} +
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [PEP 8 Style Guide](https://pep8.org/)

## Getting Help

- Check existing issues on GitHub
- Review the API documentation in `API.md`
- Check test examples in `src/tests/`
- Open an issue or discussion on GitHub

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

# Quick Reference Guide

Fast lookup for common tasks and commands.

## Installation

```bash
# Clone repository
git clone https://github.com/KenMwaura1/Fast-Api-example.git
cd Fast-Api-example

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
cd src
pip install -r requirements.txt
```

## Running the Application

### Local Development

```bash
# From project root
./run.sh

# With custom port
PORT=8001 ./run.sh

# Access:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Docker

```bash
# Start all services
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Reset database
docker-compose down -v && docker-compose up -d --build
```

## Database

### Create Local Database

```bash
# PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE fast_api_dev;
CREATE USER hello_fastapi WITH PASSWORD 'hello_fastapi';
GRANT ALL PRIVILEGES ON DATABASE fast_api_dev TO hello_fastapi;
EOF

# Verify
psql -U hello_fastapi -d fast_api_dev -c "SELECT 1"
```

### Using Docker Database

```bash
docker-compose exec db psql -U hello_fastapi -d fast_api_dev
```

## Testing

```bash
# Run all tests
pytest src -v

# Run specific test file
pytest src/tests/test_notes.py -v

# Run specific test
pytest src/tests/test_notes.py::TestCreateNote::test_create_note_success -v

# Run with coverage
pytest src --cov=src/app --cov-report=html

# Run tests matching pattern
pytest src -k "create" -v
```

## API Requests

### Using curl

```bash
# Create note
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "description": "Note content"}'

# List notes
curl http://localhost:8000/notes

# Get single note
curl http://localhost:8000/notes/1

# Search
curl "http://localhost:8000/notes?search=api"

# Filter by completion
curl "http://localhost:8000/notes?completed=true"

# Pagination
curl "http://localhost:8000/notes?skip=0&limit=5"

# Update note
curl -X PUT http://localhost:8000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated", "description": "Updated content", "completed": true}'

# Delete note
curl -X DELETE http://localhost:8000/notes/1

# Health check
curl http://localhost:8000/ping
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create
response = requests.post(
    f"{BASE_URL}/notes",
    json={"title": "Note", "description": "Content"}
)
note_id = response.json()["id"]

# Read
response = requests.get(f"{BASE_URL}/notes/{note_id}")
print(response.json())

# Search
response = requests.get(f"{BASE_URL}/notes", params={"search": "api"})
print(response.json())

# Update
response = requests.put(
    f"{BASE_URL}/notes/{note_id}",
    json={"title": "Updated", "description": "New content", "completed": True}
)

# Delete
response = requests.delete(f"{BASE_URL}/notes/{note_id}")

# Health check
response = requests.get(f"{BASE_URL}/ping")
print(response.json())
```

## Code Quality

```bash
# Lint code
pylint src/app

# Check formatting
black --check src/app

# Format code
black src/app

# Sort imports
isort src/app

# Type checking
mypy src/app
```

## Project Structure

```
src/
├── app/
│   ├── main.py           # FastAPI app
│   ├── db.py             # Database config
│   ├── .env-example      # Env template
│   └── api/
│       ├── models.py     # Pydantic models
│       ├── crud.py       # DB operations
│       ├── notes.py      # Notes endpoints
│       └── ping.py       # Health endpoint
└── tests/
    ├── conftest.py       # Test config
    ├── test_notes.py     # Notes tests
    └── test_ping.py      # Health tests

Documentation/
├── README.md             # Project overview
├── API.md                # API reference
├── DEVELOPMENT.md        # Dev guide
├── CONTRIBUTING.md       # Contribution guide
├── QUICK_REFERENCE.md    # This file
```

## Environment Variables

```bash
# src/app/.env
DATABASE_URL=postgresql://user:pass@host/db
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost,http://localhost:5173
```

## Key Files to Edit

| File | Purpose |
|------|---------|
| `src/app/main.py` | FastAPI app initialization |
| `src/app/db.py` | Database config & schema |
| `src/app/api/models.py` | Data models & validation |
| `src/app/api/crud.py` | Database operations |
| `src/app/api/notes.py` | Note endpoints |
| `src/app/api/ping.py` | Health endpoint |
| `src/tests/test_notes.py` | Note tests |

## Common Workflows

### Add a New Endpoint

1. **Add to models.py** if needed:
   ```python
   class NewModel(BaseModel):
       field: str
   ```

2. **Add to crud.py**:
   ```python
   async def new_function():
       """Implementation"""
   ```

3. **Add to notes.py**:
   ```python
   @router.get("/new-endpoint")
   async def new_endpoint():
       """Documentation"""
       return await crud.new_function()
   ```

4. **Add tests** in test_notes.py:
   ```python
   def test_new_endpoint(test_app, monkeypatch):
       """Test the new endpoint"""
   ```

5. **Update API.md** with documentation

### Debug an Issue

```bash
# Check logs
docker-compose logs web

# Test endpoint
curl -v http://localhost:8000/notes/1

# Run specific test
pytest src/tests/test_notes.py::test_specific -v -s

# Check database
docker-compose exec db psql -U hello_fastapi -d fast_api_dev
```

### Deploy Changes

1. Test locally:
   ```bash
   pytest src -v
   ./run.sh  # Verify API works
   ```

2. Commit changes:
   ```bash
   git add .
   git commit -m "feat: description"
   ```

3. Push to GitHub:
   ```bash
   git push origin feature/name
   ```

4. Create Pull Request on GitHub

## Useful Links

- [API Documentation](API.md)
- [Development Guide](DEVELOPMENT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## Ports

| Service | Port | URL |
|---------|------|-----|
| FastAPI | 8000 | http://localhost:8000 |
| FastAPI (Docker) | 8002 | http://localhost:8002 |
| PostgreSQL | 5432 | localhost:5432 |
| Vue Frontend | 5173 | http://localhost:5173 |

## Shortcuts

```bash
# One-liner to test everything
pytest src -v && ./run.sh

# Run tests with coverage
pytest src --cov=src/app --cov-report=html && open htmlcov/index.html

# Format and lint
black src/app && isort src/app && pylint src/app

# Docker quick start
docker-compose down -v && docker-compose up -d --build && sleep 5 && curl http://localhost:8002/docs
```

## Troubleshooting Quick Links

- **Port in use**: See [Troubleshooting - Port Already in Use](README.md#port-already-in-use)
- **DB connection**: See [Troubleshooting - Database Connection Issues](README.md#database-connection-issues)
- **Docker issues**: See [Troubleshooting - Docker Issues](README.md#docker-issues)
- **Installation fails**: See [Troubleshooting - Installation Issues](README.md#installation-issues)

## Getting Help

- 📖 Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup
- 📝 Read [API.md](API.md) for API reference
- 🤝 Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 💬 Open an issue on GitHub
- 🔗 Check existing issues for solutions

---

**Last Updated:** January 2026

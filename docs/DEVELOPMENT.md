# Development Guide

This guide covers setup, development workflow, and testing for the project.

## Prerequisites

- Python 3.13+
- PostgreSQL 14+
- Node.js 22+
- Docker & Docker Compose

## Local Setup

1. **Clone and Setup Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r src/requirements.txt

   # Optional: install development tools (linters, test runners)
   pip install -r src/dev-requirements.txt
   ```

2. **Database Migrations**
   The project uses Alembic for database migrations.
   ```bash
   cd src
   # Apply migrations to database
   alembic upgrade head
   
   # Create a new migration after model changes
   alembic revision --autogenerate -m "description"
   ```

3. **Environment Configuration**
   Copy `src/app/.env-example` to `src/.env` and adjust as needed.

4. **Run Development Server**
   ```bash
   ./run.sh
   ```

## Testing

Run tests using pytest:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest src -v
```

## Linting & Formatting

We use `ruff` for code quality:
```bash
# Check for issues
ruff check .

# Format code
ruff format .
```

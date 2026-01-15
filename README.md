# FastAPI Example App

![fastapi-0.115.8](https://img.shields.io/badge/fastapi-0.115.8-009688?logo=fastapi&logoColor=white) ![python-3.13](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white) [![CodeQL](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml) [![Docker Compose Actions Workflow](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kenmwaura1)
[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label=Follow&on)](https://twitter.com/Ken_Mwaura1)

A production-ready asynchronous REST API built with [FastAPI](https://fastapi.tiangolo.com/), featuring CRUD operations for notes management. The API includes advanced features like search, filtering, pagination, and is fully containerized with Docker.

## ✨ Features

- 🚀 **Asynchronous API** - Built with FastAPI and async/await patterns
- 🐘 **PostgreSQL Database** - Production-grade database with asyncpg driver
- 🔍 **Search & Filter** - Unified search with pagination support
- 📝 **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- 🐳 **Docker Support** - Fully containerized with Docker Compose
- 🧪 **Testing** - Comprehensive test suite with pytest
- 📚 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- 🎨 **Vue Frontend** - Optional modern frontend with Vite

![Fast-api](images/fast-api-scrnsht-1.png)

## 📖 Table of Contents

- [Quick Start](#-quick-start-with-docker)
- [Local Installation](#-local-installation)
- [Vue Frontend](#-vue-frontend-optional)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start with Docker

The fastest way to get started is using Docker Compose:

### Prerequisites

- [Docker](https://docs.docker.com/install/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/KenMwaura1/Fast-Api-example.git
   cd Fast-Api-example
   ```

2. **Start the application**

   ```bash
   docker-compose up -d --build
   ```

3. **Access the API**
   - API: <http://localhost:8002/notes>
   - Swagger Docs: <http://localhost:8002/docs>
   - ReDoc: <http://localhost:8002/redoc>

> **Note**: If you've previously run Docker Compose, reset the database volume: `docker-compose down -v && docker-compose up -d --build`

## 💻 Local Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 12+
- pip or uv package manager

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/KenMwaura1/Fast-Api-example.git
   cd Fast-Api-example
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   .\venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. **Configure database**

   Create a PostgreSQL database:

   ```sql
   CREATE DATABASE fast_api_dev;
   CREATE USER hello_fastapi WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE fast_api_dev TO hello_fastapi;
   ```

   Or update the `DATABASE_URL` in `src/app/.env`:

   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

5. **Run the application**

   ```bash
   cd ..
   ./run.sh
   ```

6. **Access the API**
   - API: <http://localhost:8002/notes>
   - Swagger Docs: <http://localhost:8002/docs>

## 🎨 Vue Frontend (Optional)

A modern Vue 3 frontend built with Vite is included for testing the API.

### Prerequisites

- Node.js 16+ or 18+ (LTS recommended)
- npm or yarn

### Setup

1. **Navigate to frontend directory**

   ```bash
   cd vue-client
   ```

2. **Install dependencies**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Access the frontend**
   - Frontend: <http://localhost:5173>

The frontend displays notes with their completion status and formatted creation dates.

## 📡 API Endpoints

### Notes

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| GET | `/notes` | List all notes | `skip`, `limit`, `search`, `completed` |
| POST | `/notes` | Create a note | - |
| GET | `/notes/{id}` | Get a note | - |
| PUT | `/notes/{id}` | Update a note | - |
| DELETE | `/notes/{id}` | Delete a note | - |

### Ping

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ping` | Health check |

### Example Request

```bash
# Get all completed notes with pagination
curl "http://localhost:8002/notes?completed=true&skip=0&limit=10"

# Search notes
curl "http://localhost:8002/notes?search=fastapi"

## 🧪 Testing

The project includes a comprehensive test suite using pytest with database mocking.

### Run Tests

```bash
# From the project root
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
./venv/bin/python -m pytest src

# With coverage
./venv/bin/python -m pytest src --cov=src --cov-report=html

# Run specific test file
./venv/bin/python -m pytest src/tests/test_notes.py
```

### Test Structure

- `tests/test_ping.py` - Health check endpoint tests
- `tests/test_notes.py` - CRUD operations and filtering tests
- `tests/conftest.py` - Shared fixtures and test configuration

## 📚 Documentation

### API Documentation

- **Swagger UI**: <http://localhost:8002/docs> (Interactive API documentation)
- **ReDoc**: <http://localhost:8002/redoc> (Alternative documentation view)

### Tech Stack

- **Framework**: FastAPI 0.115.8
- **Python**: 3.13
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy 1.4.50
- **Server**: Uvicorn with uvloop
- **Testing**: pytest 7.4.3
- **Frontend**: Vue 3 + Vite

## 🛠️ Development

### Project Structure

```
Fast-Api-example/
├── src/
│   ├── app/
│   │   ├── api/          # API routes
│   │   │   ├── notes.py  # Notes endpoints
│   │   │   ├── ping.py   # Health check
│   │   │   ├── crud.py   # Database operations
│   │   │   └── models.py # Pydantic models
│   │   ├── db.py         # Database configuration
│   │   └── main.py       # Application entry point
│   ├── tests/            # Test suite
│   ├── Dockerfile        # Docker configuration
│   └── requirements.txt  # Python dependencies
├── vue-client/           # Vue frontend
├── docker-compose.yml    # Docker Compose config
└── run.sh               # Local run script
```

### Environment Variables

Create a `.env` file in `src/app/`:

```env
DATABASE_URL=postgresql://hello_fastapi:password@localhost/fast_api_dev
ENVIRONMENT=development
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🚢 CI/CD & Deployment

### GitHub Actions

The project uses GitHub Actions for CI/CD with two main workflows:

- **CodeQL Analysis** - Security scanning and code quality checks
- **Docker Build & Push** - Automated Docker image builds

### Docker Hub

Pre-built Docker images are available at:

- [Docker Hub](https://hub.docker.com/repository/docker/kenmwaura1/fast-api-example)
- [GitHub Packages](https://github.com/KenMwaura1/Fast-Api-example/pkgs/container/fast-api-example)

### Required Secrets

To use GitHub Actions, add these secrets to your repository:

**For Docker Hub:**

- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

**For GitHub Packages:**

- `CR_PAT` - Personal Access Token with `write:packages` scope
- `CR_USERNAME` - Your GitHub username

> **Note**: You can remove or comment out the Docker push steps if you don't need image publishing.

### Pull Pre-built Image

```bash
docker pull kenmwaura1/fast-api-example:latest
```

## 📖 Resources

- [Official Tutorial](https://dev.to/ken_mwaura1/getting-started-with-fast-api-and-docker-515) - Complete step-by-step guide
- [API Documentation](API.md) - Comprehensive API endpoint reference
- [Development Guide](DEVELOPMENT.md) - Setup and development workflow
- [Contributing Guide](CONTRIBUTING.md) - Guidelines for contributing
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

## 🐛 Troubleshooting

### Installation Issues

#### Python Package Installation Fails

If you encounter errors installing packages (especially `pydantic-core` or `greenlet`):

1. **Ensure you have Python 3.13 or 3.12** (not 3.14+, which has compatibility issues)
   ```bash
   python --version
   ```

2. **Install build dependencies** (Linux/Mac):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
   
   # Mac
   brew install build-essential openssl
   ```

3. **Upgrade pip, setuptools, and wheel**:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

### Database Connection Issues

#### "Connection refused" when starting the app

1. **Verify PostgreSQL is running**:
   ```bash
   # Check status
   sudo systemctl status postgresql
   
   # Start if not running
   sudo systemctl start postgresql
   ```

2. **Verify credentials in `.env`**:
   ```bash
   # Check database exists
   psql -U hello_fastapi -d fast_api_dev -c "SELECT 1"
   ```

3. **Check database connection string**:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

#### Using Docker database

If using Docker Compose:
```bash
# Check if database container is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Port Already in Use

#### Port 8000 or 8002 already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
PORT=8001 ./run.sh
```

### Docker Issues

#### Docker build fails

1. **Ensure you're using Python 3.13**:
   - Check `src/Dockerfile` line 2

2. **Clear Docker cache**:
   ```bash
   docker system prune -a
   docker-compose down -v
   ```

3. **Rebuild**:
   ```bash
   docker-compose up -d --build
   ```

#### Container exits immediately

```bash
# Check container logs
docker-compose logs web

# Or for specific container
docker logs <container_id>
```

### API Issues

#### 404 Not Found on `/docs`

The API might not be running at the expected URL:
- Verify the port: Check `./run.sh` for PORT setting
- Verify the host: Usually `http://localhost:8000`
- Check that the API actually started without errors

#### 422 Validation Error

Usually means your request data doesn't match expected format:
- Check field lengths: title (3-255), description (3-1000)
- Ensure required fields are included
- Verify JSON format is correct

#### 500 Internal Server Error

Check the application logs:
```bash
# For local development
# Errors should show in the terminal where you ran ./run.sh

# For Docker
docker-compose logs web
```

### Testing Issues

#### Tests fail with "ModuleNotFoundError"

```bash
# Set PYTHONPATH correctly
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest src -v
```

#### Database-related test failures

Tests use mocked database, so this usually means the test fixture isn't working:

```bash
# Check conftest.py exists
cat src/tests/conftest.py

# Run with verbose output
pytest src -v -s
```

### Performance Issues

#### Slow API responses

1. **Check database performance**:
   ```sql
   -- Log in to database
   psql -U hello_fastapi -d fast_api_dev
   
   -- Check table size
   SELECT pg_size_pretty(pg_total_relation_size('notes'));
   ```

2. **Check query logs** (if enabled)

3. **Verify indexes exist** on frequently queried columns

#### High memory usage

- Reduce `limit` parameter in queries (max is 100)
- Check for memory leaks in custom code
- Monitor using `docker stats` (for Docker deployment)

### Frontend Issues

#### Vue frontend can't connect to API

1. **Verify API is running**:
   ```bash
   curl http://localhost:8000/ping
   ```

2. **Check CORS configuration** in `.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:5173,http://localhost
   ```

3. **Check frontend URL** in browser matches one of allowed origins

### Still Having Issues?

1. **Check the documentation**:
   - [API.md](API.md) - API reference
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide

2. **Search existing issues**:
   - [GitHub Issues](https://github.com/KenMwaura1/Fast-Api-example/issues)

3. **Open a new issue** with:
   - Clear description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Environment details (OS, Python version, etc.)

4. **Ask for help**:
   - GitHub Discussions
   - Stack Overflow (tag with `fastapi`, `postgresql`)

## 📝 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

## 👤 Author

**Kennedy Mwaura**

- Twitter: [@Ken_Mwaura1](https://twitter.com/Ken_Mwaura1)
- GitHub: [@KenMwaura1](https://github.com/KenMwaura1)

## ☕ Support

If you find this project helpful, consider:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kenmwaura1)

---

**Built with ❤️ using FastAPI**

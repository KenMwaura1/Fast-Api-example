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
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

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

# FastAPI Example App

![fastapi-0.135.3](https://img.shields.io/badge/fastapi-0.135.3-009688?logo=fastapi&logoColor=white) ![python-3.13](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white) [![CodeQL](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml) [![Docker Compose Actions Workflow](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kenmwaura1)
[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label=Follow&on)](https://twitter.com/Ken_Mwaura1)

A production-ready asynchronous REST API built with [FastAPI](https://fastapi.tiangolo.com/), featuring secure user authentication and advanced notes management. The application uses modern patterns like native SQLAlchemy 2.0 Async, Pydantic 2 settings, and is fully containerized.

## ✨ Features

- 🚀 **Asynchronous API** - Built with FastAPI 0.135.3 and async/await patterns
- 🔐 **Secure Authentication** - JWT-based OAuth2 Password Grant flow
- 🐘 **PostgreSQL Database** - Native SQLAlchemy 2.0 Async with asyncpg
- 📦 **Database Migrations** - Managed by Alembic
- 🔍 **Search & Filter** - Support for text search, completion status, and tags
- 🏷️ **Tags Support** - Organize notes with flexible tagging
- 🗑️ **Soft Deletes** - Recoverable data management
- 🐳 **Docker Support** - Fully containerized backend and frontend
- 🧪 **Testing** - Comprehensive test suite with pytest and mock dependencies
- 🎨 **Vue 3 Frontend** - Modern frontend with Vite and Pinia state management

![Fast-api](images/fast-api-scrnsht-1.png)

## 📖 Table of Contents

- [Quick Start with Docker](#-quick-start-with-docker)
- [Local Installation](#-local-installation)
- [Vue Frontend](#-vue-frontend)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
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

3. **Access the Application**
   - Frontend: <http://localhost:5173>
   - API Docs (Swagger): <http://localhost:8002/docs>
   - API Backend: <http://localhost:8002>

## 💻 Local Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 14+
- Node.js 18+

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/KenMwaura1/Fast-Api-example.git
   cd Fast-Api-example
   ```

2. **Backend Setup**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   cd src
   pip install -r requirements.txt
   ```

### Build Docker image (manual)

If you prefer to build the backend image directly (the Dockerfile lives in `src`), run from the repository root:

```bash
# build using the `src` folder as the build context
docker build -f src/Dockerfile -t fast-api-example:local src

# run the built image
docker run --rm -p 8000:8000 --env-file src/.env fast-api-example:local
```

This `docker build` command sets the build context to `src` so the `COPY requirements.txt` in the Dockerfile resolves correctly.

3. **Database Configuration**
   Configure your DATABASE_URL in `src/.env` (copy from `src/app/.env-example`):
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ```

4. **Run Migrations**
   ```bash
   cd src
   alembic upgrade head
   ```

5. **Run the Application**
   ```bash
   ./run.sh
   ```

## 🎨 Vue Frontend

A modern Vue 3 frontend built with Vite and Pinia is included.

### Setup

1. **Navigate to frontend directory**
   ```bash
   cd vue-client
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Access the frontend** at <http://localhost:5173>

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/token` | Login to get access token |

### Notes (Requires Auth)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes/` | List notes (owned by user) |
| POST | `/notes/` | Create a note |
| GET | `/notes/{id}` | Get specific note |
| PUT | `/notes/{id}` | Update note |
| DELETE | `/notes/{id}` | Soft delete note |

## 🧪 Testing

The project includes a comprehensive test suite using pytest with mocked database dependencies.

```bash
# From the project root
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest src -v
```

## 🛠️ Project Structure

```
Fast-Api-example/
├── src/
│   ├── app/
│   │   ├── api/          # API routes & logic
│   │   │   ├── auth.py   # Auth endpoints
│   │   │   ├── notes.py  # Notes endpoints
│   │   │   ├── crud.py   # DB operations
│   │   │   └── models.py # Pydantic models
│   │   ├── config.py     # Pydantic Settings
│   │   ├── db.py         # SQLAlchemy Setup
│   │   └── main.py       # FastAPI Entry
│   ├── migrations/       # Alembic migrations
│   └── tests/            # Test suite
├── vue-client/           # Vue 3 frontend
└── docker-compose.yml    # Docker orchestration
```

## 🐛 Troubleshooting

### Database Migrations
If you see "relation 'notes' already exists", ensure you have run `alembic upgrade head` rather than relying on `create_all`.

### Connection Refused
If the backend can't connect to the DB in Docker, verify the `DATABASE_URL` uses `db` as the hostname: `postgresql+asyncpg://user:pass@db/dbname`.

### Frontend API URL
Ensure `VITE_API_URL` in `vue-client/.env.development` points to the correct backend port (8002 for Docker, 8000 for local).

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 👤 Author

**Kennedy Mwaura**
- Twitter: [@Ken_Mwaura1](https://twitter.com/Ken_Mwaura1)
- GitHub: [@KenMwaura1](https://github.com/KenMwaura1)

---
**Built with ❤️ using FastAPI and Vue.js**

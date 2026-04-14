# Notes API Documentation

Complete reference for the Notes API endpoints.

## Base URL

- **Local (run.sh):** `http://localhost:8000`
- **Docker Compose:** `http://localhost:8002`

## Authentication

The API uses OAuth2 with Password Grant and JWT tokens. Most endpoints require a valid access token.

### Get Access Token

#### `POST /auth/token`

Exchange username and password for a JWT access token.

**Request (Form Data):**

- `username`: your_username
- `password`: your_password

**Response:**

```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### Registration

#### `POST /auth/register`

Create a new user account.

**Request Body:**

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

---

## Response Format

All responses are in JSON format.

### Success Response (Note)

```json
{
  "id": 1,
  "title": "Sample Note",
  "description": "This is a sample note",
  "completed": false,
  "tags": ["work", "important"],
  "owner_id": 1,
  "is_deleted": false,
  "created_date": "2024-01-15T10:30:00"
}
```

---

## Endpoints

### Health Check

#### `GET /ping`

Public health check endpoint.

---

### Notes

All notes endpoints require the header: `Authorization: Bearer <token>`

#### `POST /notes/`

Create a new note for the current user.

#### `GET /notes/`

Retrieve current user's notes with filtering and pagination.

- `skip`, `limit`: Pagination
- `search`: Search title/description
- `completed`: Filter by status
- `tag`: Filter by specific tag

#### `GET /notes/{id}`

Retrieve a specific note owned by the user.

#### `PUT /notes/{id}`

Update a specific note owned by the user.

#### `DELETE /notes/{id}`

Soft delete a specific note owned by the user.

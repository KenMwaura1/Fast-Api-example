# Notes API Documentation

Complete reference for the Notes API endpoints.

## Base URL

```
http://localhost:8002
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "id": 1,
  "title": "Sample Note",
  "description": "This is a sample note",
  "completed": false,
  "created_date": "2024-01-15T10:30:00.123456"
}
```

### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Endpoints

### Health Check

#### `GET /ping`

Health check endpoint to verify API and database connectivity.

**Response:**

- **Status:** `200 OK`

```json
{
  "status": "healthy",
  "message": "API and database are operational"
}
```

**Example:**

```bash
curl http://localhost:8002/ping
```

---

### Notes

#### `POST /notes`

Create a new note.

**Request Body:**

```json
{
  "title": "My First Note",
  "description": "This is a test note",
  "completed": false
}
```

**Field Constraints:**

- `title` (string, required): 3-255 characters
- `description` (string, required): 3-1000 characters
- `completed` (boolean, optional): Default is `false`

**Response:**

- **Status:** `201 Created`

```json
{
  "id": 1,
  "title": "My First Note",
  "description": "This is a test note",
  "completed": false,
  "created_date": "2024-01-15T10:30:00.123456"
}
```

**Error Responses:**

- `422 Unprocessable Entity` - Invalid input (validation error)

**Example:**

```bash
curl -X POST http://localhost:8002/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "description": "This is a test note"
  }'
```

---

#### `GET /notes`

Retrieve notes with optional filtering, searching, and pagination.

**Query Parameters:**

- `skip` (integer, optional, default: 0): Number of items to skip. Must be >= 0.
- `limit` (integer, optional, default: 10): Maximum items per page. Must be between 1 and 100.
- `search` (string, optional): Search term for title and description. Max 100 characters.
- `completed` (boolean, optional): Filter by completion status (true/false).

**Response:**

- **Status:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "First Note",
    "description": "Description",
    "completed": false,
    "created_date": "2024-01-15T10:30:00.123456"
  },
  {
    "id": 2,
    "title": "Second Note",
    "description": "Another description",
    "completed": true,
    "created_date": "2024-01-16T14:25:00.123456"
  }
]
```

**Examples:**

Get all notes with default pagination:

```bash
curl http://localhost:8002/notes
```

Get only completed notes:

```bash
curl "http://localhost:8002/notes?completed=true"
```

Search for notes:

```bash
curl "http://localhost:8002/notes?search=api"
```

Combine filters with pagination:

```bash
curl "http://localhost:8002/notes?completed=true&search=work&skip=0&limit=5"
```

---

#### `GET /notes/{id}`

Retrieve a specific note by ID.

**Path Parameters:**

- `id` (integer, required): Note ID. Must be > 0.

**Response:**

- **Status:** `200 OK`

```json
{
  "id": 1,
  "title": "Sample Note",
  "description": "Note description",
  "completed": false,
  "created_date": "2024-01-15T10:30:00.123456"
}
```

**Error Responses:**

- `404 Not Found` - Note with specified ID not found
- `422 Unprocessable Entity` - Invalid ID format

**Example:**

```bash
curl http://localhost:8002/notes/1
```

---

#### `PUT /notes/{id}`

Update an existing note.

**Path Parameters:**

- `id` (integer, required): Note ID. Must be > 0.

**Request Body:**

```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true
}
```

**Field Constraints:** (Same as POST)

- `title` (string, required): 3-255 characters
- `description` (string, required): 3-1000 characters
- `completed` (boolean, optional): Default is `false`

**Response:**

- **Status:** `200 OK`

```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true,
  "created_date": "2024-01-15T10:30:00.123456"
}
```

**Error Responses:**

- `404 Not Found` - Note with specified ID not found
- `422 Unprocessable Entity` - Invalid ID format or invalid input data

**Example:**

```bash
curl -X PUT http://localhost:8002/notes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "description": "Updated description",
    "completed": true
  }'
```

---

#### `DELETE /notes/{id}`

Delete a note.

**Path Parameters:**

- `id` (integer, required): Note ID. Must be > 0.

**Response:**

- **Status:** `200 OK`

Returns the deleted note:

```json
{
  "id": 1,
  "title": "Deleted Note",
  "description": "Note description",
  "completed": false,
  "created_date": "2024-01-15T10:30:00.123456"
}
```

**Error Responses:**

- `404 Not Found` - Note with specified ID not found
- `422 Unprocessable Entity` - Invalid ID format

**Example:**

```bash
curl -X DELETE http://localhost:8002/notes/1
```

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Request failed due to server error |
| 404 | Not Found | Requested resource not found |
| 422 | Unprocessable Entity | Request validation failed |
| 503 | Service Unavailable | Service temporarily unavailable |

## Rate Limiting

Currently, there is no rate limiting. Future versions may implement request rate limiting.

## Pagination

Pagination is supported via `skip` and `limit` parameters:

- Default `skip`: 0
- Default `limit`: 10
- Maximum `limit`: 100

**Example:**

```bash
# Get items 0-9
curl "http://localhost:8002/notes?skip=0&limit=10"

# Get items 10-19
curl "http://localhost:8002/notes?skip=10&limit=10"
```

## Filtering & Search

### By Completion Status

```bash
# Get completed notes
curl "http://localhost:8002/notes?completed=true"

# Get incomplete notes
curl "http://localhost:8002/notes?completed=false"
```

### By Search Term

Search is case-insensitive and searches both title and description fields:

```bash
curl "http://localhost:8002/notes?search=fastapi"
```

### Combined Filters

```bash
# Completed notes about FastAPI, first 5 results
curl "http://localhost:8002/notes?search=fastapi&completed=true&limit=5"
```

## Date Format

All dates are returned in ISO 8601 format with timezone information:

```
2024-01-15T10:30:00.123456
```

## Interactive Documentation

Two interactive documentation interfaces are available:

- **Swagger UI:** <http://localhost:8002/docs>
- **ReDoc:** <http://localhost:8002/redoc>

Use these to explore the API with a user-friendly interface.

## Common Use Cases

### Create and List Notes

```bash
# Create a note
curl -X POST http://localhost:8002/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "TODO", "description": "Build an API"}'

# List all notes
curl http://localhost:8002/notes
```

### Search and Filter

```bash
# Find all completed tasks about work
curl "http://localhost:8002/notes?search=work&completed=true"
```

### Update Progress

```bash
# Mark a note as complete
curl -X PUT http://localhost:8002/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "TODO", "description": "Build an API", "completed": true}'
```

### Clean Up

```bash
# Delete a note
curl -X DELETE http://localhost:8002/notes/1
```

## Troubleshooting

### 404 Not Found

The note ID does not exist. Check the ID and try again.

### 422 Unprocessable Entity

Usually indicates validation errors:

- Title or description is too short (minimum 3 characters)
- Title is too long (maximum 255 characters)
- Description is too long (maximum 1000 characters)
- Required field is missing

### Database Connection Issues

If the API returns connection errors:

1. Verify PostgreSQL is running
2. Check database credentials in `.env` file
3. Ensure the database exists
4. Check logs for detailed error messages

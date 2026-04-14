#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start application
echo "Starting FastAPI application..."
exec "$@"

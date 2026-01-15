#!/bin/sh

# Set default values
APP_MODULE=${APP_MODULE:-app.main:app}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

# Activate virtualenv in subshell for isolation
(
  # shellcheck disable=SC2039
  export PYTHONPATH=$PYTHONPATH:$(pwd)/src
  if [ -d "venv" ]; then
      source venv/bin/activate
  fi

  # Run app with auto-reload for development
  echo "Starting FastAPI application on http://$HOST:$PORT"
  echo "API docs available at http://$HOST:$PORT/docs"
  uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"
)
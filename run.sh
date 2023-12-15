#!/bin/sh

# Set default values
APP_MODULE=${APP_MODULE:-src.main:app}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8001}

# Activate virtualenv in subshell for isolation
(
  # shellcheck disable=SC2039
  source venv/bin/activate

  # Run app in background for auto-restart
  uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE" &
)

# Trap signals to gracefully shutdown child process
trap 'kill %1' INT TERM EXIT

# Wait for child process
wait

# uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8003
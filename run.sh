#!/bin/sh

# Set default values
APP_MODULE=${APP_MODULE:-app.main:app}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8001}

# Activate virtualenv in subshell for isolation
(
  # shellcheck disable=SC2039
  export PYTHONPATH=$PYTHONPATH:$(pwd)/src
  if [ -d "venv" ]; then
      source venv/bin/activate
  fi

  # Run app in background for auto-restart
  uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"
)
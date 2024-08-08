#!/bin/sh

set -e

whoami


APP_PORT=${PORT:-8000}
cd /app/

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm docker_setup.wsgi:application --bind "0.0.0.0:${APP_PORT}" &

/opt/venv/bin/python /opt/venv/bin/daphne -b 0.0.0.0 -p 8001 docker_setup.asgi:application &

wait

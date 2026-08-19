#!/bin/sh
set -e

# db/redis are already confirmed healthy by docker-compose's depends_on
# condition before this container starts, so no wait-loop is needed here.
python manage.py migrate --noinput

exec "$@"

#!/bin/sh

set -ex

# Wait for the database container
# See: https://docs.docker.com/compose/startup-order/
export PGHOST=${DB_HOST:-db}
export PGPORT=${DB_PORT:-5432}

fixtures_dir=${FIXTURES_DIR:-/app/fixtures}

uwsgi_port=${UWSGI_PORT:-8000}
uwsgi_processes=${UWSGI_PROCESSES:-2}
uwsgi_threads=${UWSGI_THREADS:-2}

mountpoint=${SUBPATH:-/}

# wait for required services
${SCRIPTPATH}/wait_for_db.sh

# Apply database migrations
>&2 echo "Apply database migrations"
python src/manage.py migrate

# Load any JSON fixtures present
if [ -d $fixtures_dir ]; then
    echo "Loading fixtures from $fixtures_dir"

    for fixture in $(ls "$fixtures_dir/"*.json)
    do
        echo "Loading fixture $fixture"
        python src/manage.py loaddata $fixture
    done
fi

# Create superuser
# specify password by setting OBJECTTYPE_SUPERUSER_PASSWORD in the env
# specify username by setting OBJECTTYPE_SUPERUSER_USERNAME in the env
# specify email by setting OBJECTTYPE_SUPERUSER_EMAIL in the env
if [ -n "${OBJECTTYPE_SUPERUSER_USERNAME}" ]; then
    python src/manage.py createinitialsuperuser \
        --no-input \
        --username "${OBJECTTYPE_SUPERUSER_USERNAME}" \
        --email "${OBJECTTYPE_SUPERUSER_EMAIL:-admin@admin.org}"
    unset OBJECTTYPE_SUPERUSER_USERNAME OBJECTTYPE_SUPERUSER_EMAIL OBJECTTYPE_SUPERUSER_PASSWORD
fi

# Start server
>&2 echo "Starting server"
uwsgi \
    --http :$uwsgi_port \
    --http-keepalive \
    --manage-script-name \
    --mount $mountpoint=objecttypes.wsgi:application \
    --static-map /static=/app/static \
    --static-map /media=/app/media  \
    --chdir src \
    --enable-threads \
    --processes $uwsgi_processes \
    --threads $uwsgi_threads \
    --buffer-size=65535
# Stage 1 - Compile needed python dependencies
FROM python:3.11-slim-bullseye AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        libpq-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install pip "setuptools>=70.0.0"
RUN pip install -r requirements/production.txt


# Stage 2 - build frontend
FROM node:20-alpine AS frontend-build

WORKDIR /app

COPY ./*.json /app/
RUN npm ci

COPY ./webpack.config.js ./.babelrc /app/
COPY ./build /app/build/

COPY src/objecttypes/scss/ /app/src/objecttypes/scss/
COPY src/objecttypes/js/ /app/src/objecttypes/js/
RUN npm run build


# Stage 3 - Build docker image suitable for execution and deployment
FROM python:3.11-slim-bullseye AS production

# Stage 3.1 - Set up the needed production dependencies
# install all the dependencies for GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
        # bare minimum to debug live containers
        procps \
        vim \
        # serve correct Content-Type headers
        mime-support \
        # (geo) django dependencies
        postgresql-client \
        gettext \
        binutils \
        libproj-dev \
        gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pip "setuptools>=70.0.0"

COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/uwsgi

# Stage 3.2 - Copy source code
WORKDIR /app
COPY ./bin/wait_for_db.sh /wait_for_db.sh
COPY ./bin/docker_start.sh /start.sh
COPY ./bin/setup_configuration.sh /setup_configuration.sh
RUN mkdir /app/log /app/config

COPY --from=frontend-build /app/src/objecttypes/static /app/src/objecttypes/static
COPY ./src /app/src

RUN useradd -M -u 1000 user
RUN chown -R user /app

# drop privileges
USER user

ARG COMMIT_HASH
ARG RELEASE
ENV GIT_SHA=${COMMIT_HASH}
ENV RELEASE=${RELEASE}

ENV DJANGO_SETTINGS_MODULE=objecttypes.conf.docker

ARG SECRET_KEY=dummy

# Run collectstatic, so the result is already included in the image
RUN python src/manage.py collectstatic --noinput

LABEL org.label-schema.vcs-ref=$COMMIT_HASH \
      org.label-schema.vcs-url="https://github.com/maykinmedia/objecttypes-api" \
      org.label-schema.version=$RELEASE \
      org.label-schema.name="Objecttypes API"

EXPOSE 8000
CMD ["/start.sh"]

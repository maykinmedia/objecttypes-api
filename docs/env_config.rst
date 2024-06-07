.. _installation_env_config:

===================================
Environment configuration reference
===================================



Available environment variables
===============================


Optional
========

* ``SITE_ID``: The database ID of the site object. You usually won't have to touch this. Defaults to: ``1``
* ``DEBUG``: Only set this to True on a local development environment. Various other security settings are derived from this setting!. Defaults to: ``False``
* ``ALLOWED_HOSTS``: a comma separated (without spaces!) list of domains that serve the installation. Used to protect against Host header attacks. Defaults to: ``(empty string)``
* ``USE_X_FORWARDED_HOST``: whether to grab the domain/host from the X-Forwarded-Host header or not. This header is typically set by reverse proxies (such as nginx, traefik, Apache...). Default False - this is a header that can be spoofed and you need to ensure you control it before enabling this. Defaults to: ``False``
* ``IS_HTTPS``: Used to construct absolute URLs and controls a variety of security settings. Defaults to: ``False``
* ``CACHE_DEFAULT``: redis cache address for the default cache. Defaults to: ``localhost:6379/0``
* ``CACHE_AXES``: redis cache address for the brute force login protection cache. Defaults to: ``localhost:6379/0``
* ``EMAIL_HOST``: hostname for the outgoing e-mail server. Defaults to: ``localhost``
* ``EMAIL_PORT``: port number of the outgoing e-mail server. Note that if you're on Google Cloud, sending e-mail via port 25 is completely blocked and you should use 487 for TLS. Defaults to: ``25``
* ``EMAIL_HOST_USER``: username to connect to the mail server. Defaults to: ``(empty string)``
* ``EMAIL_HOST_PASSWORD``: password to connect to the mail server. Defaults to: ``(empty string)``
* ``EMAIL_USE_TLS``: whether to use TLS or not to connect to the mail server. Should be True if you're changing the EMAIL_PORT to 487. Defaults to: ``False``
* ``DEFAULT_FROM_EMAIL``: The default email address from which emails are sent. Defaults to: ``objecttypes@example.com``
* ``LOG_STDOUT``: whether to log to stdout or not. Defaults to: ``False``
* ``LOG_LEVEL``: control the verbosity of logging output. Available values are CRITICAL, ERROR, WARNING, INFO and DEBUG. Defaults to: ``WARNING``
* ``LOG_QUERIES``: enable (query) logging at the database backend level. Note that you must also set DEBUG=1, which should be done very sparingly!. Defaults to: ``False``
* ``LOG_REQUESTS``: enable logging of the outgoing requests. Defaults to: ``False``
* ``ENVIRONMENT``: An identifier for the environment, displayed in the admin depending on the settings module used and included in the error monitoring (see SENTRY_DSN). The default is set according to DJANGO_SETTINGS_MODULE. Defaults to: ``(empty string)``
* ``SUBPATH``: The subpath the application will be mounted on. Defaults to: ``None``
* ``RELEASE``: The version number or commit hash of the application (this is also send to Sentry). Defaults to: ``None``
* ``NUM_PROXIES``: the number of reverse proxies in front of the application, as an integer. This is used to determine the actual client IP adres. On Kubernetes with an ingress you typically want to set this to 2. Defaults to: ``1``
* ``CSRF_TRUSTED_ORIGINS``: A list of trusted origins for unsafe requests (e.g. POST). Defaults to: ``[]``
* ``NOTIFICATIONS_DISABLED``: if this variable is set to true, yes or 1, the notification mechanism will be disabled. Defaults to: ``False``
* ``DISABLE_2FA``: Whether or not two factor authentication should be disabled. Defaults to: ``False``
* ``LOG_OUTGOING_REQUESTS_DB_SAVE``: Whether or not outgoing request logs should be saved to the database. Defaults to: ``False``
* ``LOG_OUTGOING_REQUESTS_MAX_AGE``: The amount of time after which request logs should be deleted from the database. Defaults to: ``7``
* ``SENTRY_DSN``: URL of the sentry project to send error reports to. Default empty, i.e. -> no monitoring set up. Highly recommended to configure this. Defaults to: ``None``


Required
========

* ``SECRET_KEY``: Secret key that's used for certain cryptographic utilities. You should generate one via `miniwebtool <https://www.miniwebtool.com/django-secret-key-generator>`_.


Database
========

* ``DB_NAME``: name of the PostgreSQL database. Defaults to: ``objecttypes``
* ``DB_USER``: username of the database user. Defaults to: ``objecttypes``
* ``DB_PASSWORD``: password of the database user. Defaults to: ``objecttypes``
* ``DB_HOST``: hostname of the PostgreSQL database. Defaults to: ``localhost``
* ``DB_PORT``: port number of the database. Defaults to: ``5432``


Cross-Origin-Resource-Sharing
=============================

* ``CORS_ALLOW_ALL_ORIGINS``: allow cross-domain access from any client. Defaults to: ``False``
* ``CORS_ALLOWED_ORIGINS``: explicitly list the allowed origins for cross-domain requests. Example: http://localhost:3000,https://some-app.gemeente.nl. Defaults to: ``[]``
* ``CORS_ALLOWED_ORIGIN_REGEXES``: same as ``CORS_ALLOWED_ORIGINS``, but supports regular expressions. Defaults to: ``[]``
* ``CORS_EXTRA_ALLOW_HEADERS``: headers that are allowed to be sent as part of the cross-domain request. By default, Authorization, Accept-Crs and Content-Crs are already included. The value of this variable is added to these already included headers. Defaults to: ``[]``


Celery
======

* ``CELERY_RESULT_BACKEND``: the URL of the broker that will be used to actually send the notifications. Defaults to: ``redis://localhost:6379/1``


Elastic APM
===========

* ``ELASTIC_APM_SERVER_URL``: URL where Elastic APM is hosted. Defaults to: ``None``
* ``ELASTIC_APM_SERVICE_NAME``: Name of the service for this application in Elastic APM. Defaults to: ``objecttypes - local``
* ``ELASTIC_APM_SECRET_TOKEN``: Token used to communicate with Elastic APM. Defaults to: ``default``
* ``ELASTIC_APM_TRANSACTION_SAMPLE_RATE``: By default, the agent will sample every transaction (e.g. request to your service). To reduce overhead and storage requirements, set the sample rate to a value between 0.0 and 1.0. Defaults to: ``0.1``



==============
Change history
==============

2.2.1 (2024-08-29)
------------------

**New features**

* made user emails unique to prevent two users logging in with the same email, causing an error (maykinmedia/open-api-framework#39)
* updated open-api-framework to 0.8.0, which includes adding CSRF, CSP and HSTS settings (#124).
  All new environment variables are added to the `documentation <https://objects-and-objecttypes-api.readthedocs.io/en/latest/installation/config.html>`_

.. warning::
    User email addresses will now be unique on a database level. The database migration will fail if there are already
    two or more users with the same email address. You must ensure this is not the case before upgrading.

.. warning::

    SECURE_HSTS_SECONDS has been added with a default of 31536000 seconds, ensure that
    before upgrading to this version of open-api-framework, your entire application is served
    over HTTPS, otherwise this setting can break parts of your application (see https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security)


**Bugfixes and QOL**

* fixed CSS style of help-text icon in the Admin (open-zaak/open-notificaties#150)
* bumped python dependencies due to security issues: django, celery, certifi, maykin-2fa, mozilla-django-oidc-db,
  sentry-sdk, webob and others (#122, #123)


2.2.0 (2024-06-27)
------------------

**New features**

* added `name` and `name_plural` fields to objecttype admin list view (#111)
* added the ``createinitialsuperuser`` command (#92)
* added ``SUBPATH`` environment variable to the docker compose setup (#108)

.. warning::

   Two-factor authentication is enabled by default. The ``DISABLE_2FA``
   environment variable can be used to disable it if needed.

.. warning::

    Because the caching backend was changed to Redis, existing deployments must
    add a Redis container or Redis instance (see ``Installation > Environment
    configuration reference`` in the documentation on how to configure) the
    connection with Redis.

.. warning::

    The service name for Elastic APM is now configurable via the
    ``ELASTIC_APM_SERVICE_NAME`` environment variable. The default value changed
    from ``Objecttypes API`` to ``objecttypes - <ENVIRONMENT>``.

.. warning::

    The following defaults for environment variables changed for the docker
    settings, be sure to override them:
      * ``DB_NAME``: ``objecttypes`` -> ``postgres``
      * ``DB_USER``: ``objecttypes`` -> ``postgres``
      * ``DB_PASSWORD``: ``objecttypes`` -> ``""``

**Bugfixes and QOL**

* updated to Django 4.2 (objects-api#385)
* updated python to 3.11 (#117)
* changed caching backend from LocMem to Redis
* fixed ``Application groups`` admin changelist page (#116)
* upgraded open-api-framework to ``0.4.2`` (#116)
* upgraded various python libraries due to security issues (#109)
* fixed objecttype admin searching with invalid UUIDs (objects-api#361)
* updated changelog regarding ``ELASTIC_AP_SERVICE_NAME`` and changes to default values (#113)
* merged the ``docker-compose-quickstart.yml`` with ``docker-compose.yml`` (#110)
* refactored various settings and configurations (#102)
* added Trivy image scanning and add ``publish`` CI step (#107)
* fixed CodeQL CI action (#106)
* fixed the styling for OIDC login (#105)

2.1.3 (2024-05-03)
------------------

Bugfix release

This release addresses a security weakness.

* [GHSA-3wcp-29hm-g82c] replaced PK for Token model.

2.1.2 (2024-02-06)
------------------

**Bugfixes and QOL**

* added ``USE_X_FORWARDED_HOST`` environment variable (#353)
* added email environment variables (#366)

2.1.1 (2024-02-06)
------------------

**Bugfixes and QOL**

* added ``ENVIRONMENT`` environment variable (maykinmedia/objects-api#310)
* updated python to 3.10 (#94)
* bumped Django to 3.2 (#88)
* removed hijack library (#88)
* replaced vng-api-common with commonground-api-common library (#88)
* updated base for docker image from Debian 10 to Debian 12 (#94)
* bumped python libraries mozilla-django-oidc, mozilla-django-oidc-db (#94)
* fixed name of the folder in INSTALL.rst (#86)

2.1.0 (2022-06-24)
------------------

**Component changes**

* **New features**

  * supported exchange of Objecttypes with Sharing Configs Lib in the Objecttypes Admin (maykinmedia/sharing-configs#32)

* **Bugfixes and QOL**

  * removed boostrap from the landing page (maykinmedia/objects-api#294)
  * bumped to newer versions of pyjwt (#84), babel, lxml, waitress (#80), django (#79), mozilla-django-oidc-db (#74), pillow (#77)
  * remove swagger2openapi from dependencies (#79)
  * fixed Elastic APM configuration (#82)
  * fixed session key name (#78)

**API 1.2.0 changes**

* **New features**

  * added `allowGeometry` field (maykinmedia/objects-api#263)

**API 2.1.0 changes**

* **New features**

  * added `allowGeometry` field (maykinmedia/objects-api#263)


2.0.0 (2021-10-04)
------------------

**Component changes**

* Supports API 2.0.0 and API 1.1.1

* **New features**

  * supported importing of objecttypes from the url in the Objecttypes Admin (#63)
  * added two-factor authentication for the Objecttypes Admin (maykinmedia/objects-api#232)

* **Bugfixes and QOL**

  * bumped to newer versions of django, django-debug-toolbar, sqlparse, pillow (#65)
  * fixed widget for JSON schema in the Objecttypes Admin (maykinmedia/objects-api#253)

**API 2.0.0 changes**

* **Breaking features**

  * paginated API responses (maykinmedia/objects-api#148)


1.1.1 (2021-08-17)
------------------

**New features**

* Supported editing metadata for published object types in the admin (maykinmedia/objects-api#118)

**Bugfixes and QOL**

* Fixed OAS generation: remove unrelated error response bodies and headers (#56)
* Bumped to newer versions of Django, urllib3, Django Debut Toolbar including security fixes (#61)


1.1.0 (2021-04-21)
------------------

**New features**

* Decoupled authentication tokens from users in the admin (maykinmedia/objects-api#115)
* Added additional fields for tokens to store extra information (maykinmedia/objects-api#155)
* Adhered the Objecttypes API to API principles API-18, API-19, API-51 defined in API Design Rules of Nederlandse API Strategie (maykinmedia/objects-api#46)
* Improved the Admin UI:

  * Prettify `json_schema` field on the "object type" page (maykinmedia/objects-api#117)
  * Include `uuid` field to "object type" page (maykinmedia/objects-api#156)

**Bugfixes**

* Bumped to newer versions of Django, Jinja2, Pillow, PyYAML, pip-tools including security fixes (#47, #48, #49, #50, #54)
* Fixed a crash when creating a new version of the objecttype with the incorrect url (maykinmedia/objects-api#121)
* Fixed a crash when opening an objecttype without versions in the admin (maykinmedia/objects-api#144)

**Deployment tooling / infrastructure**

* Created Helm chart to deploy Objecttypes API on Kubernetes (maykinmedia/objects-api#180)
* Added Ansible configuration to deploy Objecttypes on single server (#52)
* Migrated CI from Travis CI to Github Actions (maykinmedia/objects-api#140)

**Documentation**

All documentation is added to https://github.com/maykinmedia/objects-api/docs and included in the Objects API CHANGELOG

* added sections with general intoduction to the API, the description of the object type versions and JSON Schema validation into the OAS (maykinmedia/objects-api#106)

1.0.0 (2021-01-13)
------------------

🎉 First release of Objecttypes API.

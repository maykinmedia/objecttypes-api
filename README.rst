===============
Objecttypes API
===============

:Version: 3.4.0
:Source: https://github.com/maykinmedia/objecttypes-api
:Keywords: objects, assets, zaakobjecten

|docs|

API to manage object definitions. (`Nederlandse versie`_)

Developed by `Maykin Media B.V.`_ commissioned by the Municipality of Utrecht.


Introduction
============

The Objecttypes API aims to standardize various types of objects, on a national
level, in an accessible way and without the need to create a whole new API for
each (simple) object.

This national Objecttypes API is required for registering objects in local
`Objects APIs`_. Organisations can also run an Objecttypes API locally, to use
both national and local definitions of objects.


API specification
=================

|lint-oas| |generate-sdks| |generate-postman-collection|

===================     ==============  =============================
Application version     Release date    API specification
===================     ==============  =============================
latest                  n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v2/openapi.yaml>`_,
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/3.4.0..master>`_)
3.4.0                   2025-12-01      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.4.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.4.0/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/3.0.0..3.4.0>`_)
3.0.0                   2025-01-22      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.0.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.0.0/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/2.3.0..3.0.0>`_)
2.3.0                   2025-01-10      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.3.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.3.0/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/2.2.2..2.3.0>`_)
2.2.2                   2022-08-23      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.2/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.2/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/2.2.0..2.2.2#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
2.2.0                   2022-06-24      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.0/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/2.0.0..2.2.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
2.0.0                   2021-10-04      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                        `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_
                                        (`diff <https://github.com/maykinmedia/objecttypes-api/compare/1.2.0..2.0.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
===================     ==============  =============================

Previous versions are supported for 6 month after the next version is released.

See: `All versions and changes <https://github.com/maykinmedia/objecttypes-api/blob/master/CHANGELOG.rst>`_


Reference implementation
========================

|build-status| |coverage| |code-style| |codeql| |ruff| |docker| |python-versions|

The reference implementation is used to demonstrate the API in action and can
be used for test and demo purposes. The reference implementation is open source,
well tested and available as Docker image.

Quickstart
----------

1. Download and run the Objecttypes API:

   .. code:: bash

      wget https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/docker-compose.yml
      docker compose up -d --no-build
      docker compose exec -T web src/manage.py loaddata demodata
      docker compose exec web src/manage.py createsuperuser

2. In the browser, navigate to ``http://localhost:8000/`` to access the admin
   and the API.


References
==========

* `Documentation <https://objects-and-objecttypes-api.readthedocs.io/>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/objecttypes-api>`_
* `Issues <https://github.com/maykinmedia/objecttypes-api/issues>`_
* `Code <https://github.com/maykinmedia/objecttypes-api>`_
* `Community <https://commonground.nl/groups/view/54477963/objecten-en-objecttypen-api>`_


License
=======

Copyright © Maykin Media, 2020 - 2021

Licensed under the EUPL_


.. _`Nederlandse versie`: README.NL.rst

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl

.. _`Objects APIs`: https://github.com/maykinmedia/objects-api

.. _`EUPL`: LICENSE.md

.. |build-status| image:: https://github.com/maykinmedia/objecttypes-api/workflows/ci/badge.svg?branch=master
    :alt: Build status
    :target: https://github.com/maykinmedia/objecttypes-api/actions?query=workflow%3Aci

.. |docs| image:: https://readthedocs.org/projects/objects-and-objecttypes-api/badge/?version=latest
    :target: https://objects-and-objecttypes-api.readthedocs.io/
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/github/maykinmedia/objecttypes-api/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/objecttypes-api

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |code-style| image:: https://github.com/maykinmedia/objecttypes-api/actions/workflows/code-quality.yml/badge.svg?branch=master
    :alt: Code style
    :target: https://github.com/maykinmedia/objecttypes-api/actions/workflows/code-quality.yml

.. |codeql| image:: https://github.com/maykinmedia/objecttypes-api/actions/workflows/codeql-analysis.yml/badge.svg?branch=master
    :alt: CodeQL scan
    :target: https://github.com/maykinmedia/objecttypes-api/actions/workflows/codeql-analysis.yml

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/objecttypes-api.svg?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/objecttypes-api

.. |python-versions| image:: https://img.shields.io/badge/python-3.12%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/maykinmedia/objecttypes-api/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/maykinmedia/objecttypes-api/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/maykinmedia/objecttypes-api/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/maykinmedia/objecttypes-api/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/maykinmedia/objecttypes-api/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/maykinmedia/objecttypes-api/actions?query=workflow%3Agenerate-postman-collection

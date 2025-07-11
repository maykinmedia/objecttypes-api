===============
Objecttypen API
===============

:Version: 3.1.0
:Source: https://github.com/maykinmedia/objecttypes-api
:Keywords: objecten, assets, zaakobjecten

|docs|

API om object definities te beheren. (`English version`_)

Ontwikkeld door `Maykin Media B.V.`_ in opdracht van de gemeente Utrecht.


Introductie
===========

De Objecttypen API heeft als doel om uiteenlopende typen objecten op een
dynamische wijze te standaardiseren op landelijk niveau en om te voorkomen dat
voor elk (eenvoudig) object een volledige API wordt opgezet.

Deze landelijke Objecttypen API is noodzakelijk voor het registreren van
objecten in lokale `Objecten API's`_. Organisaties kunnen lokaal ook een
Objecttypen API draaien en zo landelijke als lokale definities van objecten
hanteren.


API specificatie
================

|lint-oas| |generate-sdks| |generate-postman-collection|

=================      ==============  =============================
Applicatie versie      Release datum   API specificatie
=================      ==============  =============================
latest                 n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v2/openapi.yaml>`_,
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/3.0.0..master>`_)
3.0.0                  2025-01-22      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.0.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/3.0.0/src/objecttypes/api/v2/openapi.yaml>`_
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/2.3.0..3.0.0>`_)
2.3.0                  2025-01-10      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.3.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.3.0/src/objecttypes/api/v2/openapi.yaml>`_
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/2.2.2..2.3.0>`_)
2.2.2                  2022-08-23      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.2/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.2/src/objecttypes/api/v2/openapi.yaml>`_
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/2.2.0..2.2.2#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
2.2.0                  2022-06-24      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.2.0/src/objecttypes/api/v2/openapi.yaml>`_
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/2.0.0..2.2.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
2.0.0                  2021-10-04      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                       `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_
                                       (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/1.2.0..2.0.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
=================      ==============  =============================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is uitgebracht.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/objecttypes-api/blob/master/CHANGELOG.rst>`_


Referentie implementatie
========================

|build-status| |coverage| |ruff| |docker| |python-versions|

De referentie implementatie toont de API in actie en kan gebruikt worden voor
test en demonstratie doeleinden. De referentie implementatie is open source,
goed getest en beschikbaar als Docker image.

Quickstart
----------

1. Download en start de Objecttypen API:

   .. code:: bash

      wget https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/docker-compose.yml
      docker compose up -d --no-build
      docker compose exec -T web src/manage.py loaddata demodata
      docker compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8000/`` om de admin en de
   API te benaderen.


Links
=====

* `Documentatie <https://objects-and-objecttypes-api.readthedocs.io/>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/objecttypes-api>`_
* `Issues <https://github.com/maykinmedia/objecttypes-api/issues>`_
* `Code <https://github.com/maykinmedia/objecttypes-api>`_
* `Community <https://commonground.nl/groups/view/54477963/objecten-en-objecttypen-api>`_


Licentie
========

Copyright © Maykin Media, 2020 - 2021

Licensed under the EUPL_


.. _`English version`: README.rst

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl

.. _`Objecten API's`: https://github.com/maykinmedia/objects-api

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

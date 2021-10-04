===============
Objecttypen API
===============

:Version: 2.0.0
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

==============  ==============  =============================
Versie          Release datum   API specificatie
==============  ==============  =============================
latest          n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v1/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/api/v1/openapi.yaml>`_,
                                (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/2.0.0..master#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
2.0.0           2021-10-04      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/2.0.0/src/objecttypes/api/v2/openapi.yaml>`_
                                (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/1.2.0..2.0.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
1.2.0           2021-10-04      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.2.0/src/objecttypes/api/v1/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.2.0/src/objecttypes/api/v1/openapi.yaml>`_
                                (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/1.1.1..1.2.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
1.1.1           2021-08-17      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.1.1/src/objecttypes/api/v1/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.1.1/src/objecttypes/api/v1/openapi.yaml>`_
                                (`diff <https://github.com/maykinmedia/objecttypes-api/compare/1.1.0..1.1.1#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
1.1.0           2021-04-21      `verschillen <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.1.0/src/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.1.0/src/openapi.yaml>`_
                                (`verschillen <https://github.com/maykinmedia/objecttypes-api/compare/1.0.0..1.1.0#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
1.0.0           2021-01-13      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.0.0/src/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/1.0.0/src/openapi.yaml>`_
==============  ==============  =============================

Vorige versies worden nog 6 maanden ondersteund nadat de volgende versie is uitgebracht.

Zie: `Alle versies en wijzigingen <https://github.com/maykinmedia/objecttypes-api/blob/master/CHANGELOG.rst>`_


Referentie implementatie
========================

|build-status| |coverage| |black| |docker| |python-versions|

De referentie implementatie toont de API in actie en kan gebruikt worden voor
test en demonstratie doeleinden. De referentie implementatie is open source,
goed getest en beschikbaar als Docker image.

Quickstart
----------

1. Download en start de Objecttypen API:

   .. code:: bash

      $ wget https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/docker-compose-quickstart.yml -O docker-compose-qs.yml
      $ docker-compose -f docker-compose-qs.yml up -d
      $ docker-compose exec -T web src/manage.py loaddata demodata
      $ docker-compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8001/`` om de admin en de
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

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |docker| image:: https://images.microbadger.com/badges/image/maykinmedia/objecttypes-api.svg
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/objecttypes-api

.. |python-versions| image:: https://img.shields.io/badge/python-3.7%2B-blue.svg
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

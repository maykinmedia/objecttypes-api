===============
Objecttypen API
===============

:Version: 0.1.0
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
1.0.0-alpha     n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/openapi.yaml>`_
==============  ==============  =============================

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

      $ wget https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/docker-compose-quickstart.yml
      $ docker-compose -f docker-compose-quickstart.yml up -d
      $ docker-compose exec web src/manage.py createsuperuser

2. In de browser, navigeer naar ``http://localhost:8001/`` om de admin en de 
   API te benaderen.


Links
=====

* `Documentatie <https://readthedocs.org/projects/objects-and-objecttypes-api/badge/?version=latest>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/objecttypes-api>`_
* `Issues <https://github.com/maykinmedia/objecttypes-api/issues>`_
* `Code <https://github.com/maykinmedia/objecttypes-api>`_
* `Community <https://commonground.nl/groups/view/54477963/objecten-en-objecttypen-api>`_


Licentie
========

Copyright © Maykin Media, 2020

Licensed under the EUPL_


.. _`English version`: README.rst

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl

.. _`Objecten API's`: https://github.com/maykinmedia/objects-api

.. _`EUPL`: LICENCE.md

.. |build-status| image:: https://travis-ci.org/maykinmedia/objecttypes-api.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/maykinmedia/objecttypes-api

.. |docs| image:: https://readthedocs.org/projects/objects-and-objecttypes-api/badge/?version=latest
    :target: https://objects-and-objecttypes-api.readthedocs.io/en/latest/?badge=latest
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

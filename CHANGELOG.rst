==============
Change history
==============

1.1.1 (2022-06-22)
------------------

**Bugfixes and QOL**

* Fixed OAS generation: remove unrelated error response bodies and headers (#56)


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

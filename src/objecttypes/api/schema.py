from django.conf import settings

from drf_yasg import openapi

description = """An API to manage Object types.

# Introduction

An OBJECTTYPE represents a collection of objects of similar form and/or function.
An OBJECTTYPE includes a definition of objects, represented as a JSON-schema, and
metadata attributes. Metadata are stores on the high level, JSON schema is prone
to changes and is stored in VERSIONs (see below).

## Versions

A VERSION contains the JSON schema of an OBJECTTYPE at a certain time. Each
OBJECTTYPE can have several VERSIONs. VERSIONs can be `draft` and `published`.
Only draft VERSIONs are allowed to be changed. Once a VERSION is published
it becomes immutable, and if changes are still required a new VERSION should be created.

## JSON schema validation

OBJECTTYPEs are created to ensure that OBJECTs in Objects API have the same
well defined structure. To serve this purpose JSON schemas are used.
Every time an OBJECT is created or updated in Objects API its `data` in JSON form
are validated against JSON schema in the related OBJECTTYPE VERSION.

**Useful links**

* [JSON schema](https://json-schema.org/)

"""

info = openapi.Info(
    title=f"{settings.PROJECT_NAME} API",
    default_version=settings.API_VERSION,
    description=description,
)

from django.conf import settings

from drf_yasg import openapi

description = """An API to manage Object types.

# Introduction

An OBJECTTYPE represents a collection of objects of similar form and/or function.
An OBJECTTYPE includes a definition of an object, represented as a JSON schema, and
metadata attributes. Metadata is stored on the top level and the JSON schema itself is stored
in VERSIONs because the definition of an object can change over time.

## Versions

Over time, an OBJECTTYPE can also change. This is reflected with VERSIONs. 

A VERSION contains the JSON schema of an OBJECTTYPE at a certain time. Each
OBJECTTYPE can have several VERSIONs. A VERSION can have the `status` "draft" or "published".
Only draft VERSIONs are allowed to be changed. Once a VERSION is published
it becomes immutable, and if changes are still required a new VERSION should be created.

## JSON schema validation

OBJECTTYPEs are created to ensure that OBJECTs in the Objects API have the same
well defined structure. The JSON schema makes this possible.
The Objects API retrieves the related OBJECTTYPE and validates the object data against
the JSON schema in the appropriate VERSION of the OBJECTTYPE.

**Useful links**

* [JSON schema](https://json-schema.org/)

"""

info = openapi.Info(
    title=f"{settings.PROJECT_NAME} API",
    default_version=settings.API_VERSION,
    description=description,
)

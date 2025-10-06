from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "2.2.2"


# api settings
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_FILTER_BACKENDS": ["vng_api_common.filters_backend.Backend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "objecttypes.token.authentication.TokenAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "objecttypes.utils.autoschema.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "objecttypes.token.permissions.IsTokenAuthenticated"
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v2",  # NOT to be confused with API_VERSION - it's the major version part
    "ALLOWED_VERSIONS": ("v2",),
    "VERSION_PARAM": "version",
    "EXCEPTION_HANDLER": "objecttypes.utils.views.exception_handler",
    # test
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

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

SPECTACULAR_SETTINGS = {
    "REDOC_DIST": "SIDECAR",
    "SCHEMA_PATH_PREFIX": r"/api/v[1-9]+",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "TITLE": "Objecttypes API",
    "DESCRIPTION": description,
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {
        "url": "https://github.com/maykinmedia/objecttypes-api",
    },
    "LICENSE": {"name": "EUPL-1.2"},
    "EXTERNAL_DOCS": {
        "url": "https://objects-and-objecttypes-api.readthedocs.io/",
    },
    "VERSION": API_VERSION,
    "GET_MOCK_REQUEST": "objecttypes.utils.autoschema.build_mock_request",
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
    "TAGS": [{"name": "Objecttypes"}],
    "SERVERS": [{"url": "/api/v2"}],
}

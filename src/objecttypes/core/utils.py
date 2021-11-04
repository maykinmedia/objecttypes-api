from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError

import requests
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for


def check_json_schema(json_schema: dict) -> None:
    schema_validator = validator_for(json_schema)
    try:
        schema_validator.check_schema(json_schema)
    except SchemaError as exc:
        raise ValidationError(exc.args[0]) from exc


def download_json_schema(url: str) -> dict:
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        raise ValidationError("The Objecttype URL does not exist.")

    if response.status_code != requests.codes.ok:
        raise ValidationError("Objecttype URL returned non OK status.")

    try:
        response_json = response.json()
    except JSONDecodeError:
        raise ValidationError("Could not parse JSON from Objecttype URL.")

    check_json_schema(response_json)

    return response_json


def import_json_schema(json_schema: dict, name: str = "", name_plural: str = ""):
    """
    create Objecttype with first version from JSON schema

    JSON schema should already be valid
    """

    from .models import ObjectType, ObjectVersion

    name = name or json_schema["title"].title()

    object_type = ObjectType.objects.create(
        name=name,
        name_plural=name_plural,
        description=json_schema.get("description", ""),
    )
    ObjectVersion.objects.create(
        object_type=object_type,
        json_schema=json_schema,
    )

    return object_type

from django.core.exceptions import ValidationError

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for


def check_json_schema(json_schema: dict):
    schema_validator = validator_for(json_schema)
    try:
        schema_validator.check_schema(json_schema)
    except SchemaError as exc:
        raise ValidationError(exc.args[0]) from exc

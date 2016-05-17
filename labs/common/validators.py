from jsonschema import validate as validate_schema
from jsonschema.exceptions import ValidationError as Draft4ValidationError
from django.core.exceptions import ValidationError

from .settings import URL_RegEx

info_schema = {
    "type": "object",
    "properties": {
        "languages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "level": {"type": "integer", "minimum": 0, "maximum": 10}
                },
                "required": ["name", "level"],
                "additionalProperties": False
            },
            "minItems": 1
        },
        "websites": {
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "string", "pattern": URL_RegEx},
            "maxItems": 3,
        }
    }
}

skills_schema = {
    "type": "array",
    "items": {"type": "string", "maxItems": 8}
}

location_schema = {
    "type": "array",
    "items": {"type": "array", "items": {"type": "number"}, "maxItems": 2}
}


def info_schema_validator(data):
    try:
        validate_schema(data, info_schema)
    except Draft4ValidationError as e:
        raise ValidationError(e.message)


def skills_schema_validator(data):
    try:
        validate_schema(data, skills_schema)
    except Draft4ValidationError as e:
        raise ValidationError(e.message)


def location_schema_validator(data):
    try:
        validate_schema(data, location_schema)
    except Draft4ValidationError as e:
        raise ValidationError(e.message)


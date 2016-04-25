import jsonschema


SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "minLength": 1
            },
            "time": {
                "type": "string",
                "minLength": 4
            },
            "date": {
                "type": "string",
                "minLength": 1
            },
        },
        "required": ["summary"],
        "additionalProperties": False
    }
}


# Initial validator
class Validator(jsonschema.Draft4Validator):
    def __init__(self, schema):
        format_checker = jsonschema.FormatChecker()
        super(Validator, self).__init__(
            schema, format_checker=format_checker)


# Validation of input template
def validate(config):
    return Validator(SCHEMA).validate(config)

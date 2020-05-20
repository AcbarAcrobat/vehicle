empty_string = { 'type': 'string', 'maxLength': 0 }


uuid_string = { 'type': 'string', 'pattern': r'^\w{8}(-\w{4}){3}-\w{12}$' }


def pattern_string(pattern):
    return { 'type': 'string', 'pattern': pattern }


def any_of_types(*types):
    return {
        'anyOf': [ {'type': type_} for type_ in types ]
    }


def array_of(type_):
    return {
        'type': 'array',
        'items': { 'type': type_ }
    }


ip_addr = pattern_string(
    r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' \
    r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' \
    r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' \
    r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'
)


def skeleton(items):
    return {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'required': ['result', 'done'],
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'done': { 'const': True },
            'result': {
                'type': 'array',
                'items': items
            }
        }
    }


def build(properties, keys=None):
    if keys is None:
        required = list(properties.keys())
        props = properties
    else:
        required = keys
        props = {k: properties[k] for k in keys}
    
    return {
        'type': 'object',
        'required': required,
        'additionalProperties': False,
        'properties': props
    }


def count_ok():
    return {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'required': ['result', 'done'],
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'done':     { 'const': True },
            'result':   { 'type': 'integer' }
        }
    }

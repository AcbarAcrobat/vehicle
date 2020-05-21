from schema.base import *


user_logs_fk_properties = {
    'created_at': { 'type': 'integer' },
    'user_id': { 'type': 'integer' },
    'entity': { 'type': 'string' },
    'result': { 'type': 'array' },
    'event_id': { 'type': 'integer' },
    'intention': any_of_types('object', 'array'),
    'id': { 'type': 'integer' }
}


def foreign_key_schema(keys=None):
    global user_logs_fk_properties
    return skeleton( build(user_logs_fk_properties, keys) )

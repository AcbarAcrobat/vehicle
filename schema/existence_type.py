from schema.base import *


existence_type_fk_properties = {
    'id': { 'type': 'integer' },
    'name': { 'type': 'string' },
}

def foreign_key_schema(keys=None):
    global existence_type_fk_properties
    return skeleton( build(existence_type_fk_properties, keys) )

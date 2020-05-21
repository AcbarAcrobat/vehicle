from schema.base import *


mobile_operator_fk_properties = {
    'id': { 'type': 'integer' },
    'name': { 'type': 'string' },
}

def foreign_key_schema(keys=None):
    global mobile_operator_fk_properties
    return skeleton( build(mobile_operator_fk_properties, keys) )

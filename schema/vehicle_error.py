from schema.base import *


vehicle_error_fk_properties = {
    'code': { 'type': 'integer' },
    'vehicle_id': { 'type': 'integer' },
    'occurred_at': { 'type': 'integer' },
    "outdated_at": any_of_types("null", "integer")
}

def foreign_key_schema(keys=None):
    global vehicle_error_fk_properties
    return skeleton( build(vehicle_error_fk_properties, keys) )

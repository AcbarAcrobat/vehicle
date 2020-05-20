from schema.base import *


camera_availability_fk_properties = {
    'id': { 'type': 'integer' },
    'name': { 'type': 'string' },
    'description': { 'type': 'string' }
}

def foreign_key_schema(keys=None):
    global camera_availability_fk_properties
    return skeleton( build(camera_availability_fk_properties, keys) )

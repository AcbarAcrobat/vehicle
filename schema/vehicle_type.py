from schema.base import *


vehicle_type_fk_properties = {
    "name": { "type": "string" },
    "image": { "type": "string" },
    "id": { "type": "integer" }
}

def foreign_key_schema(keys=None):
    global vehicle_type_fk_properties
    return skeleton( build(vehicle_type_fk_properties, keys) )

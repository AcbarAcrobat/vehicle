from schema.base import *


vehicle_part_type_fk_properties = {
    "name": { "type": "string" },
    "id": { "type": "integer" },
    "full_image": { "type": "string" },
    "small_image": { "type": "string" }
}

def foreign_key_schema(keys=None):
    global vehicle_part_type_fk_properties
    return skeleton( build(vehicle_part_type_fk_properties, keys) )

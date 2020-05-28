from schema.base import *


vehicle_to_attached_file_fk_properties = {
    "vehicle_id": { "type": "integer" },
    "file_name": { "type": "string" },
    "order_id": any_of_types("null", "integer"),
    "file_id": { "type": "integer" },
    "id": { "type": "integer" }
}

def foreign_key_schema(keys=None):
    global vehicle_to_attached_file_fk_properties
    return skeleton( build(vehicle_to_attached_file_fk_properties, keys) )

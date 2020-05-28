from schema.base import *


vehicle_to_stage_fk_properties = {
    "vehicle_id": { "type": "integer" },
    "stage_id": { "type": "integer" }
}

def foreign_key_schema(keys=None):
    global vehicle_to_stage_fk_properties
    return skeleton( build(vehicle_to_stage_fk_properties, keys) )

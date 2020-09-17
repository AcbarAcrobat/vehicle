from schema.base import *


vehicle_camera_error_fk_properties = {
    "vehicle_camera_id": {"type": "integer"},
    "occurred_at": {"type": "integer"},
    "code": {"type": "integer"},
    "outdated_at": any_of_types("null", "integer")
}

def foreign_key_schema(keys=None):
    global vehicle_camera_error_fk_properties
    return skeleton( build(vehicle_camera_error_fk_properties, keys) )

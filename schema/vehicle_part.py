from schema.base import *
from schema import vehicle_camera


vehicle_part_fk_properties = {
    "id": { "type": "integer" },
    "vehicle_id": { "type": "integer" },
    "part_type_id": { "type": "integer" },
    "cameras": array_of("integer")
}

vehicle_part_struct_properties = {
    ** vehicle_part_fk_properties,
    "cameras":  {
        'type': 'array',
        'items': build(vehicle_camera.vehicle_camera_struct_properties)
    }
}

def foreign_key_schema(keys=None):
    global vehicle_part_fk_properties
    return skeleton( build(vehicle_part_fk_properties, keys) )

def structural_schema(keys=None):
    global vehicle_part_struct_properties
    return skeleton( build(vehicle_part_struct_properties, keys) )

from schema.base import *


vehicle_contract_binding_fk_properties = {
    "stages": array_of("integer"),
    "id": {"type": "integer"},
    "vehicle_id": {"type": "integer"},
    "contract_id": {"type": "integer"}
}

stages_fk_properties = {
    "vehicle_contract_binding_id": {"type": "integer"},
    "stage_id": {"type": "integer"}
}

vehicle_contract_binding_struct_properties = {
    ** vehicle_contract_binding_fk_properties,
    "stages": {
        'type': 'array',
        'items': build(stages_fk_properties)
    }
}


def foreign_key_schema(keys=None):
    global vehicle_contract_binding_fk_properties
    return skeleton(build(vehicle_contract_binding_fk_properties, keys))


def structural_schema(keys=None, error_keys=None):
    global vehicle_contract_binding_struct_properties
    return skeleton(build(vehicle_contract_binding_struct_properties, keys))

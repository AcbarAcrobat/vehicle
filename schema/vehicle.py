from schema.base import *


vehicle_fk_properties = {
    "subscriber_identification_module_number": {"type": "string"},
    "international_mobile_equipment_identity": {"type": "string"},
    "vehicle_identification_number": {"type": "string"},
    "computer_serial_number": {"type": "string"},
    "is_stats_check_enabled": {"type": "boolean"},
    "mobile_operator_id": {"type": "integer"},
    "registration_plate": {"type": "string"},
    "contract_bindings": array_of("integer"),
    "ownership_type_id": {"type": "integer"},
    "financing_type_id": any_of_types("null", "integer"),
    "sync_with_netris": {"type": "boolean"},
    "attached_files": array_of("integer"),
    "approving_date": {"type": "integer"},
    "chat_room_id": {"type": "integer"},
    "availability": {"type": "integer"},
    "template_id": {"type": "integer"},
    "contract_id": {"type": "integer"},
    "ip_address": ip_addr,
    "region_id": {"type": "integer"},
    "is_hidden": {"type": "boolean"},
    "longitude": {"type": "number"},
    "password": {"type": "string"},
    "axxon_id": {"type": "string"},
    "latitude": {"type": "number"},
    "type_id": {"type": "integer"},
    "status": {
        "anyOf": [
            array_of("integer"),
            {"type": "null"}
        ]
    },
    "stages": array_of("integer"),
    "parts": array_of("integer"),
    "error": {
        "anyOf": [
            array_of("integer"),
            {"type": "null"}
        ]
    },
    "login": {"type": "string"},
    "title": {"type": "string"},
    "id": {"type": "integer"}
}

error_fk_properties = {
    "vehicle_id": {"type": "integer"},
    "occurred_at": {"type": "integer"},
    "code": {"type": "integer"}
}

status_fk_properties = {
    "storage": {"type":"integer"},
    "cameras_total": {"type":"integer"},
    "occurred_at": {"type":"integer"},
    "cameras_online": {"type":"integer"},
    "loss": {"type":"integer"},
    "ram": {"type":"integer"},
    "ping": {"type":"integer"},
    "cpu": {"type":"integer"},
    "jitter": {"type":"integer"},
    "status": {"type":"integer"},
    "vehicle_id": {"type":"integer"},
    "id": {"type":"integer"}
}

attached_files_fk_properties = {
    "id": {"type": "integer"},
    "order_id": any_of_types("null", "integer"),
    "file_id": {"type": "integer"},
    "vehicle_id": {"type": "integer"},
    "file_name": {"type": "string"}
}

contract_bindings_fk_properties = {
    "contract_id": {"type": "integer"},
    "vehicle_id": {"type": "integer"},
    "id": {"type": "integer"},
    "stages": {
        "type": "array",
        "items": {
            "type": "object",
            'required': ['stage_id', 'vehicle_contract_binding_id'],
            "additionalProperties": False,
            "properties": {
                "stage_id": {"type": "integer"},
                "vehicle_contract_binding_id": {"type": "integer"},
            }
        }
    }
}

stages_fk_properties = {
    "vehicle_id": {"type": "integer"},
    "stage_id": {"type": "integer"}
}

vehicle_struct_properties = {
    ** vehicle_fk_properties,
    "error": {
        'anyOf': [
            { 'type': 'null' },
            {
                'type': 'array',
                'items': build(error_fk_properties)
            }
        ]
    },
    "status": {
        'anyOf': [
            { 'type': 'null' },
            {
                'type': 'array',
                'items': build(status_fk_properties)
            }
        ]
    },
    "attached_files": {
        'anyOf': [
            { 'type': 'null' },
            {
                'type': 'array',
                'items': build(attached_files_fk_properties)
            }
        ]
    },
    "contract_bindings": {
        'anyOf': [
            { 'type': 'null' },
            {
                'type': 'array',
                'items': build(contract_bindings_fk_properties)
            }
        ]
    },
    "parts": {"type": "array"},
    "stages": {
        'type': 'array',
        'items': build(stages_fk_properties)
    }
}


def structural_schema(keys=None, error_keys=None):
    global vehicle_struct_properties
    return skeleton( build(vehicle_struct_properties, keys) )


def foreign_key_schema(keys=None):
    global vehicle_fk_properties
    return skeleton(build(vehicle_fk_properties, keys))

from schema.base import *


vehicle_camera_fk_properties = {
    "stream_resolution_height": {"type": "integer"},
    "stream_resolution_width": {"type": "integer"},
    "camera_availability_id": {"type": "integer"},
    "hls_second_stream_url": {"type": "string"},
    "hls_first_stream_url": {"type": "string"},
    "camera_position_id": {"type": "integer"},
    "stream_resolution": {"type": "integer"},
    "installation_site": {"type": "integer"},
    "rtsp_second_url": {"type": "string"},
    "stream_bitrate": {"type": "integer"},
    "rtsp_first_url": {"type": "string"},
    "daytime_image": {"type": "integer"},
    "night_image": {"type": "integer"},
    "rtsp_camera": {"type": "string"},
    "description": {"type": "string"},
    "ip_address": ip_addr,
    "stream_fps": {"type": "integer"},
    "axxon_id": {"type": "string"},
    "part_id": {"type": "integer"},
    "status": {
        "anyOf": [
            array_of("integer"),
            {"type": "null"}
        ]
    },
    "id": {"type": "integer"},
    "camera_position": {
        "type": "object",
        "required": ["x", "y", "scope", "azimut"],
        "additionalProperties": False,
        "properties": {
            "x": {"type": "integer"},
            "y": {"type": "integer"},
            "scope": {"type": "integer"},
            "azimut": {"type": "integer"}
        }
    },
    "error": {
        "anyOf": [
            array_of("integer"),
            {"type": "null"}
        ]
    }
}

error_fk_properties = {
    "vehicle_camera_id": {"type": "integer"},
    "occurred_at": {"type": "integer"},
    "code": {"type": "integer"}
}

status_fk_properties = {
    "scene_state": {"type": "integer"},
    "occurred_at": {"type": "integer"},
    "fps": {"type": "integer"},
    "degrade_state": {"type": "integer"},
    "camera_id": {"type": "integer"},
    "loss": {"type": "integer"},
    "resolution_width": {"type": "integer"},
    "resolution_height": {"type": "integer"},
    "ping": {"type": "integer"},
    "jitter": {"type": "integer"},
    "status": {"type": "integer"},
    "bitrate": {"type": "integer"},
    "id": {"type": "integer"}
}

vehicle_camera_struct_properties = {
    ** vehicle_camera_fk_properties,
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
    }
}


def foreign_key_schema(keys=None):
    global vehicle_camera_fk_properties
    return skeleton(build(vehicle_camera_fk_properties, keys))


def structural_schema(keys=None, error_keys=None):
    global vehicle_camera_struct_properties
    return skeleton(build(vehicle_camera_struct_properties, keys))

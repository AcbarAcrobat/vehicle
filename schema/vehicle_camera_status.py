from schema.base import *


vehicle_camera_status_fk_properties = {
    "archive_start_at_ms": {"type": "integer"},
    "archive_duration_ms": {"type": "integer"},
    "resolution_height": {"type": "integer"},
    "resolution_width": {"type": "integer"},
    "degrade_state": {"type": "integer"},
    "scene_state": {"type": "integer"},
    "occurred_at": {"type": "integer"},
    "camera_id": {"type": "integer"},
    "bitrate": {"type": "integer"},
    "jitter": {"type": "integer"},
    "status": {"type": "integer"},
    "ping": {"type": "integer"},
    "loss": {"type": "integer"},
    "fps": {"type": "integer"},
    "id": {"type": "integer"}
}


def foreign_key_schema(keys=None):
    global vehicle_camera_status_fk_properties
    return skeleton(build(vehicle_camera_status_fk_properties, keys))

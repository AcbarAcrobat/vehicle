from schema.base import *


vehicle_status_fk_properties = {
    "status": { "type": "integer" },
    "storage": { "type": "integer" },
    "id": { "type": "integer" },
    "cameras_online": { "type": "integer" },
    "cpu": { "type": "integer" },
    "ping": { "type": "integer" },
    "vehicle_id": { "type": "integer" },
    "ram": { "type": "integer" },
    "jitter": { "type": "integer" },
    "loss": { "type": "integer" },
    "occurred_at": { "type": "integer" },
    "cameras_total": { "type": "integer" }
}

def foreign_key_schema(keys=None):
    global vehicle_status_fk_properties
    return skeleton( build(vehicle_status_fk_properties, keys) )

import pytest
from endpoint import VehicleCamera, VehicleCameraError
from helper.logger import LOGGER
from datetime import datetime as dt


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleCameraError(session)


@pytest.fixture(scope='function')
def camera_id(session):
    yield VehicleCamera(session).get_random()['id']


@pytest.fixture(scope='function')
def body(faker, session, camera_id):
    yield {
        "values": [
            {"vehicle_camera_id": camera_id, "occurred_at": round(dt.utcnow().timestamp()*1000), "code": 1},
            {"vehicle_camera_id": camera_id, "occurred_at": round(dt.utcnow().timestamp()*1000), "code": 2},
            {"vehicle_camera_id": camera_id, "occurred_at": round(dt.utcnow().timestamp()*1000), "code": 3}
        ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids

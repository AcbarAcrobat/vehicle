import pytest
from endpoint import VehicleCameraStatus, VehicleCamera
from helper.logger import LOGGER
from datetime import datetime as dt


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleCameraStatus(session)


@pytest.fixture(scope='function')
def camera_id(session):
    yield VehicleCamera(session).get_random()['id']


@pytest.fixture(scope='function')
def body(faker):
    yield {
        "values": [
            {
                "scene_state": faker.random_digit_not_null(),
                "fps": faker.random_digit_not_null(),
                "degrade_state": faker.random_digit_not_null(),
                "camera_id": camera_id,
                "loss": faker.random_digit_not_null(),
                "resolution_width": faker.random_digit_not_null(),
                "resolution_height": faker.random_digit_not_null(),
                "ping": faker.random_digit_not_null(),
                "status": faker.random_digit_not_null(),
                "bitrate": faker.random_digit_not_null(),
                "jitter": faker.random_digit_not_null(),
                "occurred_at": round(dt.utcnow().timestamp()*1000)
            },
            {
                "scene_state": faker.random_digit_not_null(),
                "fps": faker.random_digit_not_null(),
                "degrade_state": faker.random_digit_not_null(),
                "camera_id": camera_id,
                "loss": faker.random_digit_not_null(),
                "resolution_width": faker.random_digit_not_null(),
                "resolution_height": faker.random_digit_not_null(),
                "ping": faker.random_digit_not_null(),
                "status": faker.random_digit_not_null(),
                "bitrate": faker.random_digit_not_null(),
                "jitter": faker.random_digit_not_null(),
                "occurred_at": round(dt.utcnow().timestamp()*1000)
            }
        ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

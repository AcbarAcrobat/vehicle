import pytest
from endpoint import VehicleCamera, VehiclePart
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleCamera(session)


@pytest.fixture(scope='function')
def part_id(session):
    yield VehiclePart(session).get_random()['id']


@pytest.fixture(scope='function')
def body(faker, session, part_id):
    yield {
        "values": [
            {"part_id": part_id, "camera_position": {"x": 11, "y": 12, "scope": 13, "azimut": 14}, "camera_position_id": 1},
            {"part_id": part_id, "camera_position": {"x": 21, "y": 22, "scope": 23, "azimut": 24}, "camera_position_id": 2},
            {"part_id": part_id, "camera_position": {"x": 31, "y": 32, "scope": 33, "azimut": 34}, "camera_position_id": 3}
        ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

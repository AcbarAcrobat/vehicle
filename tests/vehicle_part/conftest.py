import pytest
from endpoint import VehiclePart, Vehicle, VehiclePartType, VehicleCamera
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehiclePart(session)


@pytest.fixture(scope='function')
def vehicle_id(session):
    yield Vehicle(session).get_random()['id']


@pytest.fixture(scope='function')
def part_type_id(session):
    yield VehiclePartType(session).get_random()['id']


@pytest.fixture(scope='function')
def camera_id(session):
    yield VehicleCamera(session).get_random()['id']


@pytest.fixture(scope='function')
def body(faker, vehicle_id, part_type_id):
    yield {
        "values": [
            {"vehicle_id": vehicle_id, "part_type_id": part_type_id},
            {"vehicle_id": vehicle_id, "part_type_id": part_type_id}
        ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

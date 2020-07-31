import pytest
from endpoint import VehiclePart, Vehicle, VehiclePartType, VehicleCamera
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehiclePart(session)


@pytest.fixture(scope='function')
def vehicle_id(session, data_vehicle):
    # yield Vehicle(session).get_random()['id']
    yield data_vehicle["ids"][0]


@pytest.fixture(scope='function')
def part_type_id(session, data_vehicle_type):
    # yield VehiclePartType(session).get_random()['id']
    yield data_vehicle_type["ids"][0]


@pytest.fixture(scope='function')
def camera_id(session, data_vehicle_camera):
    # yield VehicleCamera(session).get_random()['id']
    yield data_vehicle_camera["ids"][0]


@pytest.fixture(scope='function')
def body(faker, vehicle_id, part_type_id):
    yield {
        "values": [
            {"vehicle_id": vehicle_id, "part_type_id": part_type_id},
            {"vehicle_id": vehicle_id, "part_type_id": part_type_id}
        ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    # ids = endpoint.add(json=body).json()['result']
    r = endpoint.add(json=body)
    LOGGER.info(r.json())
    ids = r.json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

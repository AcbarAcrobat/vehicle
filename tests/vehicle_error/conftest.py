import pytest
from endpoint import VehicleError, Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleError(session)


@pytest.fixture(scope='function')
def vehicle_id(session, data_vehicle):
    # yield Vehicle(session).get_random()['id']
    yield data_vehicle["ids"][0]


@pytest.fixture(scope='function')
def body(faker, vehicle_id):
    yield {
        "values": [
            {"vehicle_id": vehicle_id, "contract_id": 1},
            {"vehicle_id": vehicle_id, "contract_id": 2},
            {"vehicle_id": vehicle_id, "contract_id": 3}
    ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

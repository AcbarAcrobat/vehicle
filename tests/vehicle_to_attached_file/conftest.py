import pytest
from endpoint import VehicleToAttachedFile, Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToAttachedFile(session)


@pytest.fixture(scope='function')
def vehicle_id(session):
    yield Vehicle(session).get_random()['id']


@pytest.fixture(scope='function')
def body(faker, vehicle_id):
    yield {
        "values": [{
            "file_id": faker.random_number(),
            "vehicle_id": vehicle_id,
            "file_name": f"{faker.uuid4()}.pdf"
        }, {
            "file_id": faker.random_number(),
            "vehicle_id": vehicle_id,
            "file_name": f"{faker.uuid4()}.pdf"
        }]
    }

@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

import pytest
from endpoint import VehicleToAttachedFile, Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToAttachedFile(session)


@pytest.fixture(scope='function')
def vehicle_id(session, data_vehicle):
    # yield Vehicle(session).get_random()['id']
    yield data_vehicle["ids"][0]


@pytest.fixture(scope='function')
def body(faker, data_vehicle, data_loaded_file_vehicle):
    yield {
        "values": [{
            "file_id": data_loaded_file_vehicle["ids"][0],
            "vehicle_id": data_vehicle["ids"][3],
            "file_name": f"{faker.uuid4()}.pdf"
        }, {
            "file_id": data_loaded_file_vehicle["ids"][0],
            "vehicle_id": data_vehicle["ids"][4],
            "file_name": f"{faker.uuid4()}.pdf"
        }]
    }

@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

import pytest
from endpoint import VehicleType
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleType(session)


@pytest.fixture(scope='function')
def body(faker):
    yield {
        "values": [{
            "name": faker.uuid4(),
            "image": f"images/{faker.uuid4()}.svg"
        }, {
            "name": faker.uuid4(),
            "image": f"images/{faker.uuid4()}.svg"
        }]
    }


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

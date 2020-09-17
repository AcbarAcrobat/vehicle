import pytest
from endpoint import VehicleStatus
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleStatus(session)


@pytest.fixture(scope='function')
def body(faker):
    yield {
        "values": [{
            "name": faker.uuid4(),
            "full_image": f"images/{faker.uuid4()}.svg",
            "small_image": f"images/{faker.uuid4()}.svg"
        }, {
            "name": faker.uuid4(),
            "full_image": f"images/{faker.uuid4()}.svg",
            "small_image": f"images/{faker.uuid4()}.svg"
        }]
    }


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    # ids = endpoint.add(json=body).json()['result']
    r = endpoint.add(json=body)
    LOGGER.info(r.json())
    ids = r.json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

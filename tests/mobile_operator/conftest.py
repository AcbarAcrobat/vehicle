import pytest
from endpoint import MobileOperator
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield MobileOperator(session)


@pytest.fixture(scope='function')
def body(faker):
    yield {
        "values": [
            {"name": faker.uuid4()},
            {"name": faker.uuid4()}
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

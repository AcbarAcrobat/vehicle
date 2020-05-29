import pytest
from endpoint import Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield Vehicle(session)


@pytest.fixture(scope='class')
def body(faker):
    yield {
        "values": [
            {"type_id": 1, "login": "QWE"},
            {"type_id": 2, "login": "ASD"},
            {"type_id": 3, "login": "ZXC"}
    ]}


@pytest.fixture(scope='class')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

import pytest
from endpoint import CameraAvailability
from helper.logger import LOGGER
from pytest_testconfig import config


@pytest.fixture(scope='class')
def endpoint(session):
    yield CameraAvailability(session)


@pytest.fixture(scope='function')
def body(faker):
    yield {
        "values": [
            {"name": faker.uuid4(), "description": faker.uuid4()},
            {"name": faker.uuid4(), "description": faker.uuid4()}
    ]}


@pytest.fixture(scope='function')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)
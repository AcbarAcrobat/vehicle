import pytest
from endpoint import Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield Vehicle(session)

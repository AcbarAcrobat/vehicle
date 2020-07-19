import pytest
from endpoint import VehicleToStage
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToStage(session)

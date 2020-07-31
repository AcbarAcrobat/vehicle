import pytest
from endpoint import VehicleToAttachedFile, Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToAttachedFile(session)


@pytest.fixture(scope='function')
def vehicle_id(session, data_vehicle):
    yield data_vehicle["ids"][0]

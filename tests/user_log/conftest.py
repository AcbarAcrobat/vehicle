import pytest
from endpoint import EventType


@pytest.fixture(scope='function')
def event_id(request, session):
    yield EventType(session).get_random()['id']
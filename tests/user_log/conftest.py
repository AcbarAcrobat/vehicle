import pytest
from endpoint import EventType
from endpoint import UserLogs


@pytest.fixture(scope='function')
def event_id(request, session):
    yield EventType(session).get_random()['id']

@pytest.fixture(scope='class')
def endpoint(session):
    yield UserLogs(session)
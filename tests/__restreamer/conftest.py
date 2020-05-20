import pytest
from endpoint import Region

@pytest.fixture(scope='function')
def region_id(request, session):
    yield Region(session).get_random()['id']
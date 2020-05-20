import pytest
from endpoint import Contract, Restreamer


@pytest.fixture(scope='function')
def restreamer_id(request, session):
    yield Restreamer(session).get_random()['id']
    

@pytest.fixture(scope='function')
def contract_id(request, session):
    yield Contract(session).get_random()['id']
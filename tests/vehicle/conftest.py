import pytest
from endpoint import Vehicle
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield Vehicle(session)


@pytest.fixture(scope='class')
def body(faker, data_vehicle_template):
    yield {
        "values": [
            {"type_id": 1, "login": faker.uuid4(), "template_id": data_vehicle_template["ids"][0]},
            {"type_id": 1, "login": faker.uuid4(), "template_id": data_vehicle_template["ids"][1]},
            {"type_id": 1, "login": faker.uuid4(), "template_id": data_vehicle_template["ids"][2]}
    ]}

@pytest.fixture(scope='class')
def new_entity(endpoint, body):
    ids = endpoint.add(json=body).json()['result']
    LOGGER.info(f"New ids: {ids}")
    yield ids
    endpoint.delete_by_ids(ids)

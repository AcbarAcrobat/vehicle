import pytest
from endpoint import VehicleToStage, ContractStage
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToStage(session)


@pytest.fixture(scope='class')
def tmp_stages(session, faker, data_contract):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "created_at_epoch": 1000,
            "start_at_epoch": 2000,
            "end_at_epoch": 3000,
            "contract_id": data_contract["ids"][i],
            "title": faker.uuid4(),
            "price": abs(faker.pyfloat())
        })
    r = ContractStage(session).add(json=body)
    LOGGER.info(f"ContractStage: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    ContractStage(session).delete_many_by("id", ids)
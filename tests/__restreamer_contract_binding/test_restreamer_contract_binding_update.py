import pytest
import allure 
from helper import LOGGER
from endpoint import RestreamerContractBinding
from truth.truth import AssertThat


class TestRestreamerContractBindingUpdate:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerContractBindingUpdate.endpoint = RestreamerContractBinding(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляра сущности по первичному ключу")
    
    def test_update_by_id(self, contract_id):
        id_ = self.endpoint.get_random()['id']

        resp = self.endpoint.update(json={
            "values": {"id": id_, "contract_id": contract_id}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        r = self.endpoint.get_by_id(id_).json()
        LOGGER.info(f"Update: {r}")
        AssertThat(r['result'][0]['contract_id']).IsEqualTo(contract_id)



    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляров сущности по фильтру")
    
    def test_bulk_update_by_filter(self, contract_id):
        r = self.endpoint.get(json={ # Получим первые 3 объекта
            "limit": 3,
            "columns": ["id"]
        }).json()['result']
        ids = [ _['id'] for _ in r ]
        LOGGER.info(f"Fetched ids: {ids}")

        cond = [{ "attribute": "id", "operator": "in", "value": ids }]
        body = {
            "values": [{"contract_id": contract_id}],
            "filter_by": cond
        }

        resp = self.endpoint.update_by_filter(json=body).json()['result']
        AssertThat(resp).IsEqualTo(3)

        resp = self.endpoint.get(json={
            "columns": ["contract_id"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['contract_id']).IsEqualTo(contract_id)


import pytest
import allure 
from helper import LOGGER
from endpoint import RestreamerContractBinding
from truth.truth import AssertThat


class TestRestreamerContractBindingDelete:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerContractBindingDelete.endpoint = RestreamerContractBinding(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Delete")
    @allure.title("Удаление одного экземляра сущности")
    
    def test_delete_one(self, faker, restreamer_id, contract_id):
        body = {
            "values": { "restreamer_id": restreamer_id, "contract_id": contract_id }
        }

        id_ = self.endpoint.add(json=body).json()['result']
        LOGGER.info(f"New id: {id_}")

        r = self.endpoint.delete(json={
            "filter_by": {
                "attribute": "id", "operator": "=", "value": id_
            }
        })
        resp = r.json()['result']
        AssertThat(resp).IsTrue()

        resp = self.endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).IsEmpty()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Delete")
    @allure.title("Множественное удаление экземляров сущности")
    
    def test_delete_many(self, faker, restreamer_id, contract_id):
        body = {
            "values": [
                { "restreamer_id": restreamer_id, "contract_id": contract_id },
                { "restreamer_id": restreamer_id, "contract_id": contract_id },
                { "restreamer_id": restreamer_id, "contract_id": contract_id }
            ]
        }

        ids = self.endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")

        cond = { "filter_by": { "attribute": "id", "operator": "in", "value": ids }}
        resp = self.endpoint.delete(json=cond).json()['result']
        
        AssertThat(resp).IsTrue()

        resp = self.endpoint.get(json=cond).json()['result']
        AssertThat(resp).IsEmpty()
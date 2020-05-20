import pytest
import allure 
from helper import LOGGER
from endpoint import RestreamerContractBindingToStage, RestreamerContractBinding
from truth.truth import AssertThat

class TestRestreamerContractBindingAdd:

    ids = None

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerContractBindingAdd.endpoint = RestreamerContractBinding(session)


    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self):
        yield
        if self.ids is not None:
            LOGGER.info(f"Deleting {self.ids} ...")
            r = self.endpoint.delete(json={
                "filter_by": {
                    "attribute": "id", "operator": "in", "value": self.ids
                }
            })
            LOGGER.info(f"\t OK {r.json()}")


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Add")
    @allure.title("Добавление одного экземляра сущности")
    
    def test_add_one(self, restreamer_id, contract_id, faker):
        body = {
            "values": {
                "restreamer_id": restreamer_id,
                "contract_id": contract_id
            }
        }

        r = self.endpoint.add(json=body).json()
        LOGGER.info(f"Add: {r}")
        id_ = r['result']
        self.ids = [id_] # запоминаем для удаления

        resp = self.endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['restreamer_id']).IsEqualTo(restreamer_id)
        AssertThat(resp['contract_id']).IsEqualTo(contract_id)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Add")
    @allure.title("Множественное добавление экземляров сущности")
    
    def test_add_many(self, restreamer_id, contract_id, faker):
        body = {
            "values": [
                { "restreamer_id": restreamer_id, "contract_id": contract_id },
                { "restreamer_id": restreamer_id, "contract_id": contract_id }]
        }

        r = self.endpoint.add(json=body).json()
        LOGGER.info(f"Add: {r}")
        ids = r['result']
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i,_ in enumerate(body['values']):
            resp = self.endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['restreamer_id']).IsEqualTo(restreamer_id)
            AssertThat(resp['contract_id']).IsEqualTo(contract_id)

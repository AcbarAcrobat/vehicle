import pytest
import allure 
from helper import LOGGER
from endpoint import RestreamerType
from truth.truth import AssertThat


class TestRestreamerTypeAdd:

    ids = None 

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerTypeAdd.endpoint = RestreamerType(session)


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
    @allure.suite("Restreamer type")
    @allure.sub_suite("Add")
    @allure.title("Добавление одного экземляра сущности")
    
    def test_add_one(self, faker):
        body = {
            "values": { "title": faker.uuid4() }
        }

        r = self.endpoint.add(json=body)
        LOGGER.info(r.json())

        id_ = r.json()['result']
        LOGGER.info(f"New id: {id_}")
        self.ids = [id_] # запоминаем для удаления

        resp = self.endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['title']).IsEqualTo(body['values']['title'])


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Add")
    @allure.title("Множественное добавление экземляров сущности")
    
    def test_add_many(self, faker):
        body = {
            "values": [
                { "title": faker.uuid4() },
                { "title": faker.uuid4() }
            ]
        }

        ids = self.endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = self.endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['title']).IsEqualTo(params['title'])

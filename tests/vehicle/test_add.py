import pytest
import allure
from helper import LOGGER
from endpoint import Vehicle
from truth.truth import AssertThat


class TestAdd:

    ids = None

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self, endpoint):
        yield
        endpoint.delete_by_ids(self.ids)

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint):
        body = {
            "values": {
                "type_id": 1, "login": faker.uuid4()
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())

        id_ = r.json()['result']
        LOGGER.info(f"New id: {id_}")
        self.ids = [id_]

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['type_id']).IsEqualTo(body['values']['type_id'])
        AssertThat(resp['login']).IsEqualTo(body['values']['login'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint):
        body = {
            "values": [
                {"type_id": 1, "login": faker.uuid4()},
                {"type_id": 2, "login": faker.uuid4()}
            ]
        }

        ids = endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['type_id']).IsEqualTo(params['type_id'])
            AssertThat(resp['login']).IsEqualTo(params['login'])

import pytest
import allure
from helper import LOGGER
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
                "name": faker.uuid4(),
                "image": f"images/{faker.uuid4()}.svg",
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        id_ = r.json()['result']
        LOGGER.info(f"New entity id: {id_}")
        self.ids = [id_]

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['name']).IsEqualTo(body['values']['name'])
        AssertThat(resp['image']).IsEqualTo(body['values']['image'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint):
        body = {
            "values": [{
                "name": faker.uuid4(),
                "image": f"images/{faker.uuid4()}.svg",
            }, {
                "name": faker.uuid4(),
                "image": f"images/{faker.uuid4()}.svg"
            }]
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        ids = r.json()['result']
        LOGGER.info(f"New entity ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['name']).IsEqualTo(params['name'])
            AssertThat(resp['image']).IsEqualTo(params['image'])

import pytest
import allure
from helper import LOGGER
from endpoint import UserLogs
from truth.truth import AssertThat
from datetime import datetime


class TestUserLogsAdd:

    ids = None

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self, endpoint):
        yield
        endpoint.delete_by_ids(self.ids)

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint, event_id):
        body = {
            "values": {
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [faker.uuid4() for i in range(5)],
                "event_id": event_id,
                "intention": {
                    "foo": {"bar": "baz"}
                }
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())

        id_ = r.json()['result']
        LOGGER.info(f"New id: {id_}")
        self.ids = [id_]  # запоминаем для удаления

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['created_at']).IsEqualTo(body['values']['created_at'])
        AssertThat(resp['user_id']).IsEqualTo(body['values']['user_id'])
        AssertThat(resp['entity']).IsEqualTo(body['values']['entity'])
        AssertThat(resp['result']).IsEqualTo(body['values']['result'])
        AssertThat(resp['event_id']).IsEqualTo(event_id)
        AssertThat(resp['intention']).IsEqualTo(body['values']['intention'])


    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint, event_id):
        body = {
            "values": [{
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [faker.uuid4() for i in range(5)],
                "event_id": event_id,
                "intention": {
                    "foo": {"bar": "baz"}
                }
            }, {
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [faker.uuid4() for i in range(5)],
                "event_id": event_id,
                "intention": {
                    "foo": {"bar": "baz"}
                }
            }]
        }

        ids = endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['created_at']).IsEqualTo(params['created_at'])
            AssertThat(resp['user_id']).IsEqualTo(params['user_id'])
            AssertThat(resp['entity']).IsEqualTo(params['entity'])
            AssertThat(resp['result']).IsEqualTo(params['result'])
            AssertThat(resp['intention']).IsEqualTo(params['intention'])
            AssertThat(resp['event_id']).IsEqualTo(event_id)

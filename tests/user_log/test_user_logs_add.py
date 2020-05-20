import pytest
import allure 
from helper import LOGGER
from endpoint import UserLogs
from truth.truth import AssertThat
from datetime import datetime


class TestUserLogsAdd:

    ids = None 

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestUserLogsAdd.endpoint = UserLogs(session)


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
    @allure.suite("User logs")
    @allure.sub_suite("Add")
    @allure.title("Добавление одного экземляра сущности")
    
    def test_add_one(self, faker, event_id):
        body = {
            "values": {
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [ faker.uuid4() for i in range(5) ],
                "event_id": event_id,
                "intention": {
                    "foo": { "bar": "baz" }
                }
            }
        }

        r = self.endpoint.add(json=body)
        LOGGER.info(r.json())

        id_ = r.json()['result']
        LOGGER.info(f"New id: {id_}")
        self.ids = [id_] # запоминаем для удаления

        resp = self.endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['created_at']).IsEqualTo(body['values']['created_at'])
        AssertThat(resp['user_id']).IsEqualTo(body['values']['user_id'])
        AssertThat(resp['entity']).IsEqualTo(body['values']['entity'])
        AssertThat(resp['result']).IsEqualTo(body['values']['result'])
        AssertThat(resp['event_id']).IsEqualTo(event_id)
        AssertThat(resp['intention']).IsEqualTo(body['values']['intention'])


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Add")
    @allure.title("Множественное добавление экземляров сущности")
    
    def test_add_many(self, faker, event_id):
        body = {
            "values": [{
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [ faker.uuid4() for i in range(5) ],
                "event_id": event_id,
                "intention": {
                    "foo": { "bar": "baz" }
                }
            },{
                "created_at": round(datetime.utcnow().timestamp()*1000),
                "user_id": faker.random_number(),
                "entity": faker.uuid4(),
                "result": [ faker.uuid4() for i in range(5) ],
                "event_id": event_id,
                "intention": {
                    "foo": { "bar": "baz" }
                }
            }]
        }

        ids = self.endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = self.endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['created_at']).IsEqualTo(params['created_at'])
            AssertThat(resp['user_id']).IsEqualTo(params['user_id'])
            AssertThat(resp['entity']).IsEqualTo(params['entity'])
            AssertThat(resp['result']).IsEqualTo(params['result'])
            AssertThat(resp['intention']).IsEqualTo(params['intention'])
            AssertThat(resp['event_id']).IsEqualTo(event_id)

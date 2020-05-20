import pytest
import allure 
from helper import LOGGER
from endpoint import RestreamerType
from truth.truth import AssertThat


class TestRestreamerTypeUpdate:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerTypeUpdate.endpoint = RestreamerType(session)


    @pytest.fixture(scope='class')
    def new_entity(self, faker):
        body = {
            "values": [
                { "title": faker.uuid4() },
                { "title": faker.uuid4() }
        ]}
        r = self.endpoint.add(json=body)
        ids = r.json()['result']
        LOGGER.info(f"New ids: {ids}")
        yield ids
        LOGGER.info(f"Deleting {ids}")
        r = self.endpoint.delete(json={
            "filter_by": {
                "attribute": "id", "operator": "in", "value": ids
            }
        })


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляра сущности по первичному ключу")
    
    def test_update_by_id(self, faker, new_entity):
        new_title = faker.uuid4()
        r = self.endpoint.update(json={
            "values": {"id": new_entity[0], "title": new_title}
        }).json()
        LOGGER.info(f"Update: {r}")
        AssertThat(r['result']).IsEqualTo(1)

        r = self.endpoint.get_by_id(new_entity[0])
        LOGGER.info(r.content)
        title = r.json()['result'][0]['title']
        AssertThat(title).IsEqualTo(new_title)



    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляров сущности по фильтру")
    
    def test_bulk_update_by_filter(self, faker, new_entity):
        new_title = faker.uuid4()

        cond = [{ "attribute": "id", "operator": "in", "value": new_entity }]
        body = {
            "values": [{"title": new_title}],
            "filter_by": cond
        }

        resp = self.endpoint.update_by_filter(json=body).json()['result']
        AssertThat(resp).IsEqualTo(2)

        resp = self.endpoint.get(json={
            "columns": ["id", "title"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['title']).IsEqualTo(new_title)


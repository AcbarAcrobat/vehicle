import pytest
import allure 
from helper import LOGGER
from endpoint import Restreamer
from truth.truth import AssertThat


class TestRestreamerUpdate:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerUpdate.endpoint = Restreamer(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляра сущности по первичному ключу")
    
    def test_update_by_id(self, faker):
        id_ = self.endpoint.get_random()['id']

        new_title = faker.uuid4()
        resp = self.endpoint.update(json={
            "values": {"id": id_, "title": new_title}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        r = self.endpoint.get_by_id(id_)
        LOGGER.info(r.content)
        title = r.json()['result'][0]['title']
        AssertThat(title).IsEqualTo(new_title)



    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer")
    @allure.sub_suite("Update")
    @allure.title("Обновление экземляров сущности по фильтру")
    
    def test_bulk_update_by_filter(self, faker):
        r = self.endpoint.get(json={ # Получим первые 3 объекта
            "limit": 3,
            "columns": ["id"]
        }).json()['result']
        ids = [ _['id'] for _ in r ]
        LOGGER.info(f"Fetched ids: {ids}")

        new_title = faker.uuid4()

        cond = [{ "attribute": "id", "operator": "in", "value": ids }]
        body = {
            "values": [{"title": new_title}],
            "filter_by": cond
        }

        resp = self.endpoint.update_by_filter(json=body).json()['result']
        AssertThat(resp).IsEqualTo(3)

        resp = self.endpoint.get(json={
            "columns": ["id", "title"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['title']).IsEqualTo(new_title)


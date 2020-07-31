import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehicleUpdate:

    @allure.title("Обновление экземляра сущности по первичному ключу")
    def test_update_by_id(self, endpoint, faker, data_vehicle):
        new_data = faker.uuid4()
        resp = endpoint.update(json={
            "values": {"id": data_vehicle["ids"][0], "login": new_data}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        login = endpoint.get_by_id(data_vehicle["ids"][0]).json()['result'][0]['login']
        AssertThat(login).IsEqualTo(new_data)


    @allure.title("Обновление экземляров сущности по фильтру")
    def test_bulk_update_by_filter(self, endpoint, faker, data_vehicle):
        new_data = faker.uuid4()

        cond = [{"attribute": "id", "operator": "in", "value": data_vehicle[:3]}]
        body = {
            "values": [{"login": new_data}],
            "filter_by": cond
        }

        resp = endpoint.update_by_filter(json=body).json()['result']
        AssertThat(resp).IsEqualTo(3)

        resp = endpoint.get(json={
            "columns": ["login"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['login']).IsEqualTo(new_data)

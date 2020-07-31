import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehicleToAttachedFileUpdate:

    @allure.title("Обновление экземляра сущности по первичному ключу")
    def test_update_by_id(self, endpoint, faker, new_entity, body):
        new_data = f"{faker.uuid4()}.doc"
        resp = endpoint.update(json={
            "values": {"id": new_entity[0], "file_name": new_data}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        file_name = endpoint.get_by_id(new_entity[0]).json()['result'][0]['file_name']
        AssertThat(file_name).IsEqualTo(new_data)


    @allure.title("Обновление экземляров сущности по фильтру")
    def test_bulk_update_by_filter(self, endpoint, faker, new_entity, body):
        new_data = f"{faker.uuid4()}.doc"

        cond = [{"attribute": "id", "operator": "in", "value": new_entity}]
        body_ = {
            "values": [{"file_name": new_data}],
            "filter_by": cond
        }

        resp = endpoint.update_by_filter(json=body_).json()['result']
        AssertThat(resp).IsEqualTo(2)

        resp = endpoint.get(json={
            "columns": ["file_name"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['file_name']).IsEqualTo(new_data)

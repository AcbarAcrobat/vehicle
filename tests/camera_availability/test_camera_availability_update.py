import pytest
import allure
from helper import LOGGER
from endpoint import CameraAvailability
from truth.truth import AssertThat


class TestCameraAvailabilityUpdate:

    @allure.title("Обновление экземляра сущности по первичному ключу")
    def test_update_by_id(self, endpoint, faker, new_entity, body):
        new_data = faker.uuid4()
        resp = endpoint.update(json={
            "values": {"id": new_entity[0], "description": new_data}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        description = endpoint.get_by_id(new_entity[0]).json()['result'][0]['description']
        AssertThat(description).IsEqualTo(new_data)


    @allure.title("Обновление экземляров сущности по фильтру")
    def test_bulk_update_by_filter(self, endpoint, faker, new_entity, body):
        new_data = faker.uuid4()

        cond = [{"attribute": "id", "operator": "in", "value": new_entity}]
        body_ = {
            "values": [{"description": new_data}],
            "filter_by": cond
        }

        resp = endpoint.update_by_filter(json=body_).json()['result']
        AssertThat(resp).IsEqualTo(2)

        resp = endpoint.get(json={
            "columns": ["description"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['description']).IsEqualTo(new_data)

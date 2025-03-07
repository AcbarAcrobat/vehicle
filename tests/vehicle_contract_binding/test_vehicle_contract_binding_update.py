import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehicleContractBindingUpdate:

    @allure.title("Обновление экземляра сущности по первичному ключу")
    def test_update_by_id(self, endpoint, faker, new_entity, body):
        new_data = faker.random_digit_not_null()
        resp = endpoint.update(json={
            "values": {"id": new_entity[0], "contract_id": new_data}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        contract_id = endpoint.get_by_id(new_entity[0]).json()['result'][0]['contract_id']
        AssertThat(contract_id).IsEqualTo(new_data)


    @allure.title("Обновление экземляров сущности по фильтру")
    def test_bulk_update_by_filter(self, endpoint, faker, new_entity, body):
        new_data = faker.random_digit_not_null()

        cond = [{"attribute": "id", "operator": "in", "value": new_entity}]
        body_ = {
            "values": [{"contract_id": new_data}],
            "filter_by": cond
        }

        resp = endpoint.update_by_filter(json=body_).json()['result']
        AssertThat(resp).IsEqualTo(3)

        resp = endpoint.get(json={
            "columns": ["contract_id"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['contract_id']).IsEqualTo(new_data)

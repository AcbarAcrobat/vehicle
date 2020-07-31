import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat
from endpoint import Vehicle


class TestVehiclePartUpdate:

    @allure.title("Обновление экземляра сущности по первичному ключу")
    def test_update_by_id(self, session, endpoint, faker, new_entity, body, data_vehicle):
        # vehicle_id = Vehicle(session).get_random()['id']
        vehicle_id = data_vehicle["ids"][0]
        resp = endpoint.update(json={
            "values": {"id": new_entity[0], "vehicle_id": vehicle_id}
        }).json()['result']

        AssertThat(resp).IsEqualTo(1)

        description = endpoint.get_by_id(new_entity[0]).json()['result'][0]['vehicle_id']
        AssertThat(description).IsEqualTo(vehicle_id)


    @allure.title("Обновление экземляров сущности по фильтру")
    def test_bulk_update_by_filter(self, session, endpoint, faker, new_entity, body, data_vehicle):
        # vehicle_id = Vehicle(session).get_random()['id']
        vehicle_id = data_vehicle["ids"][0]

        cond = [{"attribute": "id", "operator": "in", "value": new_entity}]
        body_ = {
            "values": [{"vehicle_id": vehicle_id}],
            "filter_by": cond
        }

        resp = endpoint.update_by_filter(json=body_).json()['result']
        AssertThat(resp).IsEqualTo(2)

        resp = endpoint.get(json={
            "columns": ["vehicle_id"],
            "filter_by": cond
        }).json()['result']

        LOGGER.info(f"Updated objects: {resp}")

        for data in resp:
            AssertThat(data['vehicle_id']).IsEqualTo(vehicle_id)

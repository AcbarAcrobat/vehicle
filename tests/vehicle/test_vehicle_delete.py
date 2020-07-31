import pytest
import allure
from helper import LOGGER
from endpoint import Vehicle
from truth.truth import AssertThat


class TestDelete:

    @allure.title("Удаление одного экземляра сущности")
    def test_delete_one(self, faker, endpoint, data_vehicle, data_vehicle_type, data_vehicle_template):
        body = {
            "values": {
                "type_id": data_vehicle_type["ids"][0],
                "login": faker.uuid4(),
                "template_id": data_vehicle_template["ids"][0]
            }
        }

        id_ = endpoint.add(json=body).json()['result']
        LOGGER.info(f"New id: {id_}")

        r = endpoint.delete_by_ids([id_])
        resp = r.json()['result']
        AssertThat(resp).IsTrue()

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).IsEmpty()


    @allure.title("Множественное удаление экземляров сущности")
    def test_delete_many(self, faker, endpoint, data_vehicle, data_vehicle_type, data_vehicle_template):
        body = {
            "values": [
                {
                    "type_id": data_vehicle_type["ids"][0],
                    "login": faker.uuid4(),
                    "template_id": data_vehicle_template["ids"][0]
                },
                {
                    "type_id": data_vehicle_type["ids"][1],
                    "login": faker.uuid4(),
                    "template_id": data_vehicle_template["ids"][1]
                }
        ]}

        # ids = endpoint.add(json=body).json()['result']
        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        ids = r.json()['result']
        LOGGER.info(f"New ids: {ids}")

        cond = {"filter_by": {"attribute": "id", "operator": "in", "value": ids}}
        resp = endpoint.delete_by_ids(ids).json()['result']

        AssertThat(resp).IsTrue()

        resp = endpoint.get(json=cond).json()['result']
        AssertThat(resp).IsEmpty()

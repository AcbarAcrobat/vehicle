import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestDelete:

    @allure.title("Удаление одного экземляра сущности")
    def test_delete_one(self, faker, endpoint):
        body = {
            "values": {"vehicle_id": faker.random_number(), "stage_id": faker.random_number()}
        }

        id_ = endpoint.add(json=body).json()['result']
        LOGGER.info(f"New: {id_}")

        cond = {
            "filter_by": [
                {"attribute": "vehicle_id", "operator": "=", "value": body["values"]["vehicle_id"]},
                {"attribute": "stage_id", "operator": "=", "value": body["values"]["stage_id"]}
            ]
        }
        r = endpoint.delete(json=cond)
        resp = r.json()['result']
        AssertThat(resp).IsTrue()

        resp = endpoint.get(json=cond).json()['result']
        AssertThat(resp).IsEmpty()


    @allure.title("Множественное удаление экземляров сущности")
    def test_delete_many(self, faker, endpoint):
        body = {
            "values": [
                {"vehicle_id": faker.random_number(), "stage_id": faker.random_number()},
                {"vehicle_id": faker.random_number(), "stage_id": faker.random_number()}]
        }
        # ids = endpoint.add(json=body).json()['result']
        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        ids = r.json()['result']

        count_before = endpoint.count()
        LOGGER.info(f"New: {ids}")

        for params in body["values"]:
            cond = {
                "filter_by": [
                    {"attribute": "vehicle_id", "operator": "=", "value": params["vehicle_id"]},
                    {"attribute": "stage_id", "operator": "=", "value": params["stage_id"]}
                ]
            }
            endpoint.delete(json=cond).json()['result']

        AssertThat(endpoint.count()).IsEqualTo(count_before - 2)
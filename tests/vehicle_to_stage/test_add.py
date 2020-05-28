import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestAdd:

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint):
        body = {
            "values": {
                "vehicle_id": faker.random_number(), "stage_id": faker.random_number()
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        resp = endpoint.get(json={
            "filter_by": [
                {"attribute": "vehicle_id", "operator": "=", "value": body["values"]["vehicle_id"]},
                {"attribute": "stage_id", "operator": "=", "value": body["values"]["stage_id"]}
            ]
        }).json()['result']

        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['vehicle_id']).IsEqualTo(body['values']['vehicle_id'])
        AssertThat(resp['stage_id']).IsEqualTo(body['values']['stage_id'])
        

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint):
        body = {
            "values": [
                {"vehicle_id": faker.random_number(), "stage_id": faker.random_number()},
                {"vehicle_id": faker.random_number(), "stage_id": faker.random_number()}]
        }
        count_before = endpoint.count()

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)
        AssertThat(endpoint.count()).IsEqualTo(count_before + 2)

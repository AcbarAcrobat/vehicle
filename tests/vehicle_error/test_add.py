import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat
from datetime import datetime as dt


class TestAdd:

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint, vehicle_id):
        body = {
            "values": {
                "code": faker.random_digit_not_null(),
                "vehicle_id": vehicle_id,
                "occurred_at": int(faker.numerify("##########"))
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        resp = r.json()['result']
        LOGGER.info(f"New entity: {resp}")

        resp = endpoint.get_by("occurred_at", body['values']['occurred_at']).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['code']).IsEqualTo(body['values']['code'])
        AssertThat(resp['vehicle_id']).IsEqualTo(body['values']['vehicle_id'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint, vehicle_id):
        body = {
            "values": [{
                "code": faker.random_digit_not_null(),
                "vehicle_id": vehicle_id,
                "occurred_at": int(faker.numerify("##########"))
            }, {
                "code": faker.random_digit_not_null(),
                "vehicle_id": vehicle_id,
                "occurred_at": int(faker.numerify("##########"))
            }
        ]}

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        resp = r.json()['result']
        LOGGER.info(f"New entity: {resp}")
        AssertThat(resp).HasSize(2)


        for i, params in enumerate(body['values']):
            resp = endpoint.get_by("occurred_at", params['occurred_at']).json()['result'][0]
            AssertThat(resp['code']).IsEqualTo(params['code'])
            AssertThat(resp['vehicle_id']).IsEqualTo(params['vehicle_id'])

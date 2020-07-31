import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehicleToAttachedFileDelete:

    @allure.title("Удаление одного экземляра сущности")
    def test_delete_one(self, faker, endpoint, vehicle_id):
        body = {
            "values": {
                "file_id": faker.random_number(),
                "vehicle_id": vehicle_id,
                "file_name": f"{faker.uuid4()}.pdf"
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
    def test_delete_many(self, faker, endpoint, vehicle_id):
        body = {
            "values": [{
                "file_id": faker.random_number(),
                "vehicle_id": vehicle_id,
                "file_name": f"{faker.uuid4()}.pdf"
            }, {
                "file_id": faker.random_number(),
                "vehicle_id": vehicle_id,
                "file_name": f"{faker.uuid4()}.pdf"
            }]
        }

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

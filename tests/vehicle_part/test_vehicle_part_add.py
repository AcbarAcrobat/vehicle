import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehiclePartAdd:

    ids = None

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self, endpoint):
        yield
        endpoint.delete_by_ids(self.ids)

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint, vehicle_id, part_type_id):
        body = {
            "values": {
                "vehicle_id": vehicle_id, "part_type_id": part_type_id
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())

        id_ = r.json()['result']
        LOGGER.info(f"New id: {id_}")
        self.ids = [id_]

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['vehicle_id']).IsEqualTo(body['values']['vehicle_id'])
        AssertThat(resp['part_type_id']).IsEqualTo(body['values']['part_type_id'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint, vehicle_id, part_type_id):
        body = {
            "values": [
                {"vehicle_id": vehicle_id, "part_type_id": part_type_id},
                {"vehicle_id": vehicle_id, "part_type_id": part_type_id}
            ]
        }

        # ids = endpoint.add(json=body).json()['result']
        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        ids = r.json()['result']
        LOGGER.info(f"New ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['vehicle_id']).IsEqualTo(params['vehicle_id'])
            AssertThat(resp['part_type_id']).IsEqualTo(params['part_type_id'])

import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestVehicleCameraAdd:

    ids = None

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self, endpoint):
        yield
        endpoint.delete_by_ids(self.ids)

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint, part_id):
        LOGGER.warning(part_id)
        body = {
            "values": {
                "part_id": part_id, "camera_position": {"x": 1, "y": 2, "scope": 3, "azimut": 4}, "camera_position_id": 1
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
        AssertThat(resp['part_id']).IsEqualTo(body['values']['part_id'])
        AssertThat(resp['camera_position']).IsEqualTo(body['values']['camera_position'])
        AssertThat(resp['camera_position_id']).IsEqualTo(body['values']['camera_position_id'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint, part_id):
        body = {
            "values": [
                {"part_id": part_id, "camera_position": {"x": 1, "y": 2, "scope": 3, "azimut": 4}, "camera_position_id": 1},
                {"part_id": part_id, "camera_position": {"x": 1, "y": 2, "scope": 3, "azimut": 4}, "camera_position_id": 1}
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
            AssertThat(resp['part_id']).IsEqualTo(params['part_id'])
            AssertThat(resp['camera_position']).IsEqualTo(params['camera_position'])
            AssertThat(resp['camera_position_id']).IsEqualTo(params['camera_position_id'])

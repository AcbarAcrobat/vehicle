import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestDelete:

    @allure.title("Удаление одного экземляра сущности")
    def test_delete_one(self, faker, endpoint, part_id):
        body = {
            "values": {
                "part_id": part_id, "camera_position": {"x": 11, "y": 12, "scope": 13, "azimut": 14}, "camera_position_id": 1
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
    def test_delete_many(self, faker, endpoint, part_id):
        body = {
            "values": [
                {"part_id": part_id, "camera_position": {"x": 11, "y": 12, "scope": 13, "azimut": 14}, "camera_position_id": 1},
                {"part_id": part_id, "camera_position": {"x": 11, "y": 12, "scope": 13, "azimut": 14}, "camera_position_id": 1},
        ]}

        ids = endpoint.add(json=body).json()['result']
        LOGGER.info(f"New ids: {ids}")

        cond = {"filter_by": {"attribute": "id", "operator": "in", "value": ids}}
        resp = endpoint.delete_by_ids(ids).json()['result']

        AssertThat(resp).IsTrue()

        resp = endpoint.get(json=cond).json()['result']
        AssertThat(resp).IsEmpty()

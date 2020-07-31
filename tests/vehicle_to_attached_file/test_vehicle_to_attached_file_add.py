import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat


class TestAdd:

    ids = None

    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self, endpoint):
        yield
        endpoint.delete_by_ids(self.ids)

    @allure.title("Добавление одного экземляра сущности")
    def test_add_one(self, faker, endpoint, data_vehicle, data_loaded_file_vehicle):
        body = {
            "values": {
                "file_id": data_loaded_file_vehicle["ids"][0],
                "vehicle_id": data_vehicle["ids"][0],
                "file_name": f"{faker.uuid4()}.pdf"
            }
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        id_ = r.json()['result']
        LOGGER.info(f"New entity id: {id_}")
        self.ids = [id_]

        resp = endpoint.get_by_id(id_).json()['result']
        AssertThat(resp).HasSize(1)

        resp = resp[0]
        AssertThat(resp['file_id']).IsEqualTo(body['values']['file_id'])
        AssertThat(resp['vehicle_id']).IsEqualTo(body['values']['vehicle_id'])
        AssertThat(resp['file_name']).IsEqualTo(body['values']['file_name'])

    @allure.title("Множественное добавление экземляров сущности")
    def test_add_many(self, faker, endpoint, data_vehicle, data_loaded_file_vehicle):
        body = {
            "values": [{
                "file_id": data_loaded_file_vehicle["ids"][0],
                "vehicle_id": data_vehicle["ids"][0],
                "file_name": f"{faker.uuid4()}.pdf"
            }, {
                "file_id": data_loaded_file_vehicle["ids"][1],
                "vehicle_id": data_vehicle["ids"][1],
                "file_name": f"{faker.uuid4()}.pdf"
            }]
        }

        r = endpoint.add(json=body)
        LOGGER.info(r.json())
        AssertThat(r.status_code).IsEqualTo(200)

        ids = r.json()['result']
        LOGGER.info(f"New entity ids: {ids}")
        AssertThat(ids).HasSize(2)
        self.ids = ids

        for i, params in enumerate(body['values']):
            resp = endpoint.get_by_id(ids[i]).json()['result'][0]
            AssertThat(resp['file_id']).IsEqualTo(params['file_id'])
            AssertThat(resp['vehicle_id']).IsEqualTo(params['vehicle_id'])
            AssertThat(resp['file_name']).IsEqualTo(params['file_name'])

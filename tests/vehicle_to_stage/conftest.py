import pytest
from endpoint import VehicleToStage
from helper.logger import LOGGER


@pytest.fixture(scope='class')
def endpoint(session):
    yield VehicleToStage(session)


# @pytest.fixture(scope='function')
# def body(faker):
#     yield {
#         "values": [{
#             "stage_id": faker.random_digit_not_null(),
#             "vehicle_id": faker.random_digit_not_null()
#         }, {
#             "stage_id": faker.random_digit_not_null(),
#             "vehicle_id": faker.random_digit_not_null()
#         }]
#     }


# @pytest.fixture(scope='function')
# def new_entity(endpoint, body):
#     ids = endpoint.add(json=body).json()['result']
#     LOGGER.info(f"New ids: {ids}")
#     yield ids
#     endpoint.delete_by_ids(ids)

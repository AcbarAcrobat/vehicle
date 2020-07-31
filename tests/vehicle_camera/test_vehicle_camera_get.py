import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_camera
from schema.base import skeleton, build
from endpoint import VehicleCamera, VehicleCameraError
from truth.truth import AssertThat


class TestGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_camera.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['stream_resolution_height', 'hls_second_stream_url']),
            (['rtsp_second_url', 'ip_address', 'id']),
            (['axxon_id', 'camera_position', 'error'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'точку'")
    def test_child_attribute_via_dot(self, endpoint):
        body = {
            'columns': ['error.code']
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_camera.vehicle_camera_fk_properties,
                "error": {
                    'anyOf': [
                        {'type': 'null'},
                        {
                            'type': 'array',
                            'items': build(vehicle_camera.error_fk_properties, ['code'])
                        }
                    ]
                }
            },
            ['error']
        ))
        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'вложенный объект'")
    def test_child_attribute_via_nested_entity(self, endpoint):
        body = {
            "columns": [
                {"entity": "vehicle_camera_error", "columns": ["code"]}
            ]
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_camera.vehicle_camera_fk_properties,
                "error": {
                    'anyOf': [
                        {'type': 'null'},
                        {
                            'type': 'array',
                            'items': build(vehicle_camera.error_fk_properties, ['code'])
                        }
                    ]
                }
            },
            ['error']
        ))

        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera.structural_schema())

    @allure.title("Двойная звезочка также применима к дочерним сущностям")
    def test_get_child_entity_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['error.**']
        }
        r = endpoint.get(json=body)

        validate(r.json(), vehicle_camera.structural_schema(['error']))

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint, new_entity, body):
        body = {
            "filter_by": [{"attribute": "id", "operator": ">=", "value": new_entity[0]}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i).IsAtLeast(new_entity[0]) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint, new_entity, body):
        body = {
            "filter_by": [
                {"attribute": "id", "operator": ">=", "value": new_entity[0]},
                {"attribute": "camera_position_id", "operator": "=", "value": 3}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['id']).IsAtLeast(new_entity[0])
            AssertThat(data['camera_position_id']).IsEqualTo(3)

    @allure.title("Получение списка экземляров сущности по условию дочерней сущности")
    def test_filter_by_child_attribute(self, session, endpoint, data_vehicle_camera_error):
        # child_id = VehicleCameraError(session).get_random()['vehicle_camera_id']
        child_id = data_vehicle_camera_error["body"]["values"][0]["vehicle_camera_id"]
        LOGGER.info(f'VehicleError: {child_id}')

        body = {
            "filter_by": {"attribute": "error.vehicle_camera_id", "operator": "=", "value": child_id}
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']
        LOGGER.info(f'Vehicle: {resp}')

        for data in resp:
            AssertThat(data['error']).Contains(child_id)

    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    def test_filter_by_even_id(self, endpoint, new_entity):
        body = {
            "filter_by": [{"attribute": {"operator": "%", "attribute": "id", "value": 2}, "operator": "=", "value": 0}],
            "columns": ["id"]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i % 2).IsEqualTo(0) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, endpoint, new_entity):
        body = {
            "search_by": [
                {"attribute": "id", "operator": ">=", "value": new_entity[0]},
                {"attribute": "camera_position_id", "operator": "=", "value": 3}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            id_ = data['id']
            camera_position_id = data['camera_position_id']
            if id_ < new_entity[0] and camera_position_id != 3:
                raise AssertionError(f'Not true that {id_} >= {new_entity[0]} OR {camera_position_id} == 3')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, new_entity, endpoint):
        body = {
            "columns": ["id"],
            "order_by": ["id"]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['id'] for _ in resp]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    def test_order_by_descending(self, new_entity, endpoint):
        body = {
            "columns": ["id"],
            "order_by": [{"column": "id", "ascending": False}]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['id'] for _ in resp]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка экземляров сущности со смещением")
    def test_offset(self, endpoint):
        body = {
            "columns": ["id"],
            "limit": 3
        }
        r = endpoint.get(json=body)
        resp_limit_3 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_3)

        body['limit'] = 2
        body['offset'] = 1

        r = endpoint.get(json=body)
        resp_limit_2 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_3[1:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

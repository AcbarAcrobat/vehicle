import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_part
from schema.base import skeleton, build
from endpoint import VehicleCamera
from truth.truth import AssertThat


class TestGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_part.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['id']),
            (['vehicle_id']),
            (['part_type_id', 'cameras'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'точку'")
    def test_child_attribute_via_dot(self, endpoint):
        body = {
            'columns': ['cameras.camera_availability_id']
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_part.vehicle_part_fk_properties,
                "cameras": {
                    'camera_availability_id': {"type": "integer"}
                }
            },
            ['cameras']
        ))
        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'вложенный объект'")
    def test_child_attribute_via_nested_entity(self, endpoint):
        body = {
            "columns": [
                {"entity": "vehicle_camera", "columns": ["camera_availability_id"]}
            ]
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_part.vehicle_part_fk_properties,
                "cameras": {
                    'camera_availability_id': {"type": "integer"}
                }
            },
            ['cameras']
        ))
        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part.structural_schema())

    @allure.title("Двойная звезочка также применима к дочерним сущностям")
    def test_get_child_entity_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['cameras.**']
        }
        r = endpoint.get(json=body)

        validate(r.json(), vehicle_part.structural_schema(['cameras']))

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint):
        body = {
            "filter_by": [{"attribute": "id", "operator": "<=", "value": 2000}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i).IsAtMost(2000) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint, vehicle_id):
        body = {
            "filter_by": [
                {"attribute": "id", "operator": "<=", "value": 2000},
                {"attribute": "vehicle_id", "operator": "=", "value": vehicle_id}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['id']).IsAtMost(2000)
            AssertThat(data['vehicle_id']).IsEqualTo(vehicle_id)

    @allure.title("Получение списка экземляров сущности по условию дочерней сущности")
    def test_filter_by_child_attribute(self, session, endpoint):
        child_id = VehicleCamera(session).get_random()['id']
        LOGGER.info(f'VehicleCamera: {child_id}')

        body = {
            "filter_by": {"attribute": "cameras.id", "operator": "=", "value": child_id}
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']
        LOGGER.info(f'Vehicle: {resp}')

        for data in resp:
            AssertThat(data['cameras']).Contains(child_id)

    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    def test_filter_by_even_id(self, endpoint):
        body = {
            "filter_by": [{"attribute": {"operator": "%", "attribute": "id", "value": 2}, "operator": "=", "value": 0}],
            "columns": ["id"]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i % 2).IsEqualTo(0) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, endpoint, vehicle_id):
        body = {
            "search_by": [
                {"attribute": "id", "operator": "<=", "value": 2000},
                {"attribute": "vehicle_id", "operator": "=", "value": vehicle_id}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            id_ = data['id']
            vehicle_id_ = data['vehicle_id']
            if id_ > 2000 and vehicle_id_ != vehicle_id:
                raise AssertionError(f'Not true that {id_} <= 2000 OR {vehicle_id_} == {vehicle_id}')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, endpoint):
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
    def test_order_by_descending(self, endpoint):
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

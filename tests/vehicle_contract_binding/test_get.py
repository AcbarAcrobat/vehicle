import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_contract_binding
from schema.base import skeleton, build
from truth.truth import AssertThat
from endpoint import VehicleContractBindingToStage


class TestGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_contract_binding.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['id']),
            (['vehicle_id']),
            (['contract_id'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_contract_binding.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'точку'")
    def test_child_attribute_via_dot(self, endpoint):
        body = {
            'columns': ['stages.vehicle_contract_binding_id']
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_contract_binding.vehicle_contract_binding_fk_properties,
                "stages": {
                    'type': 'array',
                    'items': build(vehicle_contract_binding.stages_fk_properties, ['vehicle_contract_binding_id'])
                }
            },
            ['stages']
        ))
        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'вложенный объект'")
    def test_child_attribute_via_nested_entity(self, endpoint):
        body = {
            "columns": [
                {"entity": "vehicle_contract_binding_to_stage", "columns": ["vehicle_contract_binding_id"]}
            ]
        }
        r = endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** vehicle_contract_binding.vehicle_contract_binding_fk_properties,
                "stages": {
                    'type': 'array',
                    'items': build(vehicle_contract_binding.stages_fk_properties, ['vehicle_contract_binding_id'])
                }
            },
            ['stages']
        ))
        validate(r.json(), schema_)

        validate(r.json(), schema_)

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_contract_binding.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_contract_binding.structural_schema())

    @allure.title("Двойная звезочка также применима к дочерним сущностям")
    def test_get_child_entity_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['stages.**']
        }
        r = endpoint.get(json=body)

        validate(r.json(), vehicle_contract_binding.structural_schema(['stages']))

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint):
        body = {
            "filter_by": [{"attribute": "contract_id", "operator": "<=", "value": 3000}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['contract_id'] for r in resp]

        [AssertThat(i).IsAtMost(3000) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint):
        body = {
            "filter_by": [
                {"attribute": "contract_id", "operator": "<=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 100}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['contract_id']).IsAtMost(3000)
            AssertThat(data['id']).IsAtMost(100)

    @allure.title("Получение списка экземляров сущности по условию дочерней сущности")
    def test_filter_by_child_attribute(self, session, endpoint):
        child_id = VehicleContractBindingToStage(session).get_random()['stage_id']
        LOGGER.info(f'VehicleContractBindingToStage: {child_id}')

        body = {
            "filter_by": {"attribute": "stages.stage_id", "operator": "=", "value": child_id}
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']
        LOGGER.info(f'VehicleContractBinding: {resp}')

        for data in resp:
            AssertThat(data['stages']).Contains(child_id)

    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    def test_filter_by_even_id(self, endpoint):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "id", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['id']
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i % 2).IsEqualTo(0) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, endpoint):
        body = {
            "search_by": [
                {"attribute": "contract_id", "operator": "<=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 100}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            contract_id = data['contract_id']
            id_ = data['id']
            if contract_id > 3000 and id_ > 100:
                raise AssertionError(f'Not true that {id_} <= 100 OR {contract_id} <= 3000')

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
            "limit": 4
        }
        r = endpoint.get(json=body)
        resp_limit_4 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = endpoint.get(json=body)
        resp_limit_2 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

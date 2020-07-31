import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_to_stage
from schema.base import skeleton, build
from truth.truth import AssertThat


class TestVehicleToStageGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_to_stage.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['vehicle_id']),
            (['stage_id']),
            (['stage_id', 'vehicle_id'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_to_stage.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["vehicle_id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['vehicle_id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_to_stage.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_to_stage.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint, data_vehicle_to_stage):
        vehicle_id = data_vehicle_to_stage["body"]["values"][0]["vehicle_id"]
        body = {
            "filter_by": [{"attribute": "vehicle_id", "operator": ">=", "value": vehicle_id}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['vehicle_id'] for r in resp]

        [AssertThat(i).IsAtLeast(vehicle_id) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint, data_vehicle_to_stage):
        vehicle_id = data_vehicle_to_stage["body"]["values"][0]["vehicle_id"]
        stage_id = data_vehicle_to_stage["body"]["values"][4]["stage_id"]
        body = {
            "filter_by": [
                {"attribute": "vehicle_id", "operator": ">=", "value": vehicle_id},
                {"attribute": "stage_id", "operator": "<=", "value": stage_id}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['vehicle_id']).IsAtLeast(vehicle_id)
            AssertThat(data['stage_id']).IsAtMost(stage_id)

    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    def test_filter_by_even_id(self, endpoint):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "vehicle_id", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['vehicle_id']
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['vehicle_id'] for r in resp]

        [AssertThat(i % 2).IsEqualTo(0) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, endpoint, data_vehicle_to_stage):
        vehicle_id = data_vehicle_to_stage["body"]["values"][0]["vehicle_id"]
        stage_id = data_vehicle_to_stage["body"]["values"][4]["stage_id"]
        body = {
            "search_by": [
                {"attribute": "vehicle_id", "operator": ">=", "value": vehicle_id},
                {"attribute": "stage_id", "operator": "<=", "value": stage_id}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            v_id = data['vehicle_id']
            s_id = data['stage_id']
            if v_id < vehicle_id and s_id > stage_id:
                raise AssertionError(f'Not true that {v_id} >= {vehicle_id} OR {s_id} <= {stage_id}')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, endpoint):
        body = {
            "columns": ["vehicle_id"],
            "order_by": ["vehicle_id"]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['vehicle_id'] for _ in resp]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    def test_order_by_descending(self, endpoint):
        body = {
            "columns": ["vehicle_id"],
            "order_by": [{"column": "vehicle_id", "ascending": False}]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['vehicle_id'] for _ in resp]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка экземляров сущности со смещением")
    def test_offset(self, endpoint):
        body = {
            "columns": ["stage_id"],
            "limit": 4
        }
        r = endpoint.get(json=body)
        resp_limit_4 = [_['stage_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = endpoint.get(json=body)
        resp_limit_2 = [_['stage_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

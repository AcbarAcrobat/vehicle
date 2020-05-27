import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_error
from schema.base import skeleton, build
from truth.truth import AssertThat


class TestGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['vehicle_id']),
            (['code']),
            (['occurred_at'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_error.foreign_key_schema(columns))

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
        validate(r.json(), vehicle_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint):
        body = {
            "filter_by": [{"attribute": "code", "operator": "<=", "value": 10}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        codes = [r['code'] for r in resp]

        [AssertThat(i).IsAtMost(10) for i in codes]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint):
        body = {
            "filter_by": [
                {"attribute": "vehicle_id", "operator": "<=", "value": 91000},
                {"attribute": "code", "operator": "<=", "value": 10}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['vehicle_id']).IsAtMost(91000)
            AssertThat(data['code']).IsAtMost(10)

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
    def test_search_by(self, endpoint):
        body = {
            "search_by": [
                {"attribute": "vehicle_id", "operator": "<=", "value": 91000},
                {"attribute": "code", "operator": "<=", "value": 10}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            vehicle_id = data['vehicle_id']
            code = data['code']
            if vehicle_id > 91000 and code > 10:
                raise AssertionError(f'Not true that {vehicle_id} <= 91000 OR {code} <= 10')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, endpoint):
        body = {
            "columns": ["code"],
            "order_by": ["code"]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['code'] for _ in resp]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    def test_order_by_descending(self, endpoint):
        body = {
            "columns": ["code"],
            "order_by": [{"column": "code", "ascending": False}]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['code'] for _ in resp]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка экземляров сущности со смещением")
    def test_offset(self, endpoint):
        body = {
            "columns": ["vehicle_id"],
            "limit": 4
        }
        r = endpoint.get(json=body)
        resp_limit_4 = [_['vehicle_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = endpoint.get(json=body)
        resp_limit_2 = [_['vehicle_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

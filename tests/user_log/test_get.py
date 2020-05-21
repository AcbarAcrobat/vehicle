import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import user_logs
from schema.base import skeleton, build
from endpoint import UserLogs
from truth.truth import AssertThat


class TestUserLogsGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), user_logs.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['intention']),
            (['result']),
            (['entity', 'event_id'])
        ])
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get()

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint):
        body = {
            "filter_by": [{"attribute": "user_id", "operator": ">=", "value": 3000}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['user_id'] for r in resp]

        [AssertThat(i).IsAtLeast(3000) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint):
        body = {
            "filter_by": [
                {"attribute": "user_id", "operator": ">=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 50}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['user_id']).IsAtLeast(3000)
            AssertThat(data['id']).IsAtMost(50)

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
                {"attribute": "user_id", "operator": ">=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 50}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            user_id = data['user_id']
            id_ = data['id']
            if id_ > 50 and user_id < 3000:
                raise AssertionError(f'Not true that {user_id} >= 3000 OR {id_} < 50')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, endpoint):
        body = {
            "columns": ["user_id"],
            "order_by": ["user_id"]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [i['user_id'] for i in resp]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    def test_order_by_descending(self, endpoint):
        body = {
            "columns": ["user_id"],
            "order_by": [{"column": "user_id", "ascending": False}]
        }
        r = endpoint.get(json=body)
        resp = r.json()['result']

        data = [_['user_id'] for _ in resp]
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

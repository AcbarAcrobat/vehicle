import pytest
import allure 
from jsonschema import validate
from helper import LOGGER
from schema import restreamer_error
from schema.base import skeleton, build
from endpoint import RestreamerError
from truth.truth import AssertThat


class TestRestreamerErrorGet:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerErrorGet.endpoint = RestreamerError(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Схема ответа")
    
    def test_schema(self):
        r = self.endpoint.get()
        validate(r.json(), restreamer_error.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    
    @pytest.mark.parametrize(
        'columns', [
            ([ ]),
            (['code']),
            (['occurred_at', 'code']),
            (['restreamer_id', 'code'])
        ]
    )
    def test_response_contains_only_given_columns(self, columns):
        body = { 'columns': columns }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_error.foreign_key_schema(columns))

    
    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("По умолчанию сортировка по первичному ключу")
    
    def test_default_sorting_by_id(self):
        r = self.endpoint.get()

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['restreamer_id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    
    def test_get_entity_with_all_attributes_without_relations(self):
        body = {
            'columns': ['*']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_error.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    
    def test_get_entity_with_all_attributes_and_relations(self):
        body = {
            'columns': ['**']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_error.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию")
    
    def test_filter_by_attribute(self):
        body = {
            "filter_by": [{"attribute": "restreamer_id", "operator": "<=", "value": 100}]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['restreamer_id'] for r in resp ]

        [ AssertThat(i).IsAtMost(100) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'И'")
    
    def test_filter_by_multiple_attributes(self):
        body = {
            "filter_by": [
                {"attribute": "restreamer_id", "operator": "<=", "value": 100},
                {"attribute": "code", "operator": ">=", "value": 1}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['restreamer_id']).IsAtMost(100)
            AssertThat(data['code']).IsAtLeast(1)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    
    def test_filter_by_even_id(self):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "restreamer_id", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['restreamer_id']
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['restreamer_id'] for r in resp ]

        [ AssertThat(i % 2).IsEqualTo(0) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    
    def test_search_by(self):
        body = {
            "search_by": [
                {"attribute": "restreamer_id", "operator": "<=", "value": 100},
                {"attribute": "code", "operator": ">=", "value": 1}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            restreamer_id = data['restreamer_id']
            code = data['code']
            if restreamer_id > 100 and code < 1:
                raise AssertionError(f'Not true that {restreamer_id} <= 100 OR {code} >= 1')


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    
    def test_order_by(self):
        body = {
            "columns": ["restreamer_id"],
            "order_by": ["restreamer_id"]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['restreamer_id'] for _ in resp ]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    
    def test_order_by_descending(self):
        body = {
            "columns": ["restreamer_id"],
            "order_by": [{"column": "restreamer_id", "ascending": False}]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['restreamer_id'] for _ in resp ]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer error")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со смещением")
    
    def test_offset(self):
        body = {
            "columns": ["restreamer_id"],
            "limit": 4
        }
        r = self.endpoint.get(json=body)
        resp_limit_4 = [ _['restreamer_id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = self.endpoint.get(json=body)
        resp_limit_2 = [ _['restreamer_id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

import pytest
import allure 
from jsonschema import validate
from helper import LOGGER
from schema import user_logs
from schema.base import skeleton, build
from endpoint import UserLogs
from truth.truth import AssertThat


class TestUserLogsGet:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestUserLogsGet.endpoint = UserLogs(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Схема ответа")
    
    def test_schema(self):
        r = self.endpoint.get()
        validate(r.json(), user_logs.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    
    @pytest.mark.parametrize(
        'columns', [
            ([ ]),
            (['intention']),
            (['result']),
            (['entity', 'event_id'])
    ])
    def test_response_contains_only_given_columns(self, columns):
        body = { 'columns': columns }
        r = self.endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema(columns))

    
    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("По умолчанию сортировка по первичному ключу")
    
    def test_default_sorting_by_id(self):
        r = self.endpoint.get()

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    
    def test_get_entity_with_all_attributes_without_relations(self):
        body = {
            'columns': ['*']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    
    def test_get_entity_with_all_attributes_and_relations(self):
        body = {
            'columns': ['**']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), user_logs.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию")
    
    def test_filter_by_attribute(self):
        body = {
            "filter_by": [{"attribute": "user_id", "operator": ">=", "value": 3000}]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['user_id'] for r in resp ]

        [ AssertThat(i).IsAtLeast(3000) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'И'")
    
    def test_filter_by_multiple_attributes(self):
        body = {
            "filter_by": [
                {"attribute": "user_id", "operator": ">=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 50}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['user_id']).IsAtLeast(3000)
            AssertThat(data['id']).IsAtMost(50)


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    
    def test_filter_by_even_id(self):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "id", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['id']
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['id'] for r in resp ]

        [ AssertThat(i % 2).IsEqualTo(0) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    
    def test_search_by(self):
        body = {
            "search_by": [
                {"attribute": "user_id", "operator": ">=", "value": 3000},
                {"attribute": "id", "operator": "<=", "value": 50}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            user_id = data['user_id']
            id_ = data['id']
            if id_ > 50 and user_id < 3000:
                raise AssertionError(f'Not true that {user_id} >= 3000 OR {id_} < 50')


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    
    def test_order_by(self):
        body = {
            "columns": ["user_id"],
            "order_by": ["user_id"]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ i['user_id'] for i in resp ]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    
    def test_order_by_descending(self):
        body = {
            "columns": ["user_id"],
            "order_by": [{"column": "user_id", "ascending": False}]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['user_id'] for _ in resp ]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("User logs")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со смещением")
    
    def test_offset(self):
        body = {
            "columns": ["id"],
            "limit": 4
        }
        r = self.endpoint.get(json=body)
        resp_limit_4 = [ _['id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = self.endpoint.get(json=body)
        resp_limit_2 = [ _['id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

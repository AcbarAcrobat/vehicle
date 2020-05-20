import pytest
import allure 
from jsonschema import validate
from helper import LOGGER
from schema import restreamer_type
from schema.base import skeleton, build
from endpoint import RestreamerType
from truth.truth import AssertThat


class TestRestreamerTypeGet:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerTypeGet.endpoint = RestreamerType(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("Схема ответа")
    
    def test_schema(self):
        r = self.endpoint.get()
        validate(r.json(), restreamer_type.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    
    @pytest.mark.parametrize(
        'columns', [
            ([ ]),
            (['id']),
            (['title']),
            (['order_priority', 'id'])
        ]
    )
    def test_response_contains_only_given_columns(self, columns):
        body = { 'columns': columns }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_type.foreign_key_schema(columns))

    
    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("По умолчанию сортировка по первичному ключу")
    
    def test_default_sorting_by_id(self):
        r = self.endpoint.get()

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    
    def test_get_entity_with_all_attributes_without_relations(self):
        body = {
            'columns': ['*']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_type.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    
    def test_get_entity_with_all_attributes_and_relations(self):
        body = {
            'columns': ['**']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_type.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    
    def test_order_by(self):
        body = {
            "columns": ["id"],
            "order_by": ["id"]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['id'] for _ in resp ]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer type")
    @allure.sub_suite("Get")
    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    
    def test_order_by_descending(self):
        body = {
            "columns": ["id"],
            "order_by": [{"column": "id", "ascending": False}]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['id'] for _ in resp ]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()

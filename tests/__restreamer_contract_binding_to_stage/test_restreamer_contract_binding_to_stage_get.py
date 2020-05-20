import pytest
import allure 
from jsonschema import validate
from helper import LOGGER
from schema import restreamer_contract_binding_to_stage
from schema.base import skeleton, build
from endpoint import RestreamerContractBindingToStage
from truth.truth import AssertThat


class TestRestreamerContractBindingToStageGet:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerContractBindingToStageGet.endpoint = RestreamerContractBindingToStage(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Схема ответа")
    
    def test_schema(self):
        r = self.endpoint.get()
        validate(r.json(), restreamer_contract_binding_to_stage.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    
    @pytest.mark.parametrize(
        'columns', [
            ([ ]),
            (['restreamer_contract_binding_id']),
            (['stage_id'])
        ]
    )
    def test_response_contains_only_given_columns(self, columns):
        body = { 'columns': columns }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding_to_stage.foreign_key_schema(columns))


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    
    def test_get_entity_with_all_attributes_without_relations(self):
        body = {
            'columns': ['*']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding_to_stage.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    
    def test_get_entity_with_all_attributes_and_relations(self):
        body = {
            'columns': ['**']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding_to_stage.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию")
    
    def test_filter_by_attribute(self):
        body = {
            "filter_by": [{"attribute": "restreamer_contract_binding_id", "operator": ">=", "value": 6}]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['restreamer_contract_binding_id'] for r in resp ]

        [ AssertThat(i).IsAtLeast(6) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'И'")
    
    def test_filter_by_multiple_attributes(self):
        body = {
            "filter_by": [
                {"attribute": "restreamer_contract_binding_id", "operator": ">=", "value": 6},
                {"attribute": "stage_id", "operator": ">=", "value": 10000}
                
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['restreamer_contract_binding_id']).IsAtLeast(6)
            AssertThat(data['stage_id']).IsAtLeast(10000)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    
    def test_filter_by_even_id(self):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "restreamer_contract_binding_id", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['restreamer_contract_binding_id']
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['restreamer_contract_binding_id'] for r in resp ]

        [ AssertThat(i % 2).IsEqualTo(0) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    
    def test_search_by(self):
        body = {
            "search_by": [
                {"attribute": "restreamer_contract_binding_id", "operator": ">=", "value": 6},
                {"attribute": "stage_id", "operator": ">=", "value": 10000}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            restreamer_contract_binding_id = data['restreamer_contract_binding_id']
            stage_id = data['stage_id']
            if restreamer_contract_binding_id < 6 and stage_id < 10000:
                raise AssertionError(f'Not true that {restreamer_contract_binding_id} >= 6 OR {stage_id} >= 10000')


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    
    def test_order_by(self):
        body = {
            "columns": ["stage_id"],
            "order_by": ["stage_id"]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['stage_id'] for _ in resp ]
        sorted_data = sorted(data)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    
    def test_order_by_descending(self):
        body = {
            "columns": ["stage_id"],
            "order_by": [{"column": "stage_id", "ascending": False}]
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        data = [ _['stage_id'] for _ in resp ]
        sorted_data = sorted(data, reverse=True)

        AssertThat(data).ContainsExactlyElementsIn(sorted_data).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding to stage")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со смещением")
    
    def test_offset(self):
        body = {
            "columns": ["stage_id"],
            "limit": 4
        }
        r = self.endpoint.get(json=body)
        resp_limit_4 = [ _['stage_id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = self.endpoint.get(json=body)
        resp_limit_2 = [ _['stage_id'] for _ in r.json()['result'] ]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

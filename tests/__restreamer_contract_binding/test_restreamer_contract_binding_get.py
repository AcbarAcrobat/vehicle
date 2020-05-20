import pytest
import allure 
from jsonschema import validate
from helper import LOGGER
from schema import restreamer_contract_binding
from schema.base import skeleton, build
from endpoint import RestreamerContractBinding, RestreamerContractBindingToStage
from truth.truth import AssertThat


class TestRestreamerContractBindingGet:

    @pytest.fixture(scope='class', autouse=True)
    def set_endpoint(self, session):
        TestRestreamerContractBindingGet.endpoint = RestreamerContractBinding(session)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Схема ответа")
    
    def test_schema(self):
        r = self.endpoint.get()
        validate(r.json(), restreamer_contract_binding.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    
    @pytest.mark.parametrize(
        'columns', [
            ([ ]),
            (['id']),
            (['restreamer_id']),
            (['contract_id', 'stages'])
        ]
    )
    def test_response_contains_only_given_columns(self, columns):
        body = { 'columns': columns }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding.foreign_key_schema(columns))

    
    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("По умолчанию сортировка по первичному ключу")
    
    def test_default_sorting_by_id(self):
        r = self.endpoint.get()

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'точку'")
    
    def test_child_attribute_via_dot(self):
        body = {
            'columns': ['stages.stage_id', 'id']
        }
        r = self.endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** restreamer_contract_binding.restreamer_contract_binding_fk_properties,
                'stages': {
                    'type': 'array',
                    'items': build(
                        restreamer_contract_binding.stages_fk_properties,
                        ['stage_id']
                    )
                }
            },
            ['stages', 'id']
        ))
        validate(r.json(), schema_)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с определенными атрибутами дочерней сущности через 'вложенный объект'")
    
    def test_child_attribute_via_nested_entity(self):
        body = {
            'columns': [
                'id',
                { "entity": "restreamer_contract_binding_to_stage", "columns": ["stage_id"] }
            ]
        }
        r = self.endpoint.get(json=body)

        schema_ = skeleton(build(
            {
                ** restreamer_contract_binding.restreamer_contract_binding_fk_properties,
                'stages': {
                    'type': 'array',
                    'items': build(
                        restreamer_contract_binding.stages_fk_properties,
                        ['stage_id']
                    )
                }
            },
            ['stages', 'id']
        ))
        validate(r.json(), schema_)

        validate(r.json(), schema_)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    
    def test_get_entity_with_all_attributes_without_relations(self):
        body = {
            'columns': ['*']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding.foreign_key_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    
    def test_get_entity_with_all_attributes_and_relations(self):
        body = {
            'columns': ['**']
        }
        r = self.endpoint.get(json=body)
        validate(r.json(), restreamer_contract_binding.structural_schema())


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Двойная звезочка также применима к дочерним сущностям")
    
    def test_get_child_entity_all_attributes_and_relations(self):
        body = {
            'columns': ['stages.**']
        }
        r = self.endpoint.get(json=body)

        validate( r.json(), restreamer_contract_binding.structural_schema(['stages']) )


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию")
    
    def test_filter_by_attribute(self):
        body = {
            "filter_by": [{"attribute": "restreamer_id", "operator": ">=", "value": 10000}]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']
        ids = [ r['restreamer_id'] for r in resp ]

        [ AssertThat(i).IsAtLeast(10000) for i in ids ]


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'И'")
    
    def test_filter_by_multiple_attributes(self):
        body = {
            "filter_by": [
                {"attribute": "restreamer_id", "operator": ">=", "value": 10000},
                {"attribute": "id", "operator": ">=", "value": 6}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['id']).IsAtLeast(6)
            AssertThat(data['restreamer_id']).IsAtLeast(10000)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию дочерней сущности")
    
    def test_filter_by_child_attribute(self, session):
        # Получим какой-нибудь дочерний объект
        child_id = RestreamerContractBindingToStage(session).get_random()['stage_id']
        LOGGER.info(f'NetworkDeviceContractBindingToStage: {child_id}')

        body = {
            "filter_by": {"attribute": "stages.stage_id", "operator": "in", "value": [child_id]}
        }
        r = self.endpoint.get(json=body)
        resp = r.json()['result']

        for data in resp:
            AssertThat(data['stages']).Contains(child_id)


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
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
    @allure.suite("Restreamer contract binding")
    @allure.sub_suite("Get")
    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    
    def test_search_by(self):
        body = {
            "search_by": [
                {"attribute": "restreamer_id", "operator": ">=", "value": 10000},
                {"attribute": "id", "operator": ">=", "value": 6}
            ]
        }
        r = self.endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            id_ = data['id']
            restreamer_id = data['restreamer_id']
            if restreamer_id < 10000 and id_ < 6:
                raise AssertionError(f'Not true that {restreamer_id} >= 10000 OR {id_} >= 6')


    @allure.parent_suite('API - Smoke')
    @allure.suite("Restreamer contract binding")
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
    @allure.suite("Restreamer contract binding")
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
    @allure.suite("Restreamer contract binding")
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

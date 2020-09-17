import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_part_type
from schema.base import skeleton, build
from truth.truth import AssertThat


class TestVehiclePartTypeGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_part_type.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['id']),
            (['name']),
            (['full_image', 'small_image'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part_type.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part_type.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_part_type.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint):
        body = {
            "filter_by": [{"attribute": "id", "operator": "<=", "value": 10}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i).IsAtMost(10) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint):
        body = {
            "filter_by": [
                {"attribute": "id", "operator": "<=", "value": 10},
                {"attribute": "name", "operator": "=", "value": "tram_head"}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['id']).IsAtMost(10)
            AssertThat(data['name']).IsEqualTo("tram_head")

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
                {"attribute": "id", "operator": "<=", "value": 10},
                {"attribute": "name", "operator": "=", "value": "tram_head"}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            id_ = data['id']
            name = data['name']
            if id_ > 10 and name != "tram_head":
                raise AssertionError(f'Not true that {id_} <= 10 OR {name} == "tram_head"')

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

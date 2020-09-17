import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import vehicle_camera_error
from schema.base import skeleton, build
from truth.truth import AssertThat


class TestVehicleCameraErrorGet:

    @allure.title("Схема ответа")
    def test_schema(self, endpoint):
        r = endpoint.get()
        validate(r.json(), vehicle_camera_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['occurred_at', 'code']),
            (['occurred_at']),
            (['code'])
        ]
    )
    def test_response_contains_only_given_columns(self, endpoint, columns):
        body = {'columns': columns}
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera_error.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, endpoint):
        r = endpoint.get(json={"columns": ["vehicle_camera_id"]})

        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['vehicle_camera_id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, endpoint):
        body = {
            'columns': ['*']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, endpoint):
        body = {
            'columns': ['**']
        }
        r = endpoint.get(json=body)
        validate(r.json(), vehicle_camera_error.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, endpoint, data_vehicle_camera_error):
        code = data_vehicle_camera_error["body"]["values"][0]["code"]
        body = {
            "filter_by": [{"attribute": "code", "operator": "=", "value": code}]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        codes = [r['code'] for r in resp]

        [AssertThat(i).IsEqualTo(code) for i in codes]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, endpoint, data_vehicle_camera_error):
        code = data_vehicle_camera_error["body"]["values"][0]["code"]
        occurred_at = data_vehicle_camera_error["body"]["values"][0]['occurred_at']
        body = {
            "filter_by": [
                {"attribute": "code", "operator": "=", "value": code},
                {"attribute": "occurred_at", "operator": ">=", "value": occurred_at}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['code']).IsEqualTo(code)
            AssertThat(data['occurred_at']).IsAtLeast(occurred_at)

    @allure.title("Получение списка экземляров сущности по условию, содержащему препроцессор")
    def test_filter_by_even_code(self, endpoint):
        body = {
            'filter_by': [{'attribute': {"operator": "%", "attribute": "code", "value": 2}, 'operator': '=', 'value': 0}],
            'columns': ['code']
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']
        codes = [r['code'] for r in resp]

        [AssertThat(i % 2).IsEqualTo(0) for i in codes]

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, endpoint, data_vehicle_camera_error):
        code = data_vehicle_camera_error["body"]["values"][0]["code"]
        occurred_at = data_vehicle_camera_error["body"]["values"][0]['occurred_at']
        body = {
            "search_by": [
                {"attribute": "code", "operator": "=", "value": code},
                {"attribute": "occurred_at", "operator": ">=", "value": occurred_at}
            ]
        }
        r = endpoint.get(json=body)

        resp = r.json()['result']

        for data in resp:
            code_ = data['code']
            occurred_at_ = data['occurred_at']
            if code_ != code and occurred_at_ < occurred_at:
                raise AssertionError(f'{code_} != {code}, {occurred_at_} < {occurred_at}')

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
            "columns": ["vehicle_camera_id"],
            "limit": 3
        }
        r = endpoint.get(json=body)
        resp_limit_3 = [_['vehicle_camera_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_3)

        body['limit'] = 2
        body['offset'] = 1

        r = endpoint.get(json=body)
        resp_limit_2 = [_['vehicle_camera_id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_3[1:]).ContainsExactlyElementsIn(resp_limit_2).InOrder()

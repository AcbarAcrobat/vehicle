import pytest
import allure
from jsonschema import validate
from helper import LOGGER
from schema import camera_availability
from schema.base import skeleton
from endpoint import CameraAvailability
from truth.truth import AssertThat


class TestGet:

    @allure.title("Схема ответа")
    
    def test_schema(self, session):
        r = CameraAvailability(session).get()
        validate(r.json(), camera_availability.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с определенными атрибутами")
    @pytest.mark.parametrize(
        'columns', [
            ([]),
            (['id']),
            (['description']),
            (['name'])
        ]
    )
    def test_response_contains_only_given_columns(self, session, columns):
        body = {
            ** {'columns': columns}
        }
        r = CameraAvailability(session).get(json=body)
        validate(r.json(), camera_availability.foreign_key_schema(columns))

    @allure.title("По умолчанию сортировка по первичному ключу")
    def test_default_sorting_by_id(self, session):
        r = CameraAvailability(session).get()
        resp = r.json()['result']
        sorted_resp = sorted(resp, key=lambda e: e['id'])

        AssertThat(r.json()['result']).ContainsExactlyElementsIn(sorted_resp).InOrder()

    @allure.title("Получение списка экземляров сущности со всеми атрибутами без раскрытия атрибутов отношений")
    def test_get_entity_with_all_attributes_without_relations(self, session):
        body = {'columns': ['*']}
        r = CameraAvailability(session).get(json=body)
        validate(r.json(), camera_availability.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности с всеми атрибутами c раскрытием атрибутов отношений")
    def test_get_entity_with_all_attributes_and_relations(self, session):
        body = {'columns': ['**']}
        r = CameraAvailability(session).get(json=body)
        validate(r.json(), camera_availability.foreign_key_schema())

    @allure.title("Получение списка экземляров сущности по условию")
    def test_filter_by_attribute(self, session, data_camera_availability):
        id_ = data_camera_availability["ids"][0]
        body = {
            'filter_by': [{'attribute': 'id', 'operator': '>=', 'value': id_}]
        }
        r = CameraAvailability(session).get(json=body)

        resp = r.json()['result']
        ids = [r['id'] for r in resp]

        [AssertThat(i).IsAtLeast(id_) for i in ids]

    @allure.title("Получение списка экземляров сущности по условию 'И'")
    def test_filter_by_multiple_attributes(self, session, data_camera_availability):
        id_ = data_camera_availability["ids"][0]
        name = data_camera_availability["body"]["values"][0]["name"]
        body = {
            "filter_by": [
                {'attribute': 'id', 'operator': '>=', 'value': id_},
                {"attribute": "name", "operator": "=", "value": name}
            ]
        }
        r = CameraAvailability(session).get(json=body)

        resp = r.json()['result']

        for data in resp:
            AssertThat(data['id']).IsAtLeast(id_)
            AssertThat(data['name']).IsEqualTo(name)

    @allure.title("Получение списка экземляров сущности по условию 'ИЛИ'")
    def test_search_by(self, session, data_camera_availability):
        id_ = data_camera_availability["ids"][0]
        name = data_camera_availability["body"]["values"][0]["name"]
        body = {
            "search_by": [
                {'attribute': 'id', 'operator': '>=', 'value': id_},
                {"attribute": "name", "operator": "=", "value": name}
            ]
        }
        r = CameraAvailability(session).get(json=body)

        resp = r.json()['result']

        for data in resp:
            id__ = data['id']
            name_ = data['name']
            if id__ < id_ and name_ != name:
                raise AssertionError(
                    f'Not true that {id__} >= {id_} OR {name_} == {name}')

    @allure.title(" Получение списка отсортированных по возрастанию экземляров сущности")
    def test_order_by(self, session):
        body = {
            "columns": ["id"],
            "order_by": ["id"]
        }
        r = CameraAvailability(session).get(json=body)
        resp = r.json()['result']

        actual_ids = [_['id'] for _ in resp]
        sorted_ids = sorted(actual_ids)

        AssertThat(actual_ids).ContainsExactlyElementsIn(sorted_ids).InOrder()

    @allure.title("Получение списка отсортированных по убыванию экземляров сущности")
    def test_order_by_descending(self, session):
        body = {
            "columns": ["id"],
            "order_by": [{"column": "id", "ascending": False}]
        }
        r = CameraAvailability(session).get(json=body)
        resp = r.json()['result']

        actual_ids = [_['id'] for _ in resp]
        sorted_ids = sorted(actual_ids, reverse=True)

        AssertThat(actual_ids).ContainsExactlyElementsIn(sorted_ids).InOrder()

    @allure.title("Получение списка экземляров сущности со смещением")
    def test_offset(self, session):
        body = {
            "columns": ["id"],
            "limit": 4
        }
        r = CameraAvailability(session).get(json=body)
        resp_limit_4 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_4)

        body['limit'] = 2
        body['offset'] = 2

        r = CameraAvailability(session).get(json=body)
        resp_limit_2 = [_['id'] for _ in r.json()['result']]
        LOGGER.info(resp_limit_2)

        AssertThat(resp_limit_4[2:]).ContainsExactlyElementsIn(
            resp_limit_2).InOrder()

import pytest
import requests
from requests_toolbelt import sessions
from pytest_testconfig import config
from termcolor import colored
from faker import Faker
from helper import LOGGER
from xdist.scheduler.loadscope import LoadScopeScheduling
from endpoint import *
from datetime import datetime as dt


@pytest.fixture(scope='session')
def token():
    r = requests.post(config['auth_server'] + 'netris/login', json={
        'login': config['login'],
        'password': config['password'],
    })
    if 'result' not in r.json():
        LOGGER.warning(r.json())
        r.json()['result']  # Чтобы бросить KeyError

    yield {'token': r.json()['result']['token']}


@pytest.fixture(scope='session')
def session(token):
    s = sessions.BaseUrlSession(base_url=config['base_url'])
    s.headers = {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    yield s


@pytest.fixture(scope='session')
def faker():
    yield Faker('ru_RU')


def pytest_make_parametrize_id(config, val):
    return repr(val)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    print("\n" + item.pretty_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown():
    # Просто перенос для красоты
    print()


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        pretty_id = colored(item.parent.parent.name + ": ", 'magenta', attrs=['bold'])

        splitted = item.name.split('_')
        captalized = splitted[0].capitalize() + ' ' + ' '.join(splitted[1:])
        func_id = captalized

        pretty_id += colored(func_id, 'white', attrs=['bold'])

        item.pretty_id = pretty_id


class MyScheduler(LoadScopeScheduling):
    def _split_scope(self, nodeid):
        splitted = nodeid.split('/')
        id_ = splitted[0] + '/' + splitted[1].split('_')[0]
        return f"{id_}_worker"


def pytest_xdist_make_scheduler(config, log):
    return MyScheduler(config, log)


#
# Готовим данные
#
@pytest.fixture(scope='session')
def data_camera_availability(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4(),
            "description": faker.uuid4()
        })

    r = CameraAvailability(session).add(json=body)
    LOGGER.info(f"CameraAvailability: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_existence_type(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4()
        })
    r = ExistenceType(session).add(json=body)
    LOGGER.info(f"ExistenceType: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_mobile_operator(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4()
        })
    r = MobileOperator(session).add(json=body)
    LOGGER.info(f"MobileOperator: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle_type(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4(),
            "image": f"images/{faker.uuid4()}.svg"
        })
    r = VehicleType(session).add(json=body)
    LOGGER.info(f"VehicleType: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle(session, faker, data_mobile_operator, data_vehicle_type, data_existence_type):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "subscriber_identification_module_number": faker.uuid4(),
            "international_mobile_equipment_identity": faker.uuid4(),
            "vehicle_identification_number": faker.uuid4(),
            "computer_serial_number": faker.uuid4(),
            "is_stats_check_enabled": True,
            "mobile_operator_id": data_mobile_operator["ids"][0],  # <<<
            "registration_plate": faker.uuid4(),
            # "contract_bindings": array_of("integer"),
            # "ownership_type_id": {"type": "integer"},
            "sync_with_netris": True,
            # "attached_files": array_of("integer"),
            "approving_date": round(dt.utcnow().timestamp()*1000),
            "chat_room_id": faker.random_number(),
            "availability": data_existence_type["ids"][0],
            # "template_id": {"type": "integer"},
            # "contract_id": {"type": "integer"},
            "ip_address": "127.0.0.1",
            "region_id": 1,
            "is_hidden": False,
            "longitude": 12.34,
            "password": faker.uuid4(),
            "axxon_id": faker.uuid4(),
            "latitude": 56.78,
            "type_id": data_vehicle_type["ids"][0],  # <<<
            # "status": {
            #     "anyOf": [
            #         array_of("integer"),
            #         {"type": "null"}
            #     ]
            # },
            # "stages": array_of("integer"),
            # "parts": array_of("integer"),
            # "error": {
            #     "anyOf": [
            #         array_of("integer"),
            #         {"type": "null"}
            #     ]
            # },
            "login": faker.uuid4(),
            "title": faker.uuid4()
        })
    r = Vehicle(session).add(json=body)
    LOGGER.info(f"Vehicle: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle_to_stage(session, faker, data_vehicle):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][i],
            "stage_id": VehicleToStage(session).get_last()["stage_id"]+1
        })
    r = VehicleToStage(session).add(json=body)
    LOGGER.info(f"VehicleToStage: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle_to_attached_file(session, faker, data_vehicle):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][0],
            "file_name": f"{faker.uuid4()}.pdf",
            "order_id": None,
            "file_id": faker.random_number()
        })
    r = VehicleToAttachedFile(session).add(json=body)
    LOGGER.info(f"VehicleToAttachedFile: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle_part_type(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4(),
            "full_image": f"images/{faker.uuid4()}.svg",
            "small_image": f"images/{faker.uuid4()}.svg"
        })
    r = VehiclePartType(session).add(json=body)
    LOGGER.info(f"VehiclePartType: {r.json()}")
    yield {"body": body, "ids": r.json()['result']} 


@pytest.fixture(scope='session')
def data_vehicle_part(session, faker, data_vehicle, data_vehicle_part_type):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][0],
            "part_type_id": data_vehicle_part_type["ids"][0]
            # "cameras": array_of("integer")
        })
    r = VehiclePart(session).add(json=body)
    LOGGER.info(f"VehiclePart: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}


@pytest.fixture(scope='session')
def data_vehicle_camera(session, faker, data_camera_availability, data_vehicle_part):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "stream_resolution_height": faker.random_number(),
            "stream_resolution_width": faker.random_number(),
            "camera_availability_id": data_camera_availability["ids"][0],
            "hls_second_stream_url": "http://localhost:80",
            "hls_first_stream_url": "http://localhost:80",
            "camera_position_id": 0,
            "stream_resolution": faker.random_digit(),
            "installation_site": 0,
            "rtsp_second_url": "rtsp://admin:admin@127.0.0.1/baz/quux/SourceEndpoint.video:1:1",
            "stream_bitrate": faker.random_digit(),
            "rtsp_first_url": "rtsp://admin:admin@127.0.0.1/foo/bar/SourceEndpoint.video:0:0",
            # "daytime_image": {"type": "integer"},
            # "night_image": {"type": "integer"},
            "rtsp_camera": "rtsp://admin:admin@122.0.0.1:554/hello/world/0/0",
            "description": faker.uuid4(),
            "ip_address": "127.0.0.1",
            "stream_fps": faker.random_number(),
            "axxon_id": faker.uuid4(),
            "part_id": data_vehicle_part["ids"][0],
            # "status": {
            #     "anyOf": [
            #         array_of("integer"),
            #         {"type": "null"}
            #     ]
            # },
            "camera_position": {
                "x": faker.random_digit(),
                "y": faker.random_digit(),
                "scope": faker.random_digit(),
                "azimut": faker.random_digit()
            },
            # "error": {
            #     "anyOf": [
            #         array_of("integer"),
            #         {"type": "null"}
            #     ]
            # }
        })
    r = VehicleCamera(session).add(json=body)
    LOGGER.info(f"VehicleCamera: {r.json()}")
    yield {"body": body, "ids": r.json()['result']}

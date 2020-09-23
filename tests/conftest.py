import pytest
from requests import session as requests_session
from pytest_testconfig import config
from termcolor import colored
from faker import Faker
from helper import LOGGER
from xdist.scheduler.loadscope import LoadScopeScheduling
from endpoint import *
from datetime import datetime as dt
import numpy
from pathlib import Path
from PIL import Image


def now_millis():
    return round(dt.utcnow().timestamp()*1000)


@pytest.fixture(scope='session')
def session():
    s = requests_session()
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
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    CameraAvailability(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_existence_type(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4()
        })
    r = ExistenceType(session).add(json=body)
    LOGGER.info(f"ExistenceType: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    ExistenceType(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_mobile_operator(session, faker):
    body = {"values": []}
    for _ in range(5):
        body["values"].append({
            "name": faker.uuid4()
        })
    r = MobileOperator(session).add(json=body)
    LOGGER.info(f"MobileOperator: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    MobileOperator(session).delete_many_by("id", ids)


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
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehicleType(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_template(session, faker, data_vehicle_type):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "title": faker.uuid4(),
            "type_id": data_vehicle_type["ids"][i]
        })
    r = VehicleTemplate(session).add(json=body)
    LOGGER.info(f"VehicleTemplate: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehicleTemplate(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle(session, faker, data_mobile_operator, data_vehicle_type, data_existence_type, data_vehicle_template):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "subscriber_identification_module_number": faker.uuid4(),
            "international_mobile_equipment_identity": faker.uuid4(),
            "vehicle_identification_number": faker.uuid4(),
            "computer_serial_number": faker.uuid4(),
            "is_stats_check_enabled": True,
            "mobile_operator_id": data_mobile_operator["ids"][i],
            "registration_plate": faker.uuid4(),
            "sync_with_netris": True,
            "approving_date": round(dt.utcnow().timestamp()*1000),
            "financing_type_id": 1,
            "chat_room_id": faker.random_number(),
            "availability": data_existence_type["ids"][i],
            "template_id": data_vehicle_template["ids"][i],
            "ip_address": "127.0.0.1",
            "region_id": 1,
            "is_hidden": False,
            "longitude": 12.34,
            "password": faker.uuid4(),
            "axxon_id": faker.uuid4(),
            "latitude": 56.78,
            "type_id": data_vehicle_type["ids"][i],
            "login": faker.uuid4(),
            "title": faker.uuid4(),
            "created_at": now_millis()
        })
    r = Vehicle(session).add(json=body)
    LOGGER.info(f"Vehicle: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    Vehicle(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_error(session, faker, data_vehicle):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "code": faker.random_digit(),
            "vehicle_id":data_vehicle["ids"][i],
            "occurred_at": now_millis(),
            "outdated_at": now_millis()
        })
    r = VehicleError(session).add(json=body)
    LOGGER.info(f"VehicleError: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehicleError(session).delete_many_by("id", ids)


####################################################################################
####################################################################################
####################################################################################
@pytest.fixture(scope='session')
def data_loaded_file_vehicle(session, faker):
    # body = {"values": []}
    ids = []
    for i in range(5):
        i = VehicleFile(session)
        file_name = faker.uuid4()+".png"
        path_to = Path.cwd().joinpath("_data", file_name)
        with open(path_to, "wb+") as file:
            imarray = numpy.random.rand(30,30,3) * 255
            file.write(imarray)
        r = i.upload(file_name, file_name, "image/png").json()
        LOGGER.info(r)
        Path.unlink(path_to)
        ids.append(r['result'])
    LOGGER.info(f"VehicleFile: {ids}")
    yield {"body": [], "ids": ids}


@pytest.fixture(scope='session')
def data_loaded_file_immovable(session, faker):
    ids = []
    for i in range(5):
        i = ImmovableFile(session)
        file_name = faker.uuid4()+".png"
        path_to = Path.cwd().joinpath("_data", file_name)
        with open(path_to, "wb+") as file:
            imarray = numpy.random.rand(30,30,3) * 255
            file.write(imarray)
        r = i.upload(file_name, file_name, "image/png").json()
        LOGGER.info(r)
        Path.unlink(path_to)
        ids.append(r["result"])
    LOGGER.info(f"ImmovableFile: {ids}")
    yield {"body": [], "ids": ids}


@pytest.fixture(scope='session')
def data_region(session, faker, data_loaded_file_immovable):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "created_at_epoch": now_millis(),
            "osm_id": data_loaded_file_immovable["ids"][i],
            "title": faker.uuid4()
        })
    r = Region(session).add(json=body)
    LOGGER.info(f"Region: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    Region(session).delete_many_by("id", ids)



@pytest.fixture(scope='session')
def data_contract(session, faker, data_region):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "violation_minutes_to_become_defective": abs(faker.pyfloat()),
            "allowed_bitrate_deviation_percent": abs(faker.pyfloat()),
            # https://git.abm-jsc.ru/saferegion/immovable_server/-/blob/master/source/entities/no_data_consideration_type.py#L19
            "no_data_consideration_type_id": 1,
            "data_gathering_type_id": 1,
            "sane_minutes_to_become_valid": abs(faker.pyfloat()),
            "report_representation_id": faker.random_number(),
            "allowed_fps_deviation": abs(faker.pyfloat()),
            "parent_contract_id": None,
            "maintainer_phone": "88005553535",
            "max_loss_percent": abs(faker.pyfloat()),
            "maintainer_email": "hello@world.org",
            "created_at_epoch": now_millis(),
            # "network_devices": {'type': 'array'},
            "maintainer_name": faker.name(),
            # "attached_files": {'type': 'array'},
            "enable_mailing": True,
            "record_length": faker.random_number(),
            # "restreamers": {'type': 'array'},
            "description": faker.sentence(),
            "max_jitter": abs(faker.pyfloat()),
            "region_id": data_region["ids"][i],
            "max_ping": abs(faker.pyfloat()),
            # "schemas": {'type': 'array'},
            # "cameras": array_of('integer'),
            "email": "vasya@pupkin.net",
            "title": faker.uuid4()
        })
    r = Contract(session).add(json=body)
    LOGGER.info(f"Contract: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    Contract(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_contract_stage(session, faker, data_contract):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "created_at_epoch": now_millis(),
            "start_at_epoch": now_millis(),
            "end_at_epoch": now_millis(),
            "contract_id": data_contract["ids"][i],
            "title": faker.uuid4(),
            "price": abs(faker.pyfloat())
        })
    r = ContractStage(session).add(json=body)
    LOGGER.info(f"ContractStage: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    ContractStage(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_to_stage(session, faker, data_vehicle, data_contract_stage):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][i],
            "stage_id": data_contract_stage["ids"][i]
        })
    r = VehicleToStage(session).add(json=body)
    LOGGER.info(f"VehicleToStage: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    for data in body["values"]:
        VehicleToStage(session).delete_by([
            ("vehicle_id", data["vehicle_id"]),
            ("stage_id", data["stage_id"])
        ])


@pytest.fixture(scope='session')
def data_vehicle_to_attached_file(session, faker, data_vehicle, data_loaded_file_vehicle):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][i],
            "file_name": f"{faker.uuid4()}.pdf",
            "order_id": None,
            "file_id": data_loaded_file_vehicle["ids"][i]
        })
    r = VehicleToAttachedFile(session).add(json=body)
    LOGGER.info(f"VehicleToAttachedFile: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehicleToAttachedFile(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_contract_binding(session, faker, data_vehicle, data_contract):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][i],
            "contract_id": data_contract["ids"][i]
        })
    r = VehicleContractBinding(session).add(json=body)
    LOGGER.info(f"VehicleContractBinding: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehicleContractBinding(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_contract_binding_to_stage(session, faker, data_vehicle_contract_binding, data_contract_stage):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_contract_binding_id": data_vehicle_contract_binding["ids"][i],
            "stage_id": data_contract_stage["ids"][i]
        })
    r = VehicleContractBindingToStage(session).add(json=body)
    LOGGER.info(f"VehicleContractBindingToStage: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    for data in body["values"]:
        VehicleContractBindingToStage(session).delete_by([
            ("vehicle_contract_binding_id", data["vehicle_contract_binding_id"]),
            ("stage_id", data["stage_id"])
        ])


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
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehiclePartType(session).delete_many_by("id", ids) 


@pytest.fixture(scope='session')
def data_vehicle_part(session, faker, data_vehicle, data_vehicle_part_type):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_id": data_vehicle["ids"][i],
            "part_type_id": data_vehicle_part_type["ids"][i]
            # "cameras": array_of("integer")
        })
    r = VehiclePart(session).add(json=body)
    LOGGER.info(f"VehiclePart: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    VehiclePart(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_camera(session, faker, data_camera_availability, data_vehicle_part, data_loaded_file_vehicle):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "stream_resolution_height": faker.random_number(),
            "stream_resolution_width": faker.random_number(),
            "camera_availability_id": data_camera_availability["ids"][i],
            "hls_second_stream_url": "http://localhost:80",
            "hls_first_stream_url": "http://localhost:80",
            "camera_position_id": i,
            "stream_resolution": faker.random_digit(),
            "installation_site": data_loaded_file_vehicle["ids"][0],
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
            "part_id": data_vehicle_part["ids"][i],
            "camera_position": {
                "x": faker.random_digit(),
                "y": faker.random_digit(),
                "scope": faker.random_digit(),
                "azimut": faker.random_digit()
            },
        })
    r = VehicleCamera(session).add(json=body)
    LOGGER.info(f"VehicleCamera: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    # VehicleCamera(session).delete_many_by("id", ids)


@pytest.fixture(scope='session')
def data_vehicle_camera_error(session, faker, data_vehicle_camera):
    body = {"values": []}
    for i in range(5):
        body["values"].append({
            "vehicle_camera_id": data_vehicle_camera["ids"][i],
            "occurred_at": now_millis(),
            "code": faker.random_digit_not_null(),
            "outdated_at": now_millis()
        })
    r = VehicleCameraError(session).add(json=body)
    LOGGER.info(f"VehicleCameraError: {r.json()}")
    ids = r.json()['result']
    yield {"body": body, "ids": ids}
    for data in body["values"]:
        VehicleCameraError(session).delete_by([
            ("vehicle_camera_id", data["vehicle_camera_id"]),
            ("code", data["code"])
        ])


@pytest.fixture(scope='session', autouse=True)
def populate(
    data_vehicle_template,
    data_vehicle,
    data_vehicle_error,
    data_loaded_file_immovable,
    data_loaded_file_vehicle,
    data_region,
    data_contract,
    data_contract_stage,
    data_vehicle_to_stage,
    data_vehicle_to_attached_file,
    data_vehicle_part_type,
    data_vehicle_part,
    data_vehicle_camera,
    data_vehicle_camera_error
):
    s = '''
\t+-----------------+
\t| END POPULATE DB |
\t+-----------------+
    '''
    LOGGER.info(s)
    yield
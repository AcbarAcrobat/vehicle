import pytest
import requests
from requests_toolbelt import sessions
from pytest_testconfig import config
from termcolor import colored
from faker import Faker
from helper import LOGGER
from xdist.scheduler.loadscope import LoadScopeScheduling


@pytest.fixture(scope='session')
def token():
    r = requests.post(config['auth_server'] + 'netris/login', json={
        'login': config['login'],
        'password': config['password'],
    })
    if 'result' not in r.json():
        LOGGER.warning(r.json())
        r.json()['result'] # Чтобы бросить KeyError

    yield { 'token': r.json()['result']['token'] }


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
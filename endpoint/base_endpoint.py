from pytest_testconfig import config
import requests
import functools
import random
from helper.logger import LOGGER


class BaseEndpoint(object):

    PATH = ''
    APPROVE_PATH = ''
    
    def __init__(self, session, token=None):
        self.session = session
        self.token = token
        self.url = config['base_url'] + self.PATH


    def auth_before(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if self.token is None:
                r = requests.post(config['auth_server'] + 'netris/login', json={
                    'login': config['login'],
                    'password': config['password'],
                })
                self.token = { 'token': r.json()['result']['token'] }

            body = {
                ** self.token,
                ** kwargs.get('json', {})
            }
            kwargs['json'] = body
            return func(self, *args, **kwargs)
        return wrap


    @auth_before
    def approve_add(self, **kwargs):
        s = self.session
        url = config['base_url'] + self.APPROVE_PATH + 'add'
        return s.post(url, **kwargs)


    @auth_before
    def approve_begin(self, **kwargs):
        s = self.session
        url = config['base_url'] + self.APPROVE_PATH + 'begin'
        return s.post(url, **kwargs)

    @auth_before
    def approve(self, **kwargs):
        s = self.session
        url = config['base_url'] + self.APPROVE_PATH + 'approve'
        return s.post(url, **kwargs)


    @auth_before
    def commit(self, **kwargs):
        s = self.session
        url = config['base_url'] + self.APPROVE_PATH + 'commit'
        return s.post(url, **kwargs)


    @auth_before
    def get_random(self, **kwargs):
        c = self.count().json()['result']
        offset = random.randint(0, c-1)
        return self.get(json={"limit": 1, "offset": offset}).json()['result'][0]


    @auth_before
    def get(self, **kwargs):
        s = self.session
        return s.post(self.url + 'get', **kwargs)


    @auth_before
    def get_by_id(self, val, **kwargs):
        return self.get_by('id', val, **kwargs)


    @auth_before
    def get_by(self, attr, val, **kwargs):
        body = {
            ** kwargs['json'],
            "filter_by": {"attribute": attr, "operator": "=", "value": val}
        }
        kwargs['json'] = body
        return self.session.post(self.url + 'get', **kwargs)

    
    @auth_before
    def update(self, **kwargs):
        s = self.session
        return s.post(self.url + 'update', **kwargs)


    @auth_before
    def update_by_filter(self, **kwargs):
        s = self.session
        return s.post(self.url + 'update_by_filter', **kwargs)


    @auth_before
    def delete(self, **kwargs):
        s = self.session
        return s.post(self.url + 'delete', **kwargs)

    
    @auth_before
    def delete_by_ids(self, ids: list, **kwargs):
        LOGGER.info(f"Deleting {ids} ...")
        r = self.delete(json={
            "filter_by": {
                "attribute": "id", "operator": "in", "value": ids
            }
        })
        assert r.status_code == 200
        LOGGER.info(f"\t OK: {r.json()}")
        return r


    @auth_before
    def count(self, **kwargs):
        s = self.session
        return s.post(self.url + 'count', **kwargs).json()['result']


    @auth_before
    def add(self, **kwargs):
        s = self.session
        return s.post(self.url + 'add', **kwargs)

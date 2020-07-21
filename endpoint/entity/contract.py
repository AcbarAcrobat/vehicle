from endpoint import BaseEndpoint
from pytest_testconfig import config


class Contract(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["immovable_url"] + 'entity/contract/'

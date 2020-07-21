from endpoint import BaseEndpoint
from pytest_testconfig import config


class MobileOperator(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["vehicle_url"] + 'entity/mobile_operator/'

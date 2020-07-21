from endpoint import BaseEndpoint
from pytest_testconfig import config


class VehicleInformation(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["vehicle_url"] + 'entity/vehicle_information/'

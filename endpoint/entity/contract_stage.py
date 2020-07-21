from endpoint import BaseEndpoint
from pytest_testconfig import config


class ContractStage(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["immovable_url"] + 'entity/contract_stage/'

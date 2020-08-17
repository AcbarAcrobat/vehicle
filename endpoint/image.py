from endpoint import BaseEndpoint
from pytest_testconfig import config
import os
from pathlib import Path
# import numpy


class Image(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["vehicle_url"] + 'image/'

    @BaseEndpoint.auth_before
    def upload(self, byte_array, dist, mime, **kwargs):
        url = self.URL + f"upload?name={dist}"
        s = self.session

        return s.post(
            url,
            data=byte_array,
            headers={'Content-Type': mime}
        )


    @BaseEndpoint.auth_before
    def get(self, id_, **kwargs):
        """
        request url: /image/get
        request body : {"id": int}
        """

        s = self.session
        url = self.URL + "get"
        return s.post(url, json={"id": id_})
        
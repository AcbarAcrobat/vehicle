from endpoint import BaseEndpoint
from pytest_testconfig import config
import os
from pathlib import Path
# import numpy


class File(BaseEndpoint):

    def __init__(self, session):
        super().__init__(session)
        self.URL = config["vehicle_url"] + 'file/'

    @BaseEndpoint.auth_before
    def upload(self, file_name, dist, mime, **kwargs):
        url = self.URL + f"upload?name={dist}"
        s = self.session
        path = Path.cwd().joinpath("_data", file_name)
        with open(path, 'rb') as file:
            data = file.read()
        return s.post(
            url,
            data=data,
            headers={'Content-Type': mime}
        )


    @BaseEndpoint.auth_before
    def get(self, id_, **kwargs):
        """
        request url: /file/get
        request body : {"id": int}
        """

        s = self.session
        url = self.URL + "get"
        return s.post(url, json={"id": id_})

    def check_size_before_after(self, file_name, size_after):
        from truth.truth import AssertThat
        path = Path.cwd().joinpath("_data", file_name)
        with open(path, 'rb') as file:
            data = file.read()
        AssertThat(data).IsEqualTo(size_after)

import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat
from endpoint.vehicle_file import VehicleFile
import numpy


class TestFile:


    @pytest.mark.parametrize("file_name", [
                            "steam_latest.deb", 
                            "Honda_CB750.pdf",
                            "MAN_FFMPEG.odt",
                            "tasks.py", 
                            "viewtopic.html"])
    def test_file_upload_and_get(self, faker, session, file_name):
        i = VehicleFile(session)
        name = faker.uuid4()
        r = i.upload(file_name, name, "").json()
        AssertThat(r["result"]).IsInstanceOf(int)
        AssertThat(r["done"]).IsTrue()
        LOGGER.info(r)
        id_ = r["result"]

        r = i.get(id_)
        LOGGER.info(r.headers)
        i.check_size_before_after(file_name, r.content)
        AssertThat(r.headers["Content-Disposition"]).Contains(name)
        

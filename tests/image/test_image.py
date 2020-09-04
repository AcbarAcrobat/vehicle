import pytest
import allure
from helper import LOGGER
from truth.truth import AssertThat
from endpoint.vehicle_image import VehicleImage
import numpy


class TestImage:

    # def test_image_upload(self, faker, session):
    #     i = VehicleImage(session)
    #     image = bytes(numpy.random.rand(30,30,3) * 255)
    #     r = i.upload(image, faker.uuid4(), "image/png").json()
    #     """
    #     {
    #         "link": "/image/get?token=null&id=295424",
    #         "result": 295424,
    #         "done": true
    #     }
    #     """
    #     LOGGER.info(r)
    #     AssertThat(r["result"]).IsInstanceOf(int)
    #     AssertThat(r["done"]).IsTrue()

    def test_image_upload_and_get(self, faker, session):
        """
        request url: /image/get
        request body : {"id": int}
        answer: b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\xa8\x00\x00\x02\xa0\x08\x02\x00\x00\x000<\xd2%\x00\x00'
        """
        i = VehicleImage(session)
        file_name = faker.uuid4()
        image = bytes(numpy.random.rand(30, 30, 3) * 255)

        r = i.upload(image, file_name, "image/png").json()
        AssertThat(r["result"]).IsInstanceOf(int)
        AssertThat(r["done"]).IsTrue()
        LOGGER.info(r)
        id_ = r["result"]

        r = i.get(id_)
        LOGGER.info(r.headers)
        AssertThat(r.content).IsEqualTo(image)
        AssertThat(r.headers["Content-Disposition"]).Contains(file_name)
        

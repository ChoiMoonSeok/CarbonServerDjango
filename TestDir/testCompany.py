import json

from django.test import TestCase, Client

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
from Company import serializer as ComSerial
import TestFunc


class CompanyStructTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()

    def testGetStruct(self):
        response = self.client.get("/Company/Organization/삼성")
        data = json.loads(response.content)
        self.assertEqual(data["Children"][0]["ComName"], "삼성전자")
        self.assertEqual(data["Children"][1]["ComName"], "삼성생명")
        self.assertEqual(data["Children"][0]["Children"][0]["ComName"], "삼성디스플레이")

    def testCompanyRootPut(self):
        response = self.client.put(
            "/Company/PreviewInfo/삼성",
            {
                "ComName": "순양",
                "Classification": "모회사",
                "Description": "재벌집 막내 아들",
                "Location": "서울",
                "Chief": "이재용",
                "Admin": "이재용",
            },
            content_type="application/json",
        )
        data = json.loads(response.content)
        print(data)
        self.assertEqual(data["ComName"], "순양")

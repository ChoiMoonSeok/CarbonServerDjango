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
        response = self.client.get("/Company/Organization/samsung")
        data = json.loads(response.content)
        self.assertEqual(data["Children"][0]["ComName"], "삼성전자")
        self.assertEqual(data["Children"][1]["ComName"], "삼성생명")
        self.assertEqual(data["Children"][0]["Children"][0]["ComName"], "삼성디스플레이")

    def testCompanyRootPut(self):
        response = self.client.put(
            "/Company/PreviewInfo/samsung",
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
        self.assertEqual(data["ComName"], "순양")

    def testCompanyNotExist(self):
        response = self.client.put(
            "/Company/PreviewInfo/삼성자동차",
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
        self.assertEqual(data, "This Company/Department does not exist.")

    def testCompanySimpleGet(self):
        response = self.client.get("/Company/Organization/Simple/삼성전자")
        data = json.loads(response.content)
        self.assertEqual(data[0]["category"], 1)

    def testPreviewGet(self):
        response = self.client.get("/Company/Preview/samsung")
        data = json.loads(response.content)
        self.assertEqual(data["Name"], "samsung")
        self.assertEqual(data["Scopes"][0], 40.0)
        self.assertEqual(data["Scopes"][1], 40.0)
        self.assertEqual(data["Scopes"][2], 20.0)
        self.assertEqual(data["EmissionList"][11]["출장"], 40.0)

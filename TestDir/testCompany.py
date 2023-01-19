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
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testGetStruct(self):
        response = self.client.get(
            "/Company/Organization/samsung",
            **self.Auth,
        )
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
            **self.Auth,
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
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "This Company/Department does not exist.")

    def testCompanySimpleGet(self):
        response = self.client.get(
            "/Company/Organization/Simple/삼성전자",
            **self.Auth,
        )
        data = json.loads(response.content)
        self.assertEqual(data[0]["category"], 1)

    def testPreviewGetRoot(self):
        response = self.client.get(
            "/Company/Preview/samsung/2022-12-01/2023-01-01",
            **self.Auth,
        )
        data = json.loads(response.content)
        self.assertEqual(data["Name"], "samsung")
        self.assertEqual(data["Scopes"][0], 20.0)
        self.assertEqual(data["Scopes"][1], 20.0)
        self.assertEqual(data["Scopes"][2], 0.0)
        self.assertEqual(data["EmissionList"][12]["출장"], 20.0)

    def testPreviewGetNotRoot(self):
        response = self.client.get(
            "/Company/Preview/삼성전자/2023-01-01/2023-01-31",
            **self.Auth,
        )
        data = json.loads(response.content)
        self.assertEqual(data["Name"], "삼성전자")

    def testCompanyDelNotRoot(self):
        response = self.client.delete(
            "/Company/PreviewInfo/{}".format("삼성전자"), **self.Auth
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Delete Complete")
        self.assertEqual(
            len(
                ComModel.Department.objects.filter(
                    RootCom=ComModel.Company.objects.get(ComName="samsung")
                )
            ),
            1,
        )

    def testCompanyDelRoot(self):
        response = self.client.delete(
            "/Company/PreviewInfo/{}".format("samsung"), **self.Auth
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Delete Complete")
        self.assertEqual(
            len(
                ComModel.Department.objects.filter(
                    RootCom=ComModel.Company.objects.get(ComName="samsung")
                )
            ),
            0,
        )

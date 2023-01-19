import json
import datetime

from django.test import TestCase

import TestFunc


class CarbonGetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testCarbonGetRoot(self):
        response = self.client.get("/CarbonEmission/{}".format("samsung"), **self.Auth)
        data = json.loads(response.content)
        self.assertEquals(len(data), 5)

    def testCarbonGetNotRoot(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성전자"), **self.Auth)
        data = json.loads(response.content)
        self.assertEquals(len(data), 3)

    def testCompanyNotExist(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성자"), **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(data, "This Company/Department doesn't exist.")


class CarbonDelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testDeleteCarbonRight(self):
        response = self.client.delete("/CarbonEmission/{}".format(5), **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(data, "Delete Success")

    def testDeleteCarbonBad(self):
        response = self.client.delete("/CarbonEmission/{}".format(10), **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(data, "Request Data Doesn't Exist")


class CarbonPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testEnterCarbonNotRoot(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("삼성전자"),
            {
                "Type": "고정연소",
                "DetailType": "원유",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "Category": 10,
                    "CarbonActivity": "최문석 출장",
                    "usage": 20.0,
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonRoot(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "이동연소",
                "DetailType": "경유",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "Category": 10,
                    "CarbonActivity": "최문석 출장",
                    "usage": 20.0,
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")


class CarbonPutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testPut(self):
        response = self.client.put(
            "/CarbonEmission/{}".format(4),
            {
                "Type": "이동연소",
                "DetailType": "경유",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "Category": 10,
                    "CarbonActivity": "최문석 출장",
                    "usage": 25.0,
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )

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
                    "usage": "20.0/kg",
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
                    "usage": "20.0/kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonAnimal(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "대학소유동물",
                "DetailType": "송아지",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "usage": "12/마리",
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "마리",
                    "Chief": "이재용",
                    "kind": "혐기성늪",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonWasteFacilityBurning(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "폐기물처리시설(소각)",
                "DetailType": "섬유",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "usage": "12/ton",
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "ton",
                    "Chief": "이재용",
                    "kind": "연속식 - 고정상",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonWasteFacilityFoul(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "폐기물처리시설(하수처리)",
                "DetailType": "하수처리",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "usage": "12/ton",
                    "R": 10,
                    "BODIN": 10,
                    "BODOUT": 10,
                    "TNIN": 10,
                    "TNOUT": 10,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "ton",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonWasteFacilityWasteWater(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "폐기물처리시설(폐수)",
                "DetailType": "폐수",
                "CarbonData": {
                    "StartDate": datetime.date.today(),
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "usage": "12/ton",
                    "R": 10,
                    "CODIN": 10,
                    "CODOUT": 10,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "ton",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Add Carbon Data Success")

    def testEnterCarbonWrongCarbon(self):
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
                    "usage": "20.0/kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Wrong Carbon Data")

    def testEnterCarbonWrongCarbonInfo(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "이동연소",
                "DetailType": "경유",
                "CarbonData": {
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "usage": "20.0/kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Wrong CarbonInfo Data")

    def testEnterCarbonWrongNonUsage(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "이동연소",
                "DetailType": "경유",
                "CarbonData": {
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "usage Not Exist")

    def testEnterCarbonWrongUsage(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": "이동연소",
                "DetailType": "경유",
                "CarbonData": {
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "usage": "20.0kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Wrong data type entered in usage")

    def testEnterCarbonWrongNonType(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "DetailType": "경유",
                "CarbonData": {
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Type Not Exist")

    def testEnterCarbonWrongType(self):
        response = self.client.post(
            "/CarbonEmission/{}".format("samsung"),
            {
                "Type": 20,
                "DetailType": "경유",
                "CarbonData": {
                    "EndDate": datetime.date.today(),
                    "Location": "진주",
                    "Scope": 3,
                    "CarbonActivity": "최문석 출장",
                    "Category": 10,
                    "usage": "20.0/kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Wrong data type entered in Type")


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
                    "usage": "25.0/kg",
                    "CarbonUnit": "kg",
                    "Chief": "이재용",
                },
            },
            **self.Auth,
            content_type="application/json",
        )
        print(response)

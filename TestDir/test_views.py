import json
import datetime

from django.urls import reverse
from django.test import TestCase

import Carbon.models
import test_func


class OrganizationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_func.CreateSamsung()

    def testOrganizaionSamsung(self):
        response = self.client.get("/Organization/{}".format("삼성"))
        data = json.loads(response.content)
        self.assertEquals(data["Children"][0]["Children"][0]["id"], 3)


class PreviewTest(TestCase):
    def setUp(self):
        test_func.CreateSamsung()
        Carbon.models.Carbon.objects.create(
            Content="불량 소각",
            Data=10.0,
            unit="kg",
            CarbonEmission=10,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=0,
        )
        Carbon.models.Carbon.objects.create(
            Content="쓰레기 소각",
            Data=15.0,
            unit="kg",
            CarbonEmission=15,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=0,
        )
        Carbon.models.Carbon.objects.create(
            Content="불량 소각",
            Data=10.0,
            unit="kg",
            CarbonEmission=10,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=1,
        )
        Carbon.models.Carbon.objects.create(
            Content="쓰레기 소각",
            Data=15.0,
            unit="kg",
            CarbonEmission=15,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=1,
        )

    def testPreviewGet(self):
        response = self.client.get("/Preview/{}".format("삼성전자"))
        data = json.loads(response.content)
        self.assertEqual(data["고정연소"], 25.0)
        self.assertEqual(data["이동연소"], 25.0)

    def testPreviewInfoRoot(self):
        Input = {
            "DepartName": "(주)삼성",
            "Classification": "모회사",
            "chief": "이재용",
            "Description": "모회사",
            "admin": "이재용",
            "location": "busan",
        }
        response = self.client.put(
            "/PreviewInfo/{}".format("삼성"), data=json.dumps(Input)
        )
        data = json.loads(response.content)
        self.assertEqual(data["Description"], "모회사")

    def testPreviewInfoDepart(self):
        Input = {
            "DepartName": "(주)삼성전자",
            "Classification": "계열사",
            "chief": "노태문",
            "Description": "자회사",
            "admin": "노태문",
            "location": "busan",
        }
        response = self.client.put(
            "/PreviewInfo/{}".format("삼성전자"), data=json.dumps(Input)
        )
        data = json.loads(response.content)
        self.assertEqual(data["Description"], "자회사")


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_func.CreateSamsung()

    def testUserGet(self):
        response = self.client.get("/User/{}".format("삼성"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["Name"], "이재용")
        self.assertEqual(data[1]["Name"], "노태문")
        self.assertEqual(data[2]["Name"], "고동진")
        self.assertEqual(data[3]["Name"], "경계현")


class CarbonEmissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_func.CreateSamsung()
        Carbon.models.Carbon.objects.create(
            Content="불량 소각",
            Data=10.0,
            unit="kg",
            CarbonEmission=10,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성생명"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=0,
        )
        Carbon.models.Carbon.objects.create(
            Content="쓰레기 소각",
            Data=15.0,
            unit="kg",
            CarbonEmission=15,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성생명"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=0,
        )
        Carbon.models.Carbon.objects.create(
            Content="불량 소각",
            Data=10.0,
            unit="kg",
            CarbonEmission=10,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=1,
        )
        Carbon.models.Carbon.objects.create(
            Content="쓰레기 소각",
            Data=15.0,
            unit="kg",
            CarbonEmission=15,
            StartDate=datetime.datetime.now(),
            EndDate=datetime.datetime.now(),
            location="busan",
            Scope=1,
            chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
            upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
            Mother=Carbon.models.Company.objects.get(ComName="삼성"),
            Category=1,
        )

    def testCarbonEmissionGet(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성전자"))
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def testCarbonEmissionPost(self):
        Input = {
            "Content": "폐기물 처리",
            "Data": 2.8,
            "unit": "kg",
            "CarbonEmission": 2.8,
            "StartDate": "{}".format("2022-12-05"),
            "EndDate": "{}".format("2022-12-05"),
            "location": "busan",
            "chief": "노태문",
            "admin": "노태문",
            "upper": "삼성전자",
            "Mother": "삼성",
            "Scope": 1,
            "Category": 1,
            "Division": "{'건물명':'본관', '폐기물 처리 형태':'매립', '폐기물 종류':'생활', '배출 주체':'한국전력공사', '폐기물 배출량':'123456'}",
        }
        response = self.client.post(
            "/CarbonEmission/{}".format("삼성전자"),
            data=Input,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

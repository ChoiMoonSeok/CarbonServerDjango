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
        response = self.client.get("/Preview/{}/{}".format("삼성", "삼성전자"))
        data = json.loads(response.content)
        self.assertEqual(data["고정연소"], 25.0)
        self.assertEqual(data["이동연소"], 25.0)


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_func.CreateSamsung()

        Carbon.models.User_Employee.objects.create(
            Name="노태문",
            PhoneNum="123456789",
            Email="1234@naver.com",
            Company="삼성",
            JobPos="사장",
            IdentityNum="2",
            Authorization=1,
        )
        Carbon.models.User_Employee.objects.create(
            Name="고동진",
            PhoneNum="123456789",
            Email="12345@naver.com",
            Company="삼성",
            JobPos="사원",
            IdentityNum="3",
            Authorization=2,
        )
        Carbon.models.User_Employee.objects.create(
            Name="경계현",
            PhoneNum="123456789",
            Email="123456@naver.com",
            Company="삼성",
            JobPos="대리",
            IdentityNum="4",
            Authorization=3,
        )

    def testUserGet(self):
        response = self.client.get("/User/{}".format("삼성"))
        data = json.loads(response.content)
        self.assertEqual(data[0]["Name"], "이재용")
        self.assertEqual(data[1]["Name"], "노태문")
        self.assertEqual(data[2]["Name"], "고동진")
        self.assertEqual(data[3]["Name"], "경계현")

import json

from django.test import TestCase

import TestFunc
from Company import models as ComModel


class EmployeeGetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)
        cls.Auth = TestFunc.Auth(cls.token)

    def testRootGet(self):
        response = self.client.get("/User/samsung", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

    def testNotRootGet(self):
        response = self.client.get("/User/삼성전자", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def testNotExistGet(self):
        response = self.client.get("/User/삼성자동차", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(data, "This Company does not exist")


class EmployeeLogInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)

    def testLoginRight(self):
        response = self.client.post(
            "/User/Login",
            {"Email": "1234@naver.com", "password": "hi"},
        )
        data = json.loads(response.content)
        self.assertEqual(data["Email"], "1234@naver.com")


class EmployeeSignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.token = json.loads(cls.token.content)

    def testSignUpFirst(self):
        response = self.client.post(
            "/User/SignUp",
            data={
                "Email": "54321@naver.com",
                "DetailInfo": {
                    "Name": "최문석1",
                    "PhoneNum": "123456789",
                    "JobPos": "사원",
                    "IdentityNum": 13,
                    "RootCom": "samsung",
                    "BelongCom": "삼성전자",
                    "Authorization": 0,
                },
                "password": "abcdefg",
            },
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Sign Up Success")

    def testSignUpOther(self):
        response = self.client.post(
            "/User/SignUp",
            data={
                "Email": "54321@naver.com",
                "DetailInfo": {
                    "Name": "최문석1",
                    "PhoneNum": "123456789",
                    "JobPos": "사원",
                    "IdentityNum": 13,
                    "RootCom": "samsung",
                    "BelongCom": "삼성전자",
                    "Authorization": 0,
                },
                "password": "abcdefg",
            },
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Sign Up Success")


class EmployeeAddTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()
        cls.token = TestFunc.LogIn()
        cls.Auth = TestFunc.Auth(json.loads(cls.token.content))

    def testAddEmp(self):
        response = self.client.post(
            "/User/{}".format("삼성전자"),
            data={
                "Name": "최문석1",
                "PhoneNum": "123456789",
                "JobPos": "사원",
                "IdentityNum": 13,
                "RootCom": "samsung",
                "BelongCom": "삼성전자",
                "Authorization": 0,
            },
            **self.Auth,
            content_type="application/json",
        )
        data = json.loads(response.content)
        self.assertEqual(data, "Create Employee Success")

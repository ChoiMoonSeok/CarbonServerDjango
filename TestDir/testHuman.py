import json

from django.test import TestCase
import TestFunc


class EmployeeTest(TestCase):
    def setUp(self):
        TestFunc.CreateSamsung()
        self.token = TestFunc.LogIn()
        self.token = json.loads(self.token.content)
        self.Auth = TestFunc.Auth(self.token)

    def testRootGet(self):
        response = self.client.get("/User/samsung", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def testNotRootGet(self):
        response = self.client.get("/User/삼성전자", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def testNotExistGet(self):
        response = self.client.get("/User/삼성자동차", **self.Auth)
        data = json.loads(response.content)
        self.assertEqual(data, "This Company does not exist")

    def testLoginRight(self):
        response = self.client.post(
            "/User/Login",
            {"Email": "1234@naver.com", "password": "hi"},
        )
        data = json.loads(response.content)
        self.assertEqual(data, 0)

    def testSignUpRight(self):
        response = self.client.post("/User/SignUp", {"Email": ""})

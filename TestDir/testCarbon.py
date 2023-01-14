import json

from django.test import TestCase, Client

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
import TestFunc


class CarbonGetTest(TestCase):
    def setUp(self):
        TestFunc.CreateSamsung()
        self.token = TestFunc.LogIn()
        self.token = json.loads(self.token.content)
        self.Auth = TestFunc.Auth(self.token)

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
        
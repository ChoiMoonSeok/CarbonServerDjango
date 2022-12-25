import json

from django.test import TestCase, Client

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
import TestFunc


class CarbonGetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()

    def testCarbonGetRoot(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성"))
        data = json.loads(response.content)
        self.assertEquals(len(data), 5)
    
    def testCarbonGetNotRoot(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성전자"))
        data = json.loads(response.content)
        self.assertEquals(len(data), 3)

    def testCompanyNotExist(self):
        response = self.client.get("/CarbonEmission/{}".format("삼성자"))
        data = json.loads(response.content)
        self.assertEqual(data, "This Company/Department doesn't exist.")
        
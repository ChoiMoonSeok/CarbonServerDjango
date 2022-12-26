import json

from django.test import TestCase, Client

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
import TestFunc


class CompanyStructTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TestFunc.CreateSamsung()

    def testGetStruct(self):
        response = self.client.get("/Company/Organization/삼성")
        data = json.loads(response.content)
        self.assertEqual(data["Children"][0]["ComName"], "삼성전자")
        self.assertEqual(data["Children"][1]["ComName"], "삼성생명")
        self.assertEqual(data["Children"][0]["Children"][0]["ComName"], "삼성디스플레이")

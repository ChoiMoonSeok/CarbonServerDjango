import json

from django.test import TestCase
import TestFunc


class EmployeeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.host = "/User/"
        TestFunc.CreateSamsung()

    def testRootGet(self):
        response = self.client.get("/User/삼성")
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def testNotRootGet(self):
        response = self.client.get("/User/삼성전자")
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def testNotExistGet(self):
        response = self.client.get("/User/삼성자동차")
        data = json.loads(response.content)
        self.assertEqual(data, "This Company does not exist")

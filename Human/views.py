import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from Human import models as HuModel
from Human import serializer
from Company import models as ComModel
import func

# 사용자에 대한 api 함수


class User_EmployeeQuery(APIView):
    """
    모든 사용자를 리스트 형태로 반환하는 Api
    ---
    # 사용자
    """

    def get(self, request, Company, format=None):
        U_Root = ComModel.Company.objects.get(ComName="삼성")  # 로그인 구현 후 변경 예정
        try:
            Root = ComModel.Department.objects.get(
                RootCom=U_Root, DepartmentName=Company
            )
        except ComModel.Department.DoesNotExist:
            try:
                Root = ComModel.Company.objects.get(ComName=Company)
            except ComModel.Company.DoesNotExist:
                return Response(
                    "This Company does not exist", status=status.HTTP_404_NOT_FOUND
                )

        if type(Root) == ComModel.Company:
            Employee = HuModel.Employee.objects.filter(RootCom=Root)
            serial = serializer.EmployeeSerializer(Employee, many=True)
            return Response(serial.data, status=status.HTTP_200_OK)

        else:
            Departs = [Root]
            func.getChildDepart(U_Root, Root.SelfCom, Departs)

            Employee = []
            for depart in Departs:

                temp = HuModel.Employee.objects.filter(RootCom=U_Root, BelongCom=depart)
                serial = serializer.EmployeeSerializer(temp, many=True)

                Employee.append(serial.data)

            return Response(Employee, status=status.HTTP_200_OK)

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
    @swagger_auto_schema(
        operation_summary="입력한 회사와 그 자회사의 모든 직원을 가져오는 Api",
        responses={200: "API가 정상적으로 동작하고 종료 됨", 404: "입력한 회사가 존재하지 않음"},
    )
    def get(self, request, Company, format=None):
        """
        입력한 회사와 해당 회사의 자회사의 모든 소속 직원들의 정보를 가져옵니다.
        ex) 삼성전자를 호출하면 삼성전자의 모든 직원과 삼성전자의 자회사인 삼성디스플레이의 모든 직원이 반환 됨
        """
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

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from Carbon.serializer import *
import func

# 사용자에 대한 api 함수

User_root = "삼성"


class User_EmployeeQuery(APIView):
    """
    모든 사용자를 리스트 형태로 반환하는 Api
    ---
    # 사용자
    """

    @swagger_auto_schema(
        method="get",
        operation_id="입력한 회사 및 연결 자회사의 모든 사원 조회",
        operation_description="입력한 회사와 연결 자회사의 모든 사원들의 정보를 리스트 형태로 반환받습니다.",
    )
    @api_view(["GET"])
    def get(self, request, Company, format=None):
        Users = User_Employee.objects.filter(Company=Company)
        serializer = User_EmployeeSerializer(Users, many=True)
        return Response(serializer.data)


class CompanyQuery(APIView):
    """
    회사와 관련된 값들을 다루는 api
    """

    def get(self, request, CompanyName, format=None):
        """
        지주회사가 동일한 모든 회사, 부서를 계층을 가진 형태로 반환.\
        ex) 삼성 dict 내부의 Children에 리스트 형태로 자회사 혹은 부서가 저장됨.
        """
        ComId = Company.objects.get(ComName=CompanyName)
        Departments = Department.objects.filter(Mother=ComId)
        serializer = DepartmentSerializer(Departments, many=True)

        result = {
            "DepartmentName": CompanyName,
            "depth": 0,
            "Scope1": ComId.Scope1,
            "Scope2": ComId.Scope2,
            "Scope3": ComId.Scope3,
            "Children": [],
        }

        for i in serializer.data:
            i = dict(i)
            i["Children"] = []
            func.put_struct(result, i)

        return Response(result, status=status.HTTP_201_CREATED)


class PreviewQuery(APIView):
    """
    프리뷰와 관련된 내용을 다루는 api
    """

    def get(self, request, Depart, format=None):
        """요청한 부서의 탄소 배출량을 탄소 배출 원인별로 계산해 반환"""

        # 요청한 user의 모회사 확인
        # Mother = User_Employee.objects.get(UID=jwt에서 추출한 id).Mother
        Mother = User_root

        # root의 id와 Department의 id 가져오기
        Root_Id = Company.objects.get(ComName=Mother)
        Upper_Id = Department.objects.get(DepartmentName=Depart)
        Data = Carbon.objects.filter(Mother=Root_Id, upper=Upper_Id)

        ans = {}

        for i in Data:
            try:
                ans[func.CarbonCategory[i.Category]] += i.CarbonEmission
            except KeyError:
                ans[func.CarbonCategory[i.Category]] = i.CarbonEmission

        return Response(ans, status=status.HTTP_201_CREATED)


class PreviewInfoQuery(APIView):
    def put(self, request, Depart, format=None):
        """요청한 부서 혹은 회사의 정보를 변경"""

        request = json.loads(request.body)

        # 요청받은 즉 변경할 row 가져오기
        try:
            ChangeData = Company.objects.get(ComName=Depart)
            ChangeData.ComName = request["DepartName"]
            ChangeData.Classification = request["Classification"]
            ChangeData.chief = User_Employee.objects.get(Name=request["chief"])
            ChangeData.Description = request["Description"]
            ChangeData.admin = User_Employee.objects.get(Name=request["admin"])
            ChangeData.location = request["location"]
            ChangeData.save()

            serializer = CompanySerializer(ChangeData)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Company.DoesNotExist:
            Mother_id = Company.objects.get(ComName=User_root)  # user의 모회사 확인

            ChangeData = Department.objects.get(Mother=Mother_id, DepartmentName=Depart)
            ChangeData.DepartmentName = request["DepartName"]
            ChangeData.Classification = request["Classification"]
            ChangeData.chief = User_Employee.objects.get(Name=request["chief"])
            ChangeData.Description = request["Description"]
            ChangeData.admin = User_Employee.objects.get(Name=request["admin"])
            ChangeData.location = request["location"]
            ChangeData.save()

            serializer = DepartmentSerializer(ChangeData)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarbonEmissionQuery(APIView):
    def get(self, request, Depart, format=None):
        """요청받은 부서, 회사의 모든 탄소 배출 반환"""
        Mother_id = Company.objects.get(ComName=User_root)
        try:  # 요청 받은 회사가 루트, 모회사인 경우
            Upper_id = Department.objects.get(DepartmentName=Depart)
            data = Carbon.objects.filter(Mother=Mother_id, upper=Upper_id)
        except Department.DoesNotExist:
            data = Carbon.objects.filter(Mother=Mother_id)

        serializer = CarbonSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, Depart, format=None):
        """탄소 사용량 데이터 입력"""
        InputData = json.loads(request.body)
        Mother_id = User_root
        chief_id = User_Employee.objects.get(Name=InputData["chief"], Mother=Mother_id)
        Mother_id_upper = Company.objects.get(ComName=Mother_id)
        upper_id = Department.objects.get(Mother=Mother_id_upper, DepartmentName=Depart)

        # 요청한 탄소 배출 현황 생성
        Carbon.objects.create(
            Content=InputData["Content"],
            Data=InputData["Data"],
            unit=InputData["unit"],
            CarbonEmission=InputData["CarbonEmission"],
            StartDate=InputData["StartDate"],
            EndDate=InputData["EndDate"],
            location=InputData["location"],
            chief=chief_id,
            upper=upper_id,
            Mother=Mother_id_upper,
            Scope=InputData["Scope"],
            Category=InputData["Category"],
            Division=InputData["Division"],
        )

        # 모회사의 모든 탄소 배출 가져오기
        data = Carbon.objects.filter(Mother=Mother_id_upper, upper=upper_id)
        serializer = CarbonSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

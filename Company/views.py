import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


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

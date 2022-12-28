import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

import func
from . import models
from . import serializer


class CompanyQuery(APIView):
    @swagger_auto_schema(
        operation_summary="조직 설계도를 반환하는 Api",
        responses={201: "API가 정상적으로 실행 됨", 200: "API가 정상적으로 실행 됨"},
    )
    def get(self, request, CompanyName, format=None):
        """
        지주회사가 동일한 모든 회사, 부서를 계층을 가진 형태로 반환합니다.\n
        ex) 삼성 dict 내부의 Children에 리스트 형태로 자회사 혹은 부서가 저장됨.
        """
        UserRoot = models.Company.objects.get(ComName="삼성")  # 유저의 루트 컴퍼니, 로그인 구현 후에는 삭제
        ComId = models.Company.objects.get(ComName=CompanyName)

        result = serializer.CompanySerializer(ComId)
        result = result.data
        result["Children"] = []

        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if ComId.id == UserRoot.id:
            func.getStruct(UserRoot, None, result)
        else:
            func.getStruct(UserRoot, ComId, result)

        return Response(result, status=status.HTTP_200_OK)


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

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

import func
from Company import models as ComModel
from Company import serializer as ComSerial
from Human import models as HuModel


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
        UserRoot = ComModel.Company.objects.get(
            ComName="삼성"
        )  # 유저의 루트 컴퍼니, 로그인 구현 후에는 삭제
        ComId = ComModel.Company.objects.get(ComName=CompanyName)

        result = ComSerial.CompanySerializer(ComId)
        result = result.data
        result["Children"] = []

        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if ComId.id == UserRoot.id:
            func.getStruct(UserRoot, None, result)
        else:
            func.getStruct(UserRoot, ComId, result)

        return Response(result, status=status.HTTP_200_OK)


class PreviewQuery(APIView):
    @swagger_auto_schema(operation_summary="Preview 화면에서 필요한 값들을 반환하는 Api")
    def get(self, request, Depart, format=None):
        """
        요청한 부서의 탄소 배출량을 탄소 배출 원인별로 계산해 반환\n
        수식의 입력이 완료된 이후 개발이 진행될 필요성이 보임
        """

        # 요청한 user의 모회사 확인
        UserRoot = ComModel.Company.objects.get(
            ComName="삼성"
        )  # 유저의 루트 컴퍼니, 로그인 구현 후에는 삭제

        HeadDepart = ComModel.Department.objects.get(DepartmentName=Depart)


class PreviewInfoQuery(APIView):
    @swagger_auto_schema(
        operation_summary="Company 혹은 Department의 데이터를 변경하는 Api",
        request_body=ComSerial.CompanySerializer,
        responses={202: "데이터가 문제없이 변경 됨", 406: "입력한 데이터에 오류가 있음, 수정 요함"},
    )
    def put(self, request, Depart, format=None):
        """
        요청한 부서 혹은 회사의 정보를 변경\n
        아래 data에 Scope1, 2, 3을 제외한 나머지 값들은 모두 채워져 있어야만 변경이 가능\n
        Chief와 Admin의 경우 해당 회사, 부서의 책임자와 관리자의 이름을 각각 입력\n
        """

        request = json.loads(request.body)

        UserRoot = ComModel.Company.objects.get(
            ComName="삼성"
        )  # 유저의 루트 컴퍼니, 로그인 구현 후에는 삭제

        # 요청받은 즉 변경할 row 가져오기
        try:
            ChangeData = ComModel.Department.objects.get(
                RootCom=UserRoot, DepartmentName=Depart
            )
        except ComModel.Department.DoesNotExist:  # 변경할 것이 루트인 경우
            ChangeData = ComModel.Company.objects.get(ComName=Depart)

        if type(ChangeData) == ComModel.Department:
            ChangeData = ChangeData.SelfCom

        # 데이터 변경
        try:

            ChangeData.ComName = request["ComName"]
            ChangeData.Classification = request["Classification"]
            ChangeData.Chief = HuModel.Employee.objects.get(Name=request["Chief"])
            ChangeData.Description = request["Description"]
            ChangeData.Admin = HuModel.Employee.objects.get(Name=request["Admin"])
            ChangeData.Location = request["Location"]
            ChangeData.save()

            serial = ComSerial.CompanySerializer(ChangeData)

            return Response(serial.data, status=status.HTTP_202_ACCEPTED)

        except KeyError:  # request가 완전히 채워지지 않았음
            Response(
                "Please enter a whole data.",
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        except ValueError:  # 틀린 데이터가 있는 경우
            Response(
                "Please enter a correct data.",
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

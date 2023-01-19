import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

from . import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
from . import serializer
import func
from CarbonConstant import CarbonDef, CarbonClass
from Swag import CarSwag


class CarbonEmissionQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="요청한 회사의 모든 탄소 배출원을 반환하는 Api",
        responses={404: "입력한 회사가 존재하지 않음", 201: "API가 정상적으로 실행 됨"},
    )
    def get(self, request, Depart, format=None):
        """{Depart}를 통해 입력 받은 회사의 이름을 바탕으로, 해당 회사의 모든 탄소 배출원을 반환합니다.\n
        해당 회사의 탄소 배출 뿐만 아니라 해당 회사의 자회사, 부서의 탄소 배출원도 모두 포함합니다.\n
        하단의 Description에 탄소 배출원을 알고 싶은 회사의 사명을 입력하면 됩니다.\n
        탄소 배출원 예) 홍길동 교수님 출장, 탄소 배출량 20"""

        token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
        UserRoot = func.getRootViaJWT(token_str)

        try:  # 요청받은 회사가 루트가 아닌 경우
            Root_id = ComModel.Department.objects.get(
                DepartmentName=Depart, RootCom=UserRoot  # 로그인이 구현된 이후에는 사용자의 root와 비교
            )
        except ComModel.Department.DoesNotExist:  # 요청받은 회사가 루트인 경우
            try:
                Root_id = ComModel.Company.objects.get(ComName=Depart)
            except ComModel.Company.DoesNotExist:  # 요청받은 회사가 존재하지 않는 경우
                return Response(
                    "This Company/Department doesn't exist.",
                    status=status.HTTP_404_NOT_FOUND,
                )

        # 요청받은 회사가 루트인 경우
        if type(Root_id) == ComModel.Company:

            data = CarModel.Carbon.objects.filter(RootCom=Root_id)
            serial = serializer.CarbonSerializer(data, many=True)

            return Response(serial.data, status=status.HTTP_201_CREATED)

        else:  # 요청 받은 회사가 루트, 모회사가 아닌 경우
            Coms = [Root_id]
            func.getChildDepart(Root_id.RootCom, Root_id.SelfCom, Coms)

            CarbonList = []

            for Com in Coms:

                temp = CarModel.Carbon.objects.filter(BelongDepart=Com)
                serial = serializer.CarbonSerializer(temp, many=True)
                CarbonList += serial.data

            return Response(CarbonList, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="탄소 배출 원인을 입력하는 Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "Type": CarSwag.Type,
                "DetailType": CarSwag.DetailType,
                "CarbonData": CarSwag.CarbonData,
            },
        ),
        responses={200: "데이터 입력 성공"},
    )
    def post(self, request, Depart, format=None):
        """
        탄소 사용량 데이터를 입력하는 Api\n
        로그인한 임직원이 자신이 직장 생활에서 발생시킨 탄소 배출량을 기록\n
        """

        token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
        UserRoot = func.getRootViaJWT(token_str)

        if Depart == UserRoot.ComName:
            TargetCom = UserRoot
        else:
            TargetCom = ComModel.Department.objects.get(
                RootCom=UserRoot, DepartmentName=Depart
            )

        CarbonData = request.data

        CarType = CarbonData["Type"]
        CarDetailType = CarbonData["DetailType"]

        DataKind = CarbonDef.CarbonCateMap["{}".format(CarType)][
            "{}".format(CarDetailType)
        ]

        if DataKind in CarbonDef.CarbonCateMap["산림에의한흡수"]:
            CarTrans = DataKind.CO2_EQ(
                CarbonData["CarbonData"]["usage"],
                CarbonData["CarbonData"]["kind"],
            )
            # 탄소 배출 상수 입력 완료 후 사용량 외에 다른 입력값이 필요한 경우는 예외 처리 할 것
        elif DataKind == "에어컨":
            CarTrans = DataKind.CO2_EQ(
                CarbonData["CarbonData"]["usage"],
                CarbonData["CarbonData"]["nums"],
                CarbonData["CarbonData"]["kind"],
            )
        elif DataKind == "냉장고":
            CarTrans = DataKind.CO2_EQ(
                CarbonData["CarbonData"]["usage"], CarbonData["CarbonData"]["nums"]
            )
        else:
            CarTrans = DataKind.CO2_EQ(CarbonData["CarbonData"]["usage"])

        CarInfoTemp = CarModel.CarbonInfo.objects.create(
            StartDate=CarbonData["CarbonData"]["StartDate"],
            EndDate=CarbonData["CarbonData"]["EndDate"],
            Location=CarbonData["CarbonData"]["Location"],
            Scope=CarbonData["CarbonData"]["Scope"],
            Chief=HuModel.Employee.objects.get(
                RootCom=UserRoot, Name=CarbonData["CarbonData"]["Chief"]
            ),
            Category=CarbonDef.CarbonCategories.index(CarType),
            Division=str(CarbonData),
        )

        if type(TargetCom) == ComModel.Company:
            CarModel.Carbon.objects.create(
                CarbonActivity=CarbonData["CarbonData"]["CarbonActivity"],
                CarbonData=CarbonData["CarbonData"]["usage"],
                CarbonUnit=CarbonData["CarbonData"]["CarbonUnit"],
                CarbonTrans=CarTrans,
                RootCom=UserRoot,
                BelongDepart=None,
                CarbonInfo=CarInfoTemp,
            )
        else:
            CarModel.Carbon.objects.create(
                CarbonActivity=CarbonData["CarbonData"]["CarbonActivity"],
                CarbonData=CarbonData["CarbonData"]["usage"],
                CarbonUnit=CarbonData["CarbonData"]["CarbonUnit"],
                CarbonTrans=CarTrans,
                RootCom=UserRoot,
                BelongDepart=TargetCom,
                CarbonInfo=CarInfoTemp,
            )

        return Response("Add Carbon Data Success", status=status.HTTP_200_OK)


class CarbonFixingQuery(APIView):
    @swagger_auto_schema(
        operation_summary="입력된 탄소 배출 원인을 삭제하는 Api",
        responses={404: "입력한 회사가 존재하지 않음", 200: "API가 정상적으로 실행 됨"},
    )
    def delete(self, request, pk, format=None):
        """
        입력된 탄소 배출 원인 중 불필요한 내용을 삭제하는 Api\n
        삭제할 탄소 배출 원인의 기본키를 입력하여야 한다.
        """
        try:
            CarInfo = CarModel.Carbon.objects.get(
                id=pk
            ).CarbonInfo  # CarbonInfo가 CASCADE가 아니므로 먼저 삭제
        except CarModel.Carbon.DoesNotExist:  # 삭제할 데이터가 존재하지 않는 경우
            return Response(
                "Request Data Doesn't Exist", status=status.HTTP_404_NOT_FOUND
            )
        CarInfoId = CarInfo.id
        CarInfo.delete()  # CarbonInfo가 CASCADE가 아니므로 먼저 삭제
        CarModel.Carbon.objects.get(id=pk).delete()

        try:
            CarModel.Carbon.objects.get(id=pk)
        except CarModel.Carbon.DoesNotExist:
            try:
                CarModel.CarbonInfo.objects.get(id=CarInfoId)
            except CarModel.CarbonInfo.DoesNotExist:
                return Response("Delete Success", status=status.HTTP_200_OK)

            return Response(
                "Delete CarbonInfo Fail", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response("Delete Fail", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(operation_summary="탄소 배출 원인을 수정하는 Api")
    def put(self, request, pk, format=None):
        temp = CarModel.Carbon.objects.get(id=pk)

        InData = request.data

        return Response(0)

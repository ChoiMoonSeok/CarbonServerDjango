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

        UserRoot = func.GetUserRoot(request)

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

        UserRoot = func.GetUserRoot(request)

        if Depart == UserRoot.ComName:
            TargetCom = UserRoot
        else:
            TargetCom = ComModel.Department.objects.get(
                RootCom=UserRoot, DepartmentName=Depart
            )

        CarbonData = request.data

        CarType = CarbonData["Type"]
        CarDetailType = CarbonData["DetailType"]

        usage = float(CarbonData["CarbonData"]["usage"].split("/")[0])

        DataKind = CarbonDef.CarbonCateMap["{}".format(CarType)][
            "{}".format(CarDetailType)
        ]

        if CarDetailType in CarbonDef.CarbonCateMap["산림에의한흡수"]:
            CarTrans = DataKind.CO2_EQ(
                usage,
                CarbonData["CarbonData"]["kind"],
            )
        elif CarDetailType == "에어컨":
            CarTrans = DataKind.CO2_EQ(
                usage,
                CarbonData["CarbonData"]["nums"],
                CarbonData["CarbonData"]["kind"],
            )
        elif CarDetailType == "냉장고":
            CarTrans = DataKind.CO2_EQ(usage, CarbonData["CarbonData"]["nums"])
        else:
            CarTrans = DataKind.CO2_EQ(usage)

        CarInfoTemp = func.CreateCarbonInfo(CarbonData, UserRoot, CarType)

        if type(TargetCom) == ComModel.Company:
            func.CreateCarbon(CarbonData, CarTrans, usage, UserRoot, None, CarInfoTemp)
        else:
            func.CreateCarbon(
                CarbonData, round(CarTrans, 4), usage, UserRoot, TargetCom, CarInfoTemp
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

    @swagger_auto_schema(
        operation_summary="탄소 배출 원인을 수정하는 Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "DetailType": CarSwag.DetailType,
                "CarbonData": CarSwag.CarbonData,
            },
        ),
        responses={200: "데이터 입력 성공"},
    )
    def put(self, request, pk, format=None):
        """
        이전에 입력한 탄소 배출량 데이터를 수정하는 Api\n
        이전에 입력한 내용과 동일한 카테고리 내에서 값들을 수정\n
        불가능 예시) 고정연소인데 이동연소로 변경\n
        아래의 데이터들을 모두 입력하여야 변경 가능\n
        그렇지 않은 경우 오류가 발생함
        """

        UserRoot = func.GetUserRoot(request)

        temp = CarModel.Carbon.objects.get(id=pk)
        tempInfo = temp.CarbonInfo

        InData = request.data

        if InData["CarbonData"]["StartDate"] != None:
            tempInfo.StartDate = InData["CarbonData"]["StartDate"]
        if InData["CarbonData"]["EndDate"] != None:
            tempInfo.EndDate = InData["CarbonData"]["EndDate"]
        if InData["CarbonData"]["Location"] != None:
            tempInfo.Location = InData["CarbonData"]["Location"]
        if InData["CarbonData"]["Scope"] != None:
            tempInfo.Scope = InData["CarbonData"]["Scope"]
        if InData["CarbonData"]["Chief"] != None:
            tempInfo.Chief = HuModel.Employee.objects.get(
                RootCom=UserRoot, Name=InData["CarbonData"]["Chief"]
            )
        tempInfo.Division = str(InData)
        tempInfo.save()

        if InData["CarbonData"]["CarbonActivity"] != None:
            temp.CarbonActivity = InData["CarbonData"]["CarbonActivity"]
        if InData["CarbonData"]["usage"] != None:
            temp.CarbonData = float(InData["CarbonData"]["usage"].split("/")[0])
        if InData["CarbonData"]["CarbonUnit"] != None:
            temp.CarbonUnit = InData["CarbonData"]["CarbonUnit"]

        temp.CarbonTrans = CarbonDef.CarbonCateMap[
            "{}".format(CarbonDef.CarbonCategories[tempInfo.Category])
        ][InData["DetailType"]].CO2_EQ(
            float(InData["CarbonData"]["usage"].split("/")[0])
        )

        temp.CarbonInfo = tempInfo
        temp.save()
        tempInfo.save()
        return Response("Change Complete", status=status.HTTP_200_OK)

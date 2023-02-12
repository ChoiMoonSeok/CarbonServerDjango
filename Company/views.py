import json
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

import func
from Company import models as ComModel
from Carbon import models as CarModel
from Company import serializer as ComSerial
from Human import models as HuModel
from CarbonConstant import CarbonDef
from Swag import ComSwag


class CompanyQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="조직 설계도를 반환하는 Api",
        responses={201: "API가 정상적으로 실행 됨", 200: "API가 정상적으로 실행 됨"},
    )
    def get(self, request, CompanyName, format=None):
        """
        지주회사가 동일한 모든 회사, 부서를 계층을 가진 형태로 반환합니다.\n
        ex) 삼성 dict 내부의 Children에 리스트 형태로 자회사 혹은 부서가 저장됨.
        """

        UserRoot = func.GetUserRoot(request)

        ComId = ComModel.Company.objects.get(ComName=CompanyName)

        result = ComSerial.ComStructSerializer(ComId)
        result = result.data
        result["label"] = result["ComName"]
        result["expand"] = True
        if result["Chief"] != None:
            result["Chief"] = HuModel.Employee.objects.get(id=result["Chief"]).Name
        result["Children"] = []

        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if ComId.id == UserRoot.id:
            Trans = [0, 0, 0]
            func.getStruct(UserRoot, None, result, Trans)
        else:
            Trans = [0, 0, 0]
            func.getStruct(UserRoot, ComId, result, Trans)

        result["Scope1"] = Trans[0]
        result["Scope2"] = Trans[1]
        result["Scope3"] = Trans[2]

        return Response(result, status=status.HTTP_200_OK)


class CompanySimpleQuery(CompanyQuery):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="요청한 회사에 대한 최소한의 정보만을 반환하는 Api",
        responses={200: "Api가 정상적으로 동작함"},
    )
    def get(self, request, CompanyName, format=None):
        """
        요청한 회사에 대한 최소한의 정보를 반환하는 Api\n
        회사의 이름과 깊이만을 반환\n
        프론트엔드에서 Preview 정보 화면을 그릴 때 사용
        """

        UserRoot = func.GetUserRoot(request)

        try:
            ComId = ComModel.Department.objects.get(
                DepartmentName=CompanyName, RootCom=UserRoot
            )
        except ComModel.Department.DoesNotExist:
            ComId = UserRoot

        result = []
        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if type(ComId) == ComModel.Company:  # 루트인 경우
            func.getChildDepart(UserRoot, None, result)
            ans = [{"category": 1, "image": None, "name": ComId.ComName, "check": None}]
        else:
            func.getChildDepart(UserRoot, ComId.SelfCom, result)
            ans = [
                {
                    "category": 1,
                    "image": None,
                    "name": ComId.DepartmentName,
                    "check": None,
                }
            ]

        for depart in result:
            ans.append(
                {
                    "category": depart.Depth + 1,
                    "image": None,
                    "name": depart.DepartmentName,
                    "check": None,
                }
            )

        return Response(ans, status=status.HTTP_200_OK)


class PreviewQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="Preview 화면에서 필요한 값들을 반환하는 Api",
        responses={200: "Api가 정상적으로 동작함", 406: "날짜가 범위를 초과함"},
    )
    def get(self, request, Depart, start, end, format=None):
        """
        요청한 부서의 탄소 배출량을 탄소 배출 원인별로 계산해 반환\n
        /start/end를 입력할 때 start는 조회하고 싶은 기간의 시작일, \n
        end는 조회하고 싶은 기간의 마지막날을 입력할 것.\n
        start, end 입력 예시) /2001-10-15/2002-10-15
        """

        # 요청한 user의 모회사 확인
        UserRoot = func.GetUserRoot(request)

        try:
            HeadDepart = ComModel.Department.objects.get(
                DepartmentName=Depart, RootCom=UserRoot
            )
        except ComModel.Department.DoesNotExist:
            HeadDepart = UserRoot

        IsRoot = 0
        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if type(HeadDepart) == ComModel.Company:
            Departs = []
            func.getChildDepart(UserRoot, None, Departs)
            IsRoot = 1

        else:
            Departs = [HeadDepart]
            func.getChildDepart(UserRoot, HeadDepart.SelfCom, Departs)

        start = func.AddZero(start)
        end = func.AddZero(end)

        # 연단위 인사이트 요청인지 월단위 인사이트 요청인지 확인
        if (
            func.diff_month(
                datetime.strptime(end, "%Y-%m-%d"),
                datetime.strptime(start, "%Y-%m-%d"),
            )
            >= 11
        ):
            MorY = 1
        else:
            MorY = 0

        Carbons = []
        for depart in Departs:
            try:
                if MorY == 0:
                    temp = CarModel.Carbon.objects.filter(
                        BelongDepart=depart,
                        CarbonInfo__StartDate__lte=datetime.strptime(start, "%Y-%m-%d"),
                        CarbonInfo__EndDate__gte=datetime.strptime(end, "%Y-%m-%d"),
                    )
                    Carbons.extend([i for i in temp])
                else:
                    temp = (
                        CarModel.Carbon.objects.filter(
                            BelongDepart=depart,
                            CarbonInfo__StartDate__gte=datetime.strptime(
                                start, "%Y-%m-%d"
                            ),
                            CarbonInfo__EndDate__lte=datetime.strptime(end, "%Y-%m-%d"),
                        )
                        | CarModel.Carbon.objects.filter(
                            BelongDepart=depart,
                            CarbonInfo__EndDate__range=(
                                datetime.strptime(start, "%Y-%m-%d"),
                                datetime.strptime(end, "%Y-%m-%d"),
                            ),
                        )
                        | CarModel.Carbon.objects.filter(
                            BelongDepart=depart,
                            CarbonInfo__StartDate__range=(
                                datetime.strptime(start, "%Y-%m-%d"),
                                datetime.strptime(end, "%Y-%m-%d"),
                            ),
                        )
                    )
                    Carbons.extend([i for i in temp])
            except ValueError:  # 날짜가 범위를 초과한 경우 ex) 1월 35일
                return Response(
                    "Date out of range", status=status.HTTP_406_NOT_ACCEPTABLE
                )

        scope1 = 0
        scope2 = 0
        scope3 = 0
        categories = [0] * CarbonDef.CarbonCateLen

        if IsRoot == 1:  # 요청한 데이터가 루트인 경우 depart가 아니라 데이터를 가져오지 못하므로 따로 가져옴
            try:
                if MorY == 0:
                    temp = CarModel.Carbon.objects.filter(
                        BelongDepart=None,
                        CarbonInfo__StartDate__lte=datetime.strptime(start, "%Y-%m-%d"),
                        CarbonInfo__EndDate__gte=datetime.strptime(end, "%Y-%m-%d"),
                    )
                    Carbons.extend([i for i in temp])
                else:
                    temp = (
                        CarModel.Carbon.objects.filter(
                            BelongDepart=None,
                            CarbonInfo__StartDate__gte=datetime.strptime(
                                start, "%Y-%m-%d"
                            ),
                            CarbonInfo__EndDate__lte=datetime.strptime(end, "%Y-%m-%d"),
                        )
                        | CarModel.Carbon.objects.filter(
                            BelongDepart=None,
                            CarbonInfo__EndDate__range=(
                                datetime.strptime(start, "%Y-%m-%d"),
                                datetime.strptime(end, "%Y-%m-%d"),
                            ),
                        )
                        | CarModel.Carbon.objects.filter(
                            BelongDepart=None,
                            CarbonInfo__StartDate__range=(
                                datetime.strptime(start, "%Y-%m-%d"),
                                datetime.strptime(end, "%Y-%m-%d"),
                            ),
                        )
                    )
                    Carbons.extend([i for i in temp])

            except ValueError:  # 날짜가 범위를 초과한 경우 ex) 1월 35일
                return Response(
                    "Date out of range", status=status.HTTP_406_NOT_ACCEPTABLE
                )

        for car in Carbons:
            TempScope = car.CarbonInfo.Scope
            DivideScope = func.DivideByMonthOrYear(
                car.CarbonInfo.StartDate,
                car.CarbonInfo.EndDate,
                car.CarbonTrans,
                MorY,
            )
            if TempScope == 1:
                scope1 += DivideScope
            elif TempScope == 2:
                scope2 += DivideScope
            elif TempScope == 3:
                scope3 += DivideScope

            TempCate = car.CarbonInfo.Category
            categories[TempCate] += DivideScope

        ans = {
            "Name": Depart,
            "Scopes": [round(scope1, 2), round(scope2, 2), round(scope3, 2)],
            "EmissionList": [
                {CarbonDef.CarbonCategories[i]: round(categories[i], 2)}
                for i in range(CarbonDef.CarbonCateLen)
            ],
        }

        return Response(ans, status=status.HTTP_200_OK)


class PreviewInfoQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="Company 혹은 Department의 데이터를 변경하는 Api",
        request_body=ComSerial.CompanySerializer,
        responses={
            202: "데이터가 문제없이 변경 됨",
            406: "입력한 데이터에 오류가 있음, 수정 요함",
            404: "요청한 회사가 존재하지 않음",
        },
    )
    def put(self, request, Depart, format=None):
        """
        요청한 부서 혹은 회사의 정보를 변경\n
        아래 data에 Scope1, 2, 3을 제외한 나머지 값들은 모두 채워져 있어야만 변경이 가능\n
        Chief와 Admin의 경우 해당 회사, 부서의 책임자와 관리자의 이름을 각각 입력\n
        """

        UserRoot = func.GetUserRoot(request)

        request = json.loads(request.body)

        # 요청받은 즉 변경할 row 가져오기
        try:
            ChangeData = ComModel.Department.objects.get(
                RootCom=UserRoot, DepartmentName=Depart
            )
        except ComModel.Department.DoesNotExist:  # 변경할 것이 루트인 경우
            try:
                ChangeData = ComModel.Company.objects.get(ComName=Depart)
            except ComModel.Company.DoesNotExist:  # 요청한 회사가 존재하지 않음
                return Response(
                    "This Company/Department does not exist.",
                    status=status.HTTP_404_NOT_FOUND,
                )

        if type(ChangeData) == ComModel.Department:
            ChangeData = ChangeData.SelfCom

        # 데이터 변경
        try:

            if request["ComName"] != None:
                ChangeData.ComName = request["ComName"]
            if request["Classification"] != None:
                ChangeData.Classification = request["Classification"]
            if request["Chief"] != None:
                ChangeData.Chief = HuModel.Employee.objects.get(Name=request["Chief"])
            if request["Admin"] != None:
                ChangeData.Admin = HuModel.Employee.objects.get(Name=request["Admin"])
            if request["Description"] != None:
                ChangeData.Description, request["Description"]

            if request["Location"] != None:
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

    @swagger_auto_schema(
        operation_summary="회사 삭제 Api", responses={200: "Api가 정상적으로 실행됨"}
    )
    def delete(self, request, Depart, format=None):
        """
        더 이상 탄소배출에 포함하지 않을 회사를 삭제하는 Api\n
        해당하는 회사의 이름을 URL에 입력하여 요청.\n
        단, 동일한 이름의 회사는 동일한 Root에서는 존재하지 않는다고 가정.
        """

        UserRoot = func.GetUserRoot(request)

        # 모회사를 삭제하는 경우
        if Depart == UserRoot.ComName:
            DelList = []
            func.getChildCom(UserRoot, None, DelList)

            for Com in DelList:
                Com.delete()

            return Response("Delete Complete", status=status.HTTP_200_OK)

        else:
            DelList = [
                ComModel.Department.objects.get(RootCom=UserRoot, DepartmentName=Depart)
            ]
            func.getChildCom(UserRoot, DelList[0].SelfCom, DelList)

            for Com in DelList:
                Com.delete()

            return Response("Delete Complete", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="회사 생성 Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ComName": ComSwag.ComName,
                "Scope1": ComSwag.Scope1,
                "Scope2": ComSwag.Scope2,
                "Scope3": ComSwag.Scope3,
                "Chief": ComSwag.Chief,
                "Admin": ComSwag.Admin,
                "Classification": ComSwag.Classification,
                "Description": ComSwag.Description,
                "Location": ComSwag.Location,
                "DepartmentName": ComSwag.DepartmentName,
                "Depth": ComSwag.Depth,
            },
        ),
        responses={200: "Api가 정상적으로 실행됨"},
    )
    def post(self, request, Depart, format=None):
        """
        조직 설계에서 회사을 생성하는 Api\n
        현재는 최하단의 회사만 추가 가능\n
        아래의 데이터를 모두 입력하여야 추가 가능\n
        다만 Chief, Admin, Classification, Description, Location은 None 입력 가능\n
        단 {Depart}는 추가할 회사의 바로 윗 회사이여야 함
        """
        UserRoot = func.GetUserRoot(request)

        ComData = request.data

        try:
            Chief = HuModel.Employee.objects.get(
                RootCom=UserRoot, Name=ComData["Chief"]
            )
        except HuModel.Employee.DoesNotExist:
            Chief = (None,)
        try:
            Admin = HuModel.Employee.objects.get(
                RootCom=UserRoot, Name=ComData["Admin"]
            )
        except HuModel.Employee.DoesNotExist:
            Admin = None

        if Depart == UserRoot.ComName:
            BelongCom = None
        else:
            BelongCom = ComModel.Department.objects.get(
                RootCom=UserRoot, DepartmentName=Depart
            )

        SelfCom = ComModel.Company.objects.create(
            ComName=ComData["ComName"],
            Scope1=ComData["Scope1"],
            Scope2=ComData["Scope2"],
            Scope3=ComData["Scope3"],
            Chief=Chief,
            Admin=Admin,
            Classification=ComData["Classification"],
            Description=ComData["Description"],
            Location=ComData["Location"],
        )

        if BelongCom == None:
            ans = ComModel.Department.objects.create(
                DepartmentName=ComData["DepartmentName"],
                RootCom=UserRoot,
                BelongCom=BelongCom,
                SelfCom=SelfCom,
                Depth=ComData["Depth"],
            )
        else:
            ans = ComModel.Department.objects.create(
                DepartmentName=ComData["DepartmentName"],
                RootCom=UserRoot,
                BelongCom=BelongCom.SelfCom,
                SelfCom=SelfCom,
                Depth=ComData["Depth"],
            )

        ans = ComSerial.DepartmentSerializer(ans)
        return Response(ans.data, status=status.HTTP_200_OK)

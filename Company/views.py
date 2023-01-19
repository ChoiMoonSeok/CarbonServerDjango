import json
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

import func
from Company import models as ComModel
from Carbon import models as CarModel
from Company import serializer as ComSerial
from Human import models as HuModel
from CarbonConstant import CarbonDef


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
        if result["Chief"] != None:
            result["Chief"] = HuModel.Employee.objects.get(id=result["Chief"]).Name
        result["Children"] = []

        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if ComId.id == UserRoot.id:
            func.getStruct(UserRoot, None, result)
        else:
            func.getStruct(UserRoot, ComId, result)

        return Response(result, status=status.HTTP_200_OK)


class CompanySimpleQuery(CompanyQuery):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    def get(self, request, CompanyName, format=None):

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
        responses={200: "Api가 정상적으로 동작함"},
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

        Departs = []
        IsRoot = 0
        # 요청한 회사가 루트인 경우 첫번째 자회사의 BelongCom이 None이므로 달라져야 함.
        if type(HeadDepart) == ComModel.Company:
            func.getChildDepart(UserRoot, None, Departs)
            IsRoot = 1
        else:
            func.getChildDepart(UserRoot, HeadDepart.SelfCom, Departs)

        Carbons = []
        start = start.split("-")
        for i in range(len(start)):
            if len(start[i]) < 2:
                start[i] = "0{}".format(start[i])

        num = 0
        temp = str()
        for i in start:
            temp += i
            if num != 2:
                temp += "-"
                num += 1
        start = temp
        del temp

        end = end.split("-")
        for i in range(len(end)):
            if len(end[i]) < 2:
                end[i] = "0{}".format(end[i])

        num = 0
        temp = str()
        for i in end:
            temp += i
            if num != 2:
                temp += "-"
                num += 1
        end = temp
        del temp

        for depart in Departs:
            temp = CarModel.Carbon.objects.filter(
                BelongDepart=depart,
                CarbonInfo__StartDate__gte=datetime.strptime(start, "%Y-%m-%d"),
                CarbonInfo__EndDate__lte=datetime.strptime(end, "%Y-%m-%d"),
            )
            Carbons.append(temp)

        scope1 = 0
        scope2 = 0
        scope3 = 0
        categories = [0] * CarbonDef.CarbonCateLen

        if IsRoot == 1:  # 요청한 데이터가 루트인 경우 depart가 아니라 데이터를 가져오지 못하므로 따로 가져옴
            temp = CarModel.Carbon.objects.filter(
                BelongDepart=None,
                CarbonInfo__StartDate__gte=datetime.strptime(start, "%Y-%m-%d"),
                CarbonInfo__EndDate__lte=datetime.strptime(end, "%Y-%m-%d"),
            )
            Carbons.append(temp)

        for car in Carbons:
            for each in car:
                TempScope = each.CarbonInfo.Scope
                if TempScope == 1:
                    scope1 += each.CarbonTrans
                elif TempScope == 2:
                    scope2 += each.CarbonTrans
                elif TempScope == 3:
                    scope3 += each.CarbonTrans

                TempCate = each.CarbonInfo.Category
                for i in range(CarbonDef.CarbonCateLen):
                    if i == TempCate:
                        categories[i] += each.CarbonTrans
                        break

        ans = {
            "Name": Depart,
            "Scopes": [scope1, scope2, scope3],
            "EmissionList": [
                {CarbonDef.CarbonCategories[i]: categories[i]}
                for i in range(CarbonDef.CarbonCateLen)
            ],
        }

        return Response(ans, status=status.HTTP_200_OK)


class PreviewInfoQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

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

    @swagger_auto_schema(operation_summary="회사 삭제 Api")
    def delete(self, request, Depart, format=None):
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

    @swagger_auto_schema(operation_summary="회사 생성 Api")
    def post(self, request, Depart, format=None):
        UserRoot = func.GetUserRoot(request)

        pass

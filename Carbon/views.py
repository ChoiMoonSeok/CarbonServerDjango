import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from . import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
from . import serializer
import func


class CarbonEmissionQuery(APIView):
    @swagger_auto_schema(operation_summary="탄소 배출량 목록 반환")
    def get(self, request, Depart, format=None):
        """요청받은 부서, 회사의 모든 탄소 배출 목록을 리스트로 반환"""

        # 현재 사용자의 소속 회사와 요청받은 회사를 비교
        # if Depart ==
        try:  # 요청받은 회사가 루트가 아닌 경우
            Root_id = ComModel.Department.objects.get(
                DepartmentName=Depart  # 로그인이 구현된 이후에는 사용자의 root와 비교
            )
        except ComModel.Department.DoesNotExist:  # 요청받은 회사가 루트인 경우
            try:
                Root_id = ComModel.Company.objects.get(ComName=Depart)
            except ComModel.Company.DoesNotExist:  # 요청받은 회사가 존재하지 않는 경우
                return Response("This Company/Department doesn't exist.")

        # 요청받은 회사가 루트인 경우
        if type(Root_id) == ComModel.Company:

            data = CarModel.Carbon.objects.filter(RootCom=Root_id)
            serial = serializer.CarbonSerializer(data, many=True)

            return Response(serial.data, status=status.HTTP_201_CREATED)

        else:  # 요청 받은 회사가 루트, 모회사가 아닌 경우
            Coms = [Root_id.SelfCom]
            func.getChildCom(Root_id.RootCom, Root_id.SelfCom, Coms)

            CarbonList = []
            for Com in Coms:
                temp = CarModel.Carbon.objects.filter(BelongCom=Com)
                serial = serializer.CarbonSerializer(temp, many=True)
                CarbonList += serial.data

            return Response(CarbonList, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Carbon")
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

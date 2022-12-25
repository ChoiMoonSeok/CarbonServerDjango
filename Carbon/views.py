import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

import Carbon.serializer
import func


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

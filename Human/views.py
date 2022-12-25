import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

# 사용자에 대한 api 함수

User_root = "삼성"


class User_EmployeeQuery(APIView):
    """
    모든 사용자를 리스트 형태로 반환하는 Api
    ---
    # 사용자
    """

    def get(self, request, Company, format=None):
        Users = User_Employee.objects.filter(Company=Company)
        serializer = User_EmployeeSerializer(Users, many=True)
        return Response(serializer.data)

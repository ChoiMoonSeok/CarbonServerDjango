from django.shortcuts import render
from Carbon.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

# 사용자에 대한 api 함수

class User_EmployeeQuery(APIView):
    '''
    모든 사용자를 리스트 형태로 반환
    '''
    def get(self, request, Company, format=None):
        Users = User_Employee.objects.filter(Company=Company)
        serializer = User_EmployeeSerializer(Users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = User_EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyQuery(APIView):
    '''
    지주회사가 동일한 모든 회사, 부서를 리스트 형태로 반환
    '''
    def get(self, request, CompanyName, format=None):
        ComId = Company.objects.get(ComName=CompanyName)
        Departments = Department.objects.filter(Mother=ComId)
        serializer = DepartmentSerializer(Departments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
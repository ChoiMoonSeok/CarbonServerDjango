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

        result = {'DepartmentName': CompanyName, 'depth' : 0, 'Scope1':ComId.Scope1, 'Scope2':ComId.Scope2, 'Scope3':ComId.Scope3, 'Children':[]}
    
        for i in serializer.data:
            i = dict(i)
            i['Children'] = []
            put_struct(result, i)

        return Response(result, status=status.HTTP_201_CREATED)

# 조직 구조를 반환하는 함수
def put_struct(result, Company):
    if Company['upper'] == None:
        result['Children'].append(Company)
        return 0
    elif result['depth'] == Company['depth'] - 1:
        print('hi')
        print(result)
        if result['id'] == Company['upper']:
            result['Children'].append(Company)
        else:
            return 0
    else:
        if len(result['Children']) != 0:
            for i in range(len(result['Children'])):
                temp = result['Children'][i]
                put_struct(temp, Company)
        else:
            if result['id'] == Company['upper']:
                result['Children'].append(Company)
            else:
                return 0
        

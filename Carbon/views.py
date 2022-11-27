from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from Carbon.serializer import *
import func

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
    회사와 관련된 값들을 다루는 api
    '''

    def get(self, request, CompanyName, format=None):
        '''
        지주회사가 동일한 모든 회사, 부서를 계층을 가진 형태로 반환.\
        ex) 삼성 dict 내부의 Children에 리스트 형태로 자회사 혹은 부서가 저장됨.
        '''
        ComId = Company.objects.get(ComName=CompanyName)
        Departments = Department.objects.filter(Mother=ComId)
        serializer = DepartmentSerializer(Departments, many=True)

        result = {'DepartmentName': CompanyName, 'depth' : 0, 'Scope1':ComId.Scope1,\
                  'Scope2':ComId.Scope2, 'Scope3':ComId.Scope3, 'Children':[]}
    
        for i in serializer.data:
            i = dict(i)
            i['Children'] = []
            func.put_struct(result, i)

        return Response(result, status=status.HTTP_201_CREATED)

class PreviewQuery(APIView):
    '''
    프리뷰와 관련된 내용을 다루는 api
    '''
    
    def get(self, request, root, Depart, format=None):
        '''
        요청한 부서의 탄소 배출량을 탄소 배출 원인별로 계산해 반환
        '''

        # root의 id와 Department의 id 가져오기
        Root_Id = Company.objects.get(ComName=root)
        Upper_Id = Department.objects.get(DepartmentName=Depart)
        Data = Carbon.objects.filter(Mother=Root_Id, upper=Upper_Id)
        
        

        return Response(0, status=status.HTTP_201_CREATED)
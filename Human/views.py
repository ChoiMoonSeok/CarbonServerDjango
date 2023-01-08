import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password


from Human import models as HuModel
from Human import serializer
from Company import models as ComModel
import func

# 사용자에 대한 api 함수


class User_EmployeeQuery(APIView):
    @swagger_auto_schema(
        operation_summary="입력한 회사와 그 자회사의 모든 직원을 가져오는 Api",
        responses={200: "API가 정상적으로 동작하고 종료 됨", 404: "입력한 회사가 존재하지 않음"},
    )
    def get(self, request, Company, format=None):
        """
        입력한 회사와 해당 회사의 자회사의 모든 소속 직원들의 정보를 가져옵니다.
        ex) 삼성전자를 호출하면 삼성전자의 모든 직원과 삼성전자의 자회사인 삼성디스플레이의 모든 직원이 반환 됨
        """
        U_Root = ComModel.Company.objects.get(ComName="samsung")  # 로그인 구현 후 변경 예정
        try:
            Root = ComModel.Department.objects.get(
                RootCom=U_Root, DepartmentName=Company
            )
        except ComModel.Department.DoesNotExist:
            try:
                Root = ComModel.Company.objects.get(ComName=Company)
            except ComModel.Company.DoesNotExist:
                return Response(
                    "This Company does not exist", status=status.HTTP_404_NOT_FOUND
                )

        if type(Root) == ComModel.Company:
            Employee = HuModel.Employee.objects.filter(RootCom=Root)
            serial = serializer.EmployeeSerializer(Employee, many=True)
            return Response(serial.data, status=status.HTTP_200_OK)

        else:
            Departs = [Root]
            func.getChildDepart(U_Root, Root.SelfCom, Departs)

            Employee = []
            for depart in Departs:

                temp = HuModel.Employee.objects.filter(RootCom=U_Root, BelongCom=depart)
                serial = serializer.EmployeeSerializer(temp, many=True)

                Employee.append(serial.data)

            return Response(Employee, status=status.HTTP_200_OK)


class LogInView(APIView):
    @swagger_auto_schema(
        operation_summary="로그인 Api",
        request_body=serializer.UserSerializer,
        responses={404: "입력한 사용자가 존재하지 않음", 406: "입력한 데이터가 불충분 함"},
    )
    def post(self, request, format=None):
        """
        사용자의 로그인을 위한 Api.\n
        jwt를 활용하며, 사용자의 Email과 비밀번호를 json의 형태로 입력받는다.\n
        입력값들은 request body에 위치하여야 한다.
        """

        UserData = request.data
        if type(UserData) is not None:
            Email = UserData["Email"]
            User = HuModel.User.objects.get(Email=Email)
            if type(User) == None:
                Response("Wrong Email address", status=status.HTTP_404_NOT_FOUND)

            PW = UserData["password"]
            if check_password(PW, User.password):  # 비밀 번호가 일치하는지 검사

                token = TokenObtainPairSerializer.get_token(User)
                refresh_token = str(token)
                access_token = str(token.access_token)
                return Response(
                    {
                        "Email": Email,
                        "AccessToken": access_token,
                        "RefreshToken": refresh_token,
                    }
                )
            else:
                return Response("Wrong PassWord.", status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                "Please Complete the data", status=status.HTTP_406_NOT_ACCEPTABLE
            )


class SignUpView(APIView):
    @swagger_auto_schema(
        operation_summary="회원가입 Api", request_body=serializer.SignUpSerializer
    )
    def post(self, request, formant=None):
        UserData = request.data
        TempEmail = HuModel.User.objects.filter(Email=UserData["Email"])

        if len(TempEmail) == 0:
            EmployeeData = UserData["DetailInfo"]
            Detail = HuModel.Employee.objects.create(
                Name=EmployeeData["Name"],
                PhoneNum=EmployeeData["PhoneNum"],
                JobPos=EmployeeData["JobPos"],
                IdentityNum=EmployeeData["IdentityNum"],
                Authorization=EmployeeData["Authorization"],
                RootCom=ComModel.Company.objects.get(ComName=EmployeeData["BelongCom"]),
                BelongCom=ComModel.Department.objects.get(
                    DepartmentName=EmployeeData["BelongCom"]
                ),
            )

            NewUser = HuModel.User.objects.create(
                Email=UserData["Email"],
                DetailInfo=Detail,
                password=UserData["password"],
            )

            Detail.save()
            NewUser.save()

            serial = serializer.UserSerializer(NewUser)
            return Response(serial.data, status=status.HTTP_200_OK)

        else:
            return Response(
                "This account already exist.", status=status.HTTP_400_BAD_REQUEST
            )

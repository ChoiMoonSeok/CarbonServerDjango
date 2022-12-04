import datetime

import Carbon.models


def CreateSamsung():
    Carbon.models.User_Employee.objects.create(
        Name="이재용",
        PhoneNum="123456789",
        Email="1234@naver.com",
        Company="삼성",
        JobPos="회장",
        IdentityNum="1",
        Authorization=0,
    )
    Carbon.models.Company.objects.create(
        ComName="삼성",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
    )
    Carbon.models.Department.objects.create(
        id=1,
        DepartmentName="삼성전자",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
        depth=1,
        upper=None,
        Mother=Carbon.models.Company.objects.get(ComName="삼성"),
    )
    Carbon.models.Department.objects.create(
        id=2,
        DepartmentName="삼성생명",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
        depth=1,
        upper=None,
        Mother=Carbon.models.Company.objects.get(ComName="삼성"),
    )
    Carbon.models.Department.objects.create(
        id=3,
        DepartmentName="삼성디스플레이",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        chief=Carbon.models.User_Employee.objects.get(Name="이재용"),
        depth=2,
        upper=Carbon.models.Department.objects.get(DepartmentName="삼성전자"),
        Mother=Carbon.models.Company.objects.get(ComName="삼성"),
    )

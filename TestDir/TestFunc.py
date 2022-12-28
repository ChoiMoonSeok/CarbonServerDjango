import datetime

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel


def CreateSamsung():
    HuModel.Employee.objects.create(
        Name="이재용",
        PhoneNum="123456789",
        Email="1234@naver.com",
        JobPos="회장",
        IdentityNum="1",
    )
    HuModel.Employee.objects.create(
        Name="노태문",
        PhoneNum="123456789",
        Email="1234@naver.com",
        JobPos="사장",
        IdentityNum="2",
    )
    HuModel.Employee.objects.create(
        Name="고동진",
        PhoneNum="123456789",
        Email="12345@naver.com",
        JobPos="사원",
        IdentityNum="3",
    )
    HuModel.Employee.objects.create(
        Name="경계현",
        PhoneNum="123456789",
        Email="123456@naver.com",
        JobPos="대리",
        IdentityNum="4",
    )
    ComModel.Company.objects.create(
        ComName="삼성",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        Chief=HuModel.Employee.objects.get(Name="이재용"),
    )
    ComModel.Company.objects.create(
        ComName="삼성전자",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        Chief=HuModel.Employee.objects.get(Name="이재용"),
    )
    ComModel.Department.objects.create(
        DepartmentName="삼성전자",
        Depth=1,
        BelongCom=None,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        SelfCom=ComModel.Company.objects.get(ComName="삼성전자"),
    )
    ComModel.Company.objects.create(
        ComName="삼성생명",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        Chief=HuModel.Employee.objects.get(Name="이재용"),
    )
    ComModel.Department.objects.create(
        DepartmentName="삼성생명",
        Depth=1,
        BelongCom=None,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        SelfCom=ComModel.Company.objects.get(ComName="삼성생명"),
    )
    ComModel.Company.objects.create(
        ComName="삼성디스플레이",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        Chief=HuModel.Employee.objects.get(Name="이재용"),
    )
    ComModel.Department.objects.create(
        DepartmentName="삼성디스플레이",
        Depth=2,
        BelongCom=ComModel.Company.objects.get(ComName="삼성전자"),
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        SelfCom=ComModel.Company.objects.get(ComName="삼성디스플레이"),
    )

    CarModel.Carbon.objects.create(
        CarbonActivity="김재호 교수 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        BelongDepart=None,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="김재호 교수 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성전자"),
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="정혜미 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성디스플레이"),
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="정대호 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성생명"),
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="최문석 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="삼성"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성전자"),
    )

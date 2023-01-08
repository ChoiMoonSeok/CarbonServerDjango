import datetime

from Carbon import models as CarModel
from Human import models as HuModel
from Company import models as ComModel


def CreateSamsung():
    HuModel.Employee.objects.create(
        Name="이재용",
        PhoneNum="123456789",
        JobPos="회장",
        IdentityNum="1",
    )
    ComModel.Company.objects.create(
        ComName="samsung",
        Scope1=0,
        Scope2=0,
        Scope3=0,
        Chief=HuModel.Employee.objects.get(Name="이재용"),
    )
    HuModel.User.objects.create(
        Email="1234@naver.com",
        DetailInfo=HuModel.Employee.objects.get(Name="이재용"),
        password="hi",
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
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
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
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
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
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        SelfCom=ComModel.Company.objects.get(ComName="삼성디스플레이"),
    )
    CarModel.CarbonInfo.objects.create(
        id=1,
        StartDate=datetime.date(2023, 1, 1),
        EndDate=datetime.date(2023, 1, 31),
        Location="진주",
        Scope=1,
        Category=12,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="김재호 교수 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongDepart=None,
        CarbonInfo=CarModel.CarbonInfo.objects.get(id=1),
    )
    CarModel.CarbonInfo.objects.create(
        id=2,
        StartDate=datetime.date(2022, 12, 1),
        EndDate=datetime.date(2023, 1, 1),
        Location="진주",
        Scope=1,
        Category=12,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="김재호 교수 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성전자"),
        CarbonInfo=CarModel.CarbonInfo.objects.get(id=2),
    )
    CarModel.CarbonInfo.objects.create(
        id=3,
        StartDate=datetime.date(2022, 12, 1),
        EndDate=datetime.date(2023, 1, 1),
        Location="진주",
        Scope=2,
        Category=11,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="정혜미 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성디스플레이"),
        CarbonInfo=CarModel.CarbonInfo.objects.get(id=3),
    )
    CarModel.CarbonInfo.objects.create(
        id=4,
        StartDate=datetime.date(2022, 1, 1),
        EndDate=datetime.date(2023, 1, 1),
        Location="진주",
        Scope=2,
        Category=11,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="정대호 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성생명"),
        CarbonInfo=CarModel.CarbonInfo.objects.get(id=4),
    )
    CarModel.CarbonInfo.objects.create(
        id=5,
        StartDate=datetime.date.today(),
        EndDate=datetime.date.today(),
        Location="진주",
        Scope=3,
        Category=10,
    )
    CarModel.Carbon.objects.create(
        CarbonActivity="최문석 출장",
        CarbonData=20.0,
        CarbonUnit="kg",
        CarbonTrans=20.0,
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongDepart=ComModel.Department.objects.get(DepartmentName="삼성전자"),
        CarbonInfo=CarModel.CarbonInfo.objects.get(id=5),
    )
    HuModel.Employee.objects.create(
        Name="노태문",
        PhoneNum="123456789",
        JobPos="사장",
        IdentityNum="2",
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongCom=ComModel.Department.objects.get(DepartmentName="삼성전자"),
    )
    HuModel.User.objects.create(
        Email="12345@naver.com",
        password="hihi",
        DetailInfo=HuModel.Employee.objects.get(Name="노태문"),
    )
    HuModel.Employee.objects.create(
        Name="고동진",
        PhoneNum="123456789",
        JobPos="사원",
        IdentityNum="3",
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongCom=ComModel.Department.objects.get(DepartmentName="삼성생명"),
    )
    HuModel.User.objects.create(
        Email="123456@naver.com",
        password="hihihi",
        DetailInfo=HuModel.Employee.objects.get(Name="고동진"),
    )
    HuModel.Employee.objects.create(
        Name="경계현",
        PhoneNum="123456789",
        JobPos="대리",
        IdentityNum="4",
        RootCom=ComModel.Company.objects.get(ComName="samsung"),
        BelongCom=ComModel.Department.objects.get(DepartmentName="삼성디스플레이"),
    )
    HuModel.User.objects.create(
        Email="1234567@naver.com",
        password="hihihihi",
        DetailInfo=HuModel.Employee.objects.get(Name="경계현"),
    )

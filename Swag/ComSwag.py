from drf_yasg import openapi

from . import CarSwag

ComName = openapi.Schema(type=openapi.TYPE_STRING, description="회사명")

Scope1 = openapi.Schema(type=openapi.TYPE_INTEGER, description="해당 회사의 Scope1 탄소 배출량")

Scope2 = openapi.Schema(type=openapi.TYPE_INTEGER, description="해당 회사의 Scope2 탄소 배출량")

Scope3 = openapi.Schema(type=openapi.TYPE_INTEGER, description="해당 회사의 Scope3 탄소 배출량")

Chief = CarSwag.Chief

Admin = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="해당 회사의 관리자 이름\n\
            ex) 홍길동",
)

Classification = openapi.Schema(
    type=openapi.TYPE_STRING, description="해당 회사의 Scope1 탄소 배출량"
)

Description = openapi.Schema(type=openapi.TYPE_STRING, description="해당 회사에 대한 간략한 설명")

Location = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="해당 회사의 소재지\n\
            ex) 진주, 부산, 서울 etc",
)

DepartmentName = openapi.Schema(type=openapi.TYPE_STRING, description="회사명 혹은 부서명")

Depth = openapi.Schema(
    type=openapi.TYPE_INTEGER,
    description="해당 회사의 깊이\n\
            ex) 삼성의 자회사 삼성전자의 깊이는 1",
)

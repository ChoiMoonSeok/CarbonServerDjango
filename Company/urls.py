from django.urls import path

from . import views

app_name = "Company"
urlpatterns = [
    path(
        "Organization/<str:CompanyName>", views.CompanyQuery.as_view(), name="OrganGet"
    ),  # 최상위회사 이름으로 조직 설계도 호출
    path(
        "Preview/<str:Depart>", views.PreviewQuery.as_view(), name="CarbonGet"
    ),  # 회사의 탄소 배출량 합계
    path(
        "PreviewInfo/<str:Depart>", views.PreviewInfoQuery.as_view(), name="InfoPut"
    ),  # 회사의 정보 변경
]

"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Carbon import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("admin", admin.site.urls),
    path("User", views.User_EmployeeQuery.as_view()),
    path(
        "User/<str:Company>", views.User_EmployeeQuery.as_view(), name="get"
    ),  # 조직설계에서 구성원 호출
    path(
        "Organization/<str:CompanyName>", views.CompanyQuery.as_view(), name="get"
    ),  # 최상위회사 이름으로 조직 설계도 호출
    path(
        "Preview/<str:Depart>", views.PreviewQuery.as_view(), name="get"
    ),  # 회사의 탄소 배출량 합계
    path(
        "PreviewInfo/<str:Depart>", views.PreviewQuery.as_view(), name="put"
    ),  # 회사의 정보 변경
    path(
        "CarbonEmission/<str:Depart>",
        views.CarbonEmissionQuery.as_view(),
        name="get",
    ),
    path(
        "CarbonEmission/<str:Depart>",
        views.CarbonEmissionQuery.as_view(),
        name="post",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

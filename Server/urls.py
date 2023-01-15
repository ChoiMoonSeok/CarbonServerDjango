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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from Carbon import views

schema_view = get_schema_view(
    openapi.Info(
        title="CarbonServer",
        default_version="0.0.0",
        description="해당 서버는 bigsys data lab의 탄소 배출 측정 연구 과제를 위한 api 서버입니다.\n\
            Login과 Signin을 제외한 모든 API는 jwt인증이 필요합니다.\n\
                swagger 활용을 위해 api 인증이 필요한 경우, 우측의 Authorize 버튼을 눌러 검증한 후 실행하십시요.\n\
                    ex) Bearer (User/Login에서 얻은 Access jwt)",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # swagger를 이용한 자동 문서화를 위해 필요한 url
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    # api의 url
    path("admin", admin.site.urls),
    path("User/", include("Human.urls")),
    path("CarbonEmission/", include("Carbon.urls")),
    path("Company/", include("Company.urls")),
]

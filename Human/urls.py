from django.urls import path

from . import views

app_name = "Human"
urlpatterns = [
    path(
        "<str:Company>", views.User_EmployeeQuery.as_view(), name="get"
    ),  # 조직설계에서 구성원 호출
]

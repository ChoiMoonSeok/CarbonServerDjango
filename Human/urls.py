from django.urls import path

from . import views

app_name = "Human"
urlpatterns = [
    # 로그인/회원가입
    path("login", views.LogInView.as_view(), name="login"),
    # path("signup/", JWTSignupView.as_view()),
    # # 토큰
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "<str:Company>", views.User_EmployeeQuery.as_view(), name="get"
    ),  # 조직설계에서 구성원 호출
]

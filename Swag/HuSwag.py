from drf_yasg import openapi

Email = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            로그인 할 유저의 email 주소\n\
            ex) 홍길동 유저가 회원가입시 email에 hong@gnu.ac.kr을 입력했다면\
                hong@gnu.ac.kr 을 입력",
)

password = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            로그인 할 유저의 비밀번호\n\
            ex) 홍길동 유저가 회원가입시 비밀번호로 1234를 입력했다면\
                1234 를 입력",
)
